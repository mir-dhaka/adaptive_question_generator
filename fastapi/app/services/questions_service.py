import logging
from logging import Logger
from sqlalchemy.orm import Session
from app.models.question_models import Question, Option  # adjust to your actual file/module names
from app.schemas.question_schemas import QuestionCreate, QuestionUpdate, QuestionOut
from app.infra.response_handlers import OkResponse, BadRequestException, ResourceNotFoundException


class QuestionService:
    @staticmethod
    def create_question(question_data: QuestionCreate, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Creating question: title={question_data.title}, kc_id={question_data.kc_id}")

        # Optional: Prevent duplicate question titles for the same KC
        existing = db.query(Question).filter(
            Question.kc_id == question_data.kc_id,
            Question.title == question_data.title
        ).first()
        if existing:
            logger.warning("Question with this title already exists for the given KC")
            raise BadRequestException("Question already exists for this KC.")

        new_question = Question(
            kc_id=question_data.kc_id,
            title=question_data.title,
            correct_option=question_data.correct_option
        )
        db.add(new_question)
        db.flush()  # get ID before adding options

        # Add options
        for opt in question_data.options:
            option = Option(
                question_id=new_question.id,
                text=opt.text,
                order=opt.order
            )
            db.add(option)

        db.commit()
        db.refresh(new_question)

        logger.info(f"Created question with ID {new_question.id}")
        return OkResponse(QuestionOut.from_orm(new_question))

    @staticmethod
    def get_question(question_id: int, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Fetching question ID {question_id}")

        question = db.query(Question).get(question_id)
        if not question:
            logger.warning(f"Question ID {question_id} not found")
            raise ResourceNotFoundException("Question not found.")

        return OkResponse(QuestionOut.from_orm(question))

    @staticmethod
    def update_question(question_id: int, question_data: QuestionUpdate, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Updating question ID {question_id}")

        question = db.query(Question).get(question_id)
        if not question:
            logger.warning(f"Question ID {question_id} not found")
            raise ResourceNotFoundException("Question not found.")

        for field, value in question_data.dict(exclude_unset=True).items():
            setattr(question, field, value)

        db.commit()
        db.refresh(question)

        logger.info(f"Updated question ID {question_id}")
        return OkResponse(QuestionOut.from_orm(question))

    @staticmethod
    def delete_question(question_id: int, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Deleting question ID {question_id}")

        question = db.query(Question).get(question_id)
        if not question:
            logger.warning(f"Question ID {question_id} not found")
            raise ResourceNotFoundException("Question not found.")

        db.delete(question)
        db.commit()

        logger.info(f"Deleted question ID {question_id}")
        return OkResponse(message=f"Question ID {question_id} deleted successfully.")

    @staticmethod
    def list_questions(db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info("Listing all questions")

        questions = db.query(Question).all()
        questions_out = [QuestionOut.from_orm(q) for q in questions]

        return OkResponse({"questions": questions_out})
