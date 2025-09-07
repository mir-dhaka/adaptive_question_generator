import base64
from collections import defaultdict
import json
import logging
from logging import Logger
from operator import itemgetter, or_
import random
from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import aliased
from sqlalchemy import select, text

from app.models.auth_models import User
from app.models.dag_models import DAG, KC
from app.models.question_models import Exam, ExamDetail, Question, Option, SimulatedExamData, SimulatedStudentData  # adjust to your actual file/module names
from app.models.student_models import Mastery, Profile
from app.schemas.question_schemas import QuestionCreate, QuestionUpdate, QuestionOut
from app.infra.response_handlers import OkResponse, BadRequestException, ResourceNotFoundException
from app.services.processors.bayesian_updater import BayesianUpdater
from app.services.processors.question_engine import QuestionEngine
from cachetools import TTLCache, cached

kc_question_option_list_cache = TTLCache(maxsize=100, ttl=60)

class GetProcessors:
    @staticmethod
    def get_student_dag_info(data: dict, db: Session, logger: Logger = None) -> list[dict]:   
        result = (
            db.query(
                User.id.label("user_id"),
                User.first_name,
                User.last_name,
                User.email,
                Profile.id.label("profile_id"),
                DAG.id.label("dag_id"),
                DAG.title.label("dag_title")
            )
            .join(Profile, Profile.user_id == User.id) 
            .join(DAG, Profile.dag_id == DAG.id)
            .order_by(User.first_name)
            .all()
        )

        if not result:
            if logger:
                logger.warning("No student information found")
            return []

        return [
            {
                "user_id": r.user_id,
                "name": f"{r.first_name} {r.last_name}",
                "email": r.email,
                "profile_id": r.profile_id,
                "dag_id": r.dag_id, 
                "dag_title": r.dag_title, 
                "title": f"{r.first_name} {r.last_name} - {r.dag_title}"
            }
            for r in result
        ]
        
    @staticmethod
    def get_exam_info(data: dict, db: Session, logger: Logger = None) -> list[dict]:   
        student_id = data.get("student_id")
        result = db.query(Exam).filter(Exam.student_id == student_id).all()

        if not result:
            if logger:
                logger.warning("No exam information found")
            return []

        output = []
        for r in result:
            try:
                decoded_info = json.loads(
                    base64.b64decode(r.exam_info).decode("utf-8")
                )
                finished_at = decoded_info.get("finished_at")
            except Exception as e:
                if logger:
                    logger.error(f"Failed to decode exam_info for Exam {r.id}: {e}")
                finished_at = None

            output.append(
                {
                    "id": r.id,
                    "title": f" Exam Finished at {finished_at}" if finished_at else f"Not finished with {r.id}"
                }
            )

        return output
        
    @staticmethod
    def get_exam_detail_info(data: dict, db: Session, logger: Logger = None) -> dict:
        exam_id = data.get("id") 
        
        # Step 1: fetch all exam details
        exam_details = db.query(ExamDetail).filter(ExamDetail.exam_id == exam_id).all() 
        if not exam_details:
            if logger:
                logger.warning("No exam details found")
            return {"info": [], "mastery": []}

        # Step 2: preload reference data
        kc_map = {k.id: k.title for k in db.query(KC).all()}   
        question_map = {q.id: q for q in db.query(Question).all()}
        option_map = {}
        for o in db.query(Option).all():
            option_map.setdefault(o.question_id, []).append(o)

        # Step 3: build output
        output = {"info": [], "mastery": []}  # mastery skipped for now
        for ed in exam_details:
            question = question_map.get(ed.question_id)
            if not question:
                continue

            options = option_map.get(ed.question_id, [])
            answer = next((o for o in options if o.id == ed.option_id), None)
            correct_option = next((o for o in options if o.order == question.correct_option), None)

            # information
            output["info"].append({
                "question_id":ed.question_id,
                "kc": kc_map.get(ed.kc_id),
                "question": question.title if question else None,
                "answer": answer.text if answer else None,
                "is_correct": ed.is_correct,
                "correct_answer": correct_option.text if correct_option else None
            })  
        
        output["mastery"] =BayesianUpdater.get_kc_masteries(exam_id, db, logger)  

        return output
        
    @staticmethod
    def get_mastery_report(data: dict, db: Session, logger: Logger = None):
        """
        Returns a report of user info with DAG/KC mastery.
        """
        sql = text("""
            SELECT 
                u.first_name,
                u.last_name,
                u.email,
                d.title AS dag_title,
                k.title AS kc_title,
                AVG(sed.calculated_mastery) AS avg_mastery
            FROM simulated_exam_data sed
            JOIN simulated_exam_data_raw sedr 
                ON sed.master_id = sedr.id
            JOIN users u 
                ON u.email = sedr.email
            JOIN dags d 
                ON sed.dag_id = d.id
            JOIN kcs k 
                ON sed.kc_id = k.id
            GROUP BY u.first_name, u.last_name, u.email, d.title, k.title
            ORDER BY u.email, d.title, k.title;
        """)

        result = db.execute(sql).mappings().all()  # use mappings() to get dict-like rows

        report_list = [
            {
                "name": f"{r['first_name']} {r['last_name']}",
                "email": r['email'],
                "dag": r['dag_title'],
                "kc": r['kc_title'],
                "mastery": float(r['avg_mastery'])  # convert to float for JSON safety
            }
            for r in result
        ]

        return report_list
    
    @staticmethod
    def get_question_options(data:dict, db: Session, logger: Logger = None) -> dict: 
        question_id = data.get("question_id")
        if not question_id:
            raise ValueError("Missing question_id in data")
        
         # Fetch question with its options
        result = (
            db.query(Question, Option)
            .join(Option, Option.question_id == Question.id)
            .filter(Question.id == question_id)
            .order_by(Option.order)
            .all()
        )

        if not result:
            if logger:
                logger.warning(f"No question found for ID {question_id}")
            return {}

        # First tuple contains the question
        question_obj = result[0][0]

        # Build output
        output = {
            "id": question_obj.id,
            "kc_id": question_obj.kc_id,
            "title": question_obj.title,
            "correct_option": question_obj.correct_option,
            "options": []
        }

        for _, opt in result:
            output["options"].append({
                "id": opt.id,
                "text": opt.text,
                "order": opt.order
            })

        return output 
    
    @staticmethod
    def get_next_question(data:dict,db: Session, logger: Logger) -> dict: 
        user_id, dag_id = itemgetter("user_id", "dag_id")(data) 
        kc_question_option_list=GetProcessors.get_kc_question_option_list(db, logger)
        selected_question=QuestionEngine.generate_next_question(kc_question_option_list, user_id,dag_id,db,logger)
        return selected_question
    
    @staticmethod
    @cached(kc_question_option_list_cache)
    def get_kc_question_option_list(db: Session, logger: Logger = None) -> list: 
        result = (
            db.query(KC, Question, Option)
            .join(Question, Question.kc_id == KC.id)
            .join(Option, Option.question_id == Question.id)
            .order_by(Question.title, Option.order)
            .all()
        )

        if not result:
            return []

        # Use a dict to group options by question
        questions_map = defaultdict(lambda: {
            "kc_id": None,
            "id": None,
            "title": None,
            "correct_option": None,
            "options": []
        })

        for kc_obj, question_obj, option_obj in result:
            qid = question_obj.id
            if questions_map[qid]["id"] is None:  # Initialize question info
                questions_map[qid]["kc_id"] = kc_obj.id
                questions_map[qid]["id"] = question_obj.id
                questions_map[qid]["title"] = question_obj.title
                questions_map[qid]["correct_option"] = question_obj.correct_option
            
            # Append option info
            questions_map[qid]["options"].append({
                "id": option_obj.id,
                "text": option_obj.text,
                "order": option_obj.order
            })

        # Convert dict values to list
        return list(questions_map.values())
    
    @staticmethod
    def check_student_data_validity(data: dict, db: Session, logger: Logger = None) -> list:
        ids, dag_id = itemgetter("ids", "dag_id")(data)

        # Fetch simulated student records
        items = (
            db.query(SimulatedStudentData)
            .filter(
                SimulatedStudentData.id.in_(ids),
                or_(
                    SimulatedStudentData.is_processed != 1,
                    SimulatedStudentData.is_processed.is_(None)
                )
            )
            .all()
        )

        # Pre-fetch existing users
        emails = [item.email for item in items]
        existing_users = {
            u.email: u for u in db.query(User).filter(User.email.in_(emails)).all()
        }

        # Prepare the validation result
        result = []

        # Pre-fetch profiles for this dag_id and user_ids that exist
        user_ids = [u.id for u in existing_users.values()]
        existing_profiles = {
            (p.user_id, p.dag_id) for p in db.query(Profile.user_id, Profile.dag_id)
            .filter(Profile.user_id.in_(user_ids), Profile.dag_id == dag_id)
            .all()
        }

        for item in items:
            entry = {"id": item.id}

            if item.email in existing_users:
                user = existing_users[item.email]
                entry["user"] = "Yes"
                entry["profile"] = "Yes" if (user.id, dag_id) in existing_profiles else "No"
            else:
                entry["user"] = "No"
                entry["profile"] = "No"

            result.append(entry)

        return result
    
    
    @staticmethod
    def check_exam_data_validity(data: List[Dict], db: Session, logger: Logger = None) -> List[Dict]:
        """
        Checks exam data validity against database records, adjusts metric outliers, and calculates mastery.
        """

        checked_data = []

        # Preload DB mappings for faster lookups
        result = (
            db.query(User.id, User.email, Profile.id.label("profile_id"))
            .outerjoin(Profile, Profile.user_id == User.id)
            .all()
        ) 
        email_map = {email: (user_id, profile_id) for user_id, email, profile_id in result} 
        
        dag_titles = {d.title for d in db.query(DAG).all()}
        kc_titles = {k.title for k in db.query(KC).all()}

        # Map questions by title for quick lookup
        questions_map = {q.title: q.id for q in db.query(Question).all()}
        
        # Map options by question_id for validation
        options_map = {}
        for opt in db.query(Option).all():
            options_map.setdefault(opt.question_id, []).append((opt.order, opt.text))

        for entry in data:
            email = entry["email"]

            # Check user & profile existence using email_map
            if email in email_map:
                user_exists = "Yes"
                profile_exists = "Yes" if email_map[email][1] is not None else "No"
            else:
                user_exists = "No"
                profile_exists = "No"

            # DAG, KC, and Question validation
            dag_exist = "Yes" if entry["dag_title"] in dag_titles else "No"
            kc_exist = "Yes" if entry["kc_title"] in kc_titles else "No"
            question_id = questions_map.get(entry["question"])
            question_exist = "Yes" if question_id else "No"

            # Option validation
            option_exist = "No"
            if question_id and question_id in options_map:
                if any(opt_text == entry["selected_option"] for _, opt_text in options_map[question_id]):
                    option_exist = "Yes"

            # Adjust outlier metric values (simple min-max clamping)
            def clamp(val, min_val, max_val):
                return max(min_val, min(val, max_val))

            time_taken = clamp(entry["time_taken"], 0, 120)  # max 2 minutes
            screen_weight = clamp(entry["screen_movement_weight"], 0, 1)
            expression_weight = clamp(entry["facial_expression_weight"], 0, 1)
            help_taken = clamp(entry["help_taken"], 0, 10)

            # Mastery calculation (simple formula: higher metrics = higher mastery)
            # You can tweak the formula based on your learning science approach
            mastery = round(
                (1 - (help_taken / 10)) * 
                (1 - expression_weight) * 
                (1 - screen_weight) * 
                (time_taken / 120), 2
            )

            checked_data.append({
                "id": entry["id"],
                "email": email,
                "profile_info": {
                    "user": user_exists,
                    "profile": profile_exists,
                },
                "kc_info": {
                    "dag_title": dag_exist,
                    "kc_title": kc_exist,
                    "question": question_exist,
                    "selected_option": option_exist
                },
                "metrics": {
                    "time_taken": time_taken,
                    "screen_movement_weight": screen_weight,
                    "facial_expression_weight": expression_weight,
                    "help_taken": help_taken
                },
                "mastery": mastery,
                "valid?": (
                    user_exists == "Yes" and
                    profile_exists == "Yes" and
                    dag_exist == "Yes" and
                    kc_exist == "Yes" and
                    question_exist == "Yes" and
                    option_exist == "Yes"
                )
            })

        if logger:
            logger.info(f"Checked {len(checked_data)} exam entries for validity.")

        return checked_data

    @staticmethod
    def get_dashboard_counter_info(data: List[Dict], db: Session, logger: Logger = None) -> dict:
        try:
            counters = {
                "dags": db.query(DAG).count(),
                "kcs": db.query(KC).count(),
                "students": db.query(SimulatedStudentData).count(),
                "exams": db.query(Exam).count(),
            }

            if logger:
                logger.info("Dashboard counters retrieved: %s", counters)

            return counters

        except Exception as e:
            if logger:
                logger.error("Error while retrieving dashboard counters: %s", e, exc_info=True)
            raise