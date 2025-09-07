from logging import Logger
import random
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.question_models import Option, Question
from app.models.student_models import Mastery, Profile
from app.models.dag_models import KC
import math

class WeakComponentIdentifier:

    # BKT parameters — tunable per KC or globally
    P_T = 0.1  # Learning probability
    P_G = 0.2  # Guess probability
    P_S = 0.1  # Slip probability

    @staticmethod
    def bkt_update(p_mastery, is_correct: bool):
        """
        Update mastery probability using BKT equations.
        """
        if is_correct:
            p_mastery_post = (p_mastery * (1 - WeakComponentIdentifier.P_S)) / (
                p_mastery * (1 - WeakComponentIdentifier.P_S) + (1 - p_mastery) * WeakComponentIdentifier.P_G
            )
        else:
            p_mastery_post = (p_mastery * WeakComponentIdentifier.P_S) / (
                p_mastery * WeakComponentIdentifier.P_S + (1 - p_mastery) * (1 - WeakComponentIdentifier.P_G)
            )

        # Learning step
        p_mastery_post = p_mastery_post + (1 - p_mastery_post) * WeakComponentIdentifier.P_T
        return min(max(p_mastery_post, 0.0), 1.0)

    @staticmethod
    def get_weakest_kc_bkt(profile_id: int, threshold: float, db: Session, logger: Logger = None):
        """
        Get the KC with lowest mastery probability using BKT.
        """
        stmt = select(Mastery.kc_id, Mastery.mastery).where(Mastery.profile_id == profile_id)
        results = db.execute(stmt).all()
        if not results:
            if logger:
                logger.warning(f"No mastery records found for profile {profile_id}")
            return None

        weakest_kc_id = None
        weakest_mastery = 1.0

        for kc_id, mastery in results:
            # Here we simulate one BKT update assuming last answer was incorrect (conservative)
            updated_mastery = WeakComponentIdentifier.bkt_update(mastery, is_correct=False)
            if updated_mastery < weakest_mastery:
                weakest_mastery = updated_mastery
                weakest_kc_id = kc_id

        if weakest_mastery >= threshold:
            return None

        return weakest_kc_id

    @staticmethod
    def get_question_from_kc(kc_id: int, db: Session):
        stmt = select(Question).where(Question.kc_id == kc_id)
        questions = db.execute(stmt).scalars().all()
        if not questions:
            return None
        return random.choice(questions)

    @staticmethod
    def get_question_with_options(profile_id: int, threshold: float, db: Session, logger: Logger = None):
        """
        Return a question from the weakest KC (BKT-based) with its options.
        Signature and return type kept same as before.
        """
        # 1. Find weakest KC using BKT
        kc_id = WeakComponentIdentifier.get_weakest_kc_bkt(profile_id, threshold, db, logger)
        if not kc_id:
            return None

        # 2. Pick a random question
        question = WeakComponentIdentifier.get_question_from_kc(kc_id, db)
        if not question:
            return None

        # 3. Fetch options
        stmt = select(Option).where(Option.question_id == question.id).order_by(Option.order)
        options = db.execute(stmt).scalars().all()

        return {
            "kc_id": kc_id,
            "question_id": question.id,
            "question_text": question.title,
            "options": [{"id": o.id, "text": o.text, "order": o.order} for o in options],
        }
