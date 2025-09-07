import logging
from logging import Logger
from operator import itemgetter, or_
import random
from typing import Dict, List
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.infra.auth import get_password_hash
from app.models.auth_models import User
from app.models.dag_models import DAG, KC
from app.models.question_models import Exam, ExamDetail, Question, Option, SimulatedExamData, SimulatedExamDataRaw, SimulatedStudentData  # adjust to your actual file/module names
from app.models.student_models import Mastery, Profile
from app.schemas.question_schemas import QuestionCreate, QuestionUpdate, QuestionOut
from app.infra.response_handlers import OkResponse, BadRequestException, ResourceNotFoundException
from app.services.processors.dag_util import DagUtil

class BayesianUpdater:
    """
    Implements probabilistic Bayesian mastery updating.
    """
    @staticmethod
    def update_mastery(
        dag_id: int,
        kc_id: int,
        profile_id: int,
        previous_mastery: float,
        is_correct: bool,
        db: Session,
        logger: Logger = None,
    ) -> float:
        """
        Update mastery using Bayesian inference with slip and guess parameters.
        """

        # Parameters (tunable)
        slip = 0.2   # chance student fails despite mastery
        guess = 0.25 # chance student succeeds without mastery

        prior = previous_mastery
        if is_correct:
            likelihood = slip * prior + guess * (1 - prior)
            posterior = (slip * prior) / likelihood if likelihood > 0 else prior
        else:
            p_incorrect_if_mastered = 1 - slip
            p_incorrect_if_not = 1 - guess
            likelihood = p_incorrect_if_mastered * prior + p_incorrect_if_not * (1 - prior)
            posterior = (p_incorrect_if_mastered * prior) / likelihood if likelihood > 0 else prior

        # Smooth update
        learning_rate = 0.2
        new_mastery = (1 - learning_rate) * prior + learning_rate * posterior
        new_mastery = max(0.0, min(1.0, new_mastery))  
        
        if logger:
            logger.info(
                f"[BayesianUpdater] Profile {profile_id}, KC {kc_id} → {new_mastery:.4f} "
                f"(was {prior:.4f}, correct={is_correct})"
            )

        return new_mastery
    
    @staticmethod
    def update_mastery_using_simple_method(dag_id:int, kc_id:int, profile_id:int, current_mastery:float, is_correct:bool, db: Session, logger: Logger = None) -> float:        
        percentage = random.uniform(0.1, 0.2)
        change = current_mastery * percentage 
        
        if is_correct:
            new_mastery = current_mastery + change
            action = "increased"
        else:
            new_mastery = current_mastery - change
            action = "decreased"

        # Clamp mastery between 0.0 and 1.0
        new_mastery = max(0.0, min(1.0, new_mastery))

        if logger:
            logger.info(
                f"Mastery for profile {profile_id}, KC {kc_id}, DAG {dag_id} {action} by {percentage:.2%} → {new_mastery:.4f}"
            )

        return new_mastery 
    
    @staticmethod
    def get_kc_masteries(exam_id: int, db: Session, logger: Logger = None) -> list:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            return []

        # All KC titles
        kc_map = {k.id: k.title for k in db.query(KC).all()}

        # Masteries recorded for the student
        kc_mastery_map = {
            m.kc_id: m.mastery
            for m in db.query(Mastery).filter(Mastery.profile_id == exam.student_id).all()
        }

        # Exam-specific average masteries
        exam_mastery_data = (
            db.query(
                ExamDetail.kc_id,
                func.avg(ExamDetail.previous_mastery).label("avg_previous_mastery"),
                func.avg(ExamDetail.current_mastery).label("avg_current_mastery"),
            )
            .filter(ExamDetail.exam_id == exam_id)
            .group_by(ExamDetail.kc_id)
            .all()
        )

        exam_mastery_map = {
            kc_id: {
                "avg_previous_mastery": avg_prev,
                "avg_current_mastery": avg_curr,
            }
            for kc_id, avg_prev, avg_curr in exam_mastery_data
        }

        # Build output with fallbacks
        output = []
        for kc_id, title in kc_map.items():
            if kc_id in exam_mastery_map:
                prev = exam_mastery_map[kc_id]["avg_previous_mastery"]
                curr = exam_mastery_map[kc_id]["avg_current_mastery"]
            elif kc_id in kc_mastery_map:
                prev = curr = kc_mastery_map[kc_id]
            else:
                prev = curr = 0.0

            output.append(
                {
                    "kc": title,
                    "previous_mastery": prev,
                    "current_mastery": curr,
                }
            )

        return output
    
    
     