import logging
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.infra.response_handlers import ResourceNotFoundException, BadRequestException
from app.schemas.question_schemas import QuestionCreate, QuestionUpdate
from app.services.questions_service import QuestionService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/",
    summary="Create a new question",
    description="Adds a new question and its options to the system",
)
def create_question(
    question_data: QuestionCreate = Body(...),
    db: Session = Depends(get_db)
):
    return QuestionService.create_question(question_data, db, logger)


@router.get(
    "/{question_id}",
    summary="Get a specific question",
    description="Fetches question details by its ID",
)
def get_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    return QuestionService.get_question(question_id, db, logger)


@router.put(
    "/{question_id}",
    summary="Update an existing question",
    description="Updates question details and options",
)
def update_question(
    question_id: int,
    question_data: QuestionUpdate = Body(...),
    db: Session = Depends(get_db)
):
    return QuestionService.update_question(question_id, question_data, db, logger)


@router.delete(
    "/{question_id}",
    summary="Delete a question",
    description="Removes a question and its options from the system",
)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    return QuestionService.delete_question(question_id, db, logger)


@router.get(
    "/",
    summary="List all questions",
    description="Fetches a list of all questions and their options",
)
def list_questions(
    db: Session = Depends(get_db)
):
    return QuestionService.list_questions(db, logger)
