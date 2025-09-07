from logging import Logger 
import random 
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.question_models import Option, Question
from app.models.student_models import Mastery, Profile
from app.models.dag_models import KC  

class WeakComponentIdentifier:
    @staticmethod
    def get_weakest_kc(profile_id: int, threshold: float, db: Session, logger=None):
        """
        Get the weakest KC for a student profile.
        """
        stmt = (
            select(Mastery.kc_id, Mastery.mastery)
            .where(Mastery.profile_id == profile_id)
            .order_by(Mastery.mastery.asc())
        )
        result = db.execute(stmt).all()

        if not result:
            if logger:
                logger.warning(f"No mastery records found for profile {profile_id}")
            return None

        kc_id, score = result[0]
        return kc_id if score < threshold else None

    @staticmethod
    def get_question_from_kc(kc_id: int, db: Session):
        """
        Get one random question for a given KC.
        """
        stmt = select(Question).where(Question.kc_id == kc_id)
        questions = db.execute(stmt).scalars().all()
        if not questions:
            return None
        return random.choice(questions)

    @staticmethod
    def get_question_with_options(profile_id: int, threshold: float, db: Session, logger=None):
        """
        Return a question from the weakest KC with its options.
        """
        # 1. Find weakest KC
        kc_id = WeakComponentIdentifier.get_weakest_kc(profile_id, threshold, db, logger)
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
        
    def use_case():         
        # # Example usage inside a handler
        # suggestion = WeakComponentIdentifier.get_question_with_options(
        #     profile_id=42, threshold=0.6, db=session, logger=logger
        # )

        # if suggestion:
        #     print("Weakest KC Question:", suggestion)
        # else:
        #     print("No weak KC found or no questions available.")
        pass
            

# class WeaknessIdentifier:
#     """
#     Identifies weak KCs and provides counterfactual improvement simulations.
#     """

#     @staticmethod
#     def find_weak_components(
#         profile_id: int,
#         threshold: float,
#         db: Session,
#         logger: Logger = None,
#     ) -> list:
#         """
#         Return list of weak KCs below mastery threshold.
#         """
#         weak = (
#             db.query(Mastery)
#             .filter(Mastery.profile_id == profile_id, Mastery.mastery < threshold)
#             .all()
#         )

#         kc_ids = [m.kc_id for m in weak]
#         kc_titles = (
#             db.query(KC)
#             .filter(KC.id.in_(kc_ids))
#             .all()
#         )

#         result = [{"kc_id": kc.id, "kc": kc.title, "mastery": m.mastery} 
#                   for kc in kc_titles 
#                   for m in weak if m.kc_id == kc.id]

#         if logger:
#             logger.info(
#                 f"[WeaknessIdentifier] Profile {profile_id} weak KCs → {result}"
#             )

#         return result

#     @staticmethod
#     def counterfactual_improvement(
#         profile_id: int,
#         kc_id: int,
#         delta: float,
#         db: Session,
#         logger: Logger = None,
#     ) -> float:
#         """
#         Hypothetically increase mastery of a KC by delta.
#         Does not persist — used for 'what-if' reasoning.
#         """
#         mastery_row = (
#             db.query(Mastery)
#             .filter(Mastery.profile_id == profile_id, Mastery.kc_id == kc_id)
#             .first()
#         )
#         if not mastery_row:
#             return 0.0

#         new_value = min(1.0, mastery_row.mastery + delta)

#         if logger:
#             logger.info(
#                 f"[WeaknessIdentifier] Counterfactual: Profile {profile_id}, KC {kc_id} → {new_value:.4f} "
#                 f"(original {mastery_row.mastery:.4f}, +{delta:.2f})"
#             )

#         return new_value

#     @staticmethod
#     def suggest_focus(
#         profile_id: int,
#         threshold: float,
#         db: Session,
#         logger: Logger = None,
#     ) -> str:
#         """
#         Suggest the weakest KC for targeted learning.
#         """
#         weak_components = WeaknessIdentifier.find_weak_components(profile_id, threshold, db, logger)
#         if not weak_components:
#             return "No major weaknesses detected."

#         weakest = min(weak_components, key=lambda x: x["mastery"])
#         suggestion = f"Focus on improving '{weakest['kc']}' (mastery {weakest['mastery']:.2f})"

#         if logger:
#             logger.info(f"[WeaknessIdentifier] Suggestion → {suggestion}")

#         return suggestion