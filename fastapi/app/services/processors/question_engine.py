from logging import Logger
import random
from sqlalchemy.orm import Session
from app.services.processors.bkt_weak_component_identifier import WeakComponentIdentifier
#from app.services.processors.rule_based_weak_component_identifier import WeakComponentIdentifier

class QuestionEngine: 
    @staticmethod
    def generate_next_question(kc_question_option_list:list, profile_id: int, dag_id: int, db: Session, logger: Logger = None) -> list:        
        # get suggested weak kcs
        suggestion = WeakComponentIdentifier.get_question_with_options(
            profile_id=profile_id, threshold=0.6, db=db, logger=logger
        )

        # Extract question_id safely
        question_id = suggestion.get("question_id") if suggestion else None

        # Try to find the matching question
        next_question = None
        if question_id:
            next_question = next((obj for obj in kc_question_option_list if obj.id == question_id), None)

        # Fallback: random selection if not found
        if not next_question:
            next_question = random.choice(kc_question_option_list)

        return next_question 