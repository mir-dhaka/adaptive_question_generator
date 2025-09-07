import base64
from datetime import datetime
import json
import logging
from logging import Logger
from operator import itemgetter, or_
import random
from typing import Dict, List
from sqlalchemy.orm import Session
from app.infra.auth import get_password_hash
from app.models.auth_models import User
from app.models.dag_models import DAG, KC
from app.models.question_models import Exam, ExamDetail, Question, Option, SimulatedExamData, SimulatedExamDataRaw, SimulatedStudentData  # adjust to your actual file/module names
from app.models.student_models import Mastery, Profile
from app.schemas.question_schemas import QuestionCreate, QuestionUpdate, QuestionOut
from app.infra.response_handlers import OkResponse, BadRequestException, ResourceNotFoundException
from app.services.processors.bayesian_updater import BayesianUpdater
from app.services.processors.dag_util import DagUtil

class PostProcessors:
    @staticmethod
    def get_dag_url(data:dict, db: Session, logger: Logger = None) -> dict:  
        id=data['id']
        file_name=DagUtil.generate_dag_image(db, id)
        data= {"file_name":file_name} 
        return data
    
    @staticmethod
    def create_student_profiles(data:dict, db: Session, logger: Logger = None) -> dict:
        ids, dag_id = itemgetter("ids", "dag_id")(data)
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
        
        emails = [item.email for item in items]
        existing_users = {
            u.email: u for u in db.query(User).filter(User.email.in_(emails)).all()
        }

        try:
            for item in items:
                if item.email in existing_users:
                    user = existing_users[item.email]
                else:
                    hashed_password = get_password_hash(item.password)
                    user = User(
                        first_name=item.firstname,
                        last_name=item.lastname,
                        user_name=item.email,
                        email=item.email,
                        hashed_password=hashed_password,
                        role="student"
                    )
                    db.add(user)
                    db.flush()
                    existing_users[item.email] = user  # so later duplicates in same batch are handled

                db.add(Profile(user_id=user.id, dag_id=dag_id, is_active=True))
                item.is_processed = 1  # mark processed

            db.commit() 
        except Exception as e: 
            db.rollback() 
            if logger: 
                logger.error(f"Error creating student profiles: {e}") 
                raise 
        return {}
    
    @staticmethod
    def save_exam_details(data: dict, db: Session, logger: Logger = None) -> dict:
        try:
            exam_id,kc_id=itemgetter("exam_id", "kc_id")(data)
            exam=db.query(Exam).filter(Exam.id==exam_id).first() 
            profile_id=exam.student_id
            decoded_info = json.loads(base64.b64decode(exam.exam_info).decode("utf-8"))
            dag_id=decoded_info["dag_id"] 
            is_correct= data["is_correct"]
            
            previous_mastery=random.uniform(0.2, 0.6) # random
            current_mastery=BayesianUpdater.update_mastery(dag_id,kc_id,profile_id,previous_mastery, is_correct, db,logger)
            
            mastery=db.query(Mastery).filter(Mastery.profile_id==profile_id and Mastery.kc_id==kc_id and Mastery.dag_id==dag_id).first()
            if mastery:
                previous_mastery=mastery.mastery
                mastery.mastery=current_mastery
            else:
                mastery = Mastery(
                    profile_id=profile_id,
                    dag_id=dag_id,
                    kc_id=kc_id,
                    mastery=current_mastery
                )
                db.add(mastery)
            
            # Unpack dictionary directly (simpler than itemgetter for many keys)
            exam_detail = ExamDetail(
                kc_id=kc_id,
                exam_id=exam_id,
                question_id=data["question_id"],
                option_id=data["option_id"],
                is_correct=is_correct,
                previous_mastery=previous_mastery,
                current_mastery=current_mastery
            )

            db.add(exam_detail)
            db.commit()     # commit ensures ID is generated
            db.refresh(exam_detail)  # refresh ensures object has new ID from DB

            return exam_detail

        except Exception as e:
            db.rollback()
            if logger:
                logger.error(f"Failed to save exam details: {e}", exc_info=True)
            raise
    
    @staticmethod
    def finish_exam(data: Dict, db: Session, logger: Logger = None) -> dict:
        try:
            exam_id = data.get("id")
            if not exam_id:
                raise ValueError("Exam id is missing in request data")

            # fetch exam from DB
            exam = db.query(Exam).filter(Exam.id == exam_id).first()
            if not exam:
                raise ValueError(f"Exam with id {exam_id} not found")

            # decode base64 -> JSON
            decoded_info = json.loads(base64.b64decode(exam.exam_info).decode("utf-8"))

            # update finished
            decoded_info["finished"] = True
            decoded_info["finished_at"] = datetime.utcnow().isoformat()  # e.g. "2025-08-16T10:45:12.345678"


            # encode JSON -> base64
            updated_info_b64 = base64.b64encode(json.dumps(decoded_info).encode("utf-8")).decode("utf-8")

            # update record
            exam.exam_info = updated_info_b64
            db.add(exam)
            
            # TODO: in a report model store exam-result info and calculated kc-masteries for that dag for that student.
            
            
            db.commit()
            db.refresh(exam)

            if logger:
                logger.info(f"Exam {exam_id} marked as finished")

            return {}

        except Exception as e:
            if logger:
                logger.error(f"Error finishing exam: {str(e)}")
            raise
    
    @staticmethod
    def create_exam_profiles(data: List[Dict], db: Session, logger: Logger = None) -> List[Dict]:
        """
        Create users, profiles, and insert valid exam data into SimulatedExamData table.
        """
        created_entries = [] 
        
        # Preload items
        ids_to_process = [entry["id"] for entry in data]

        raw_entries = (
            db.query(SimulatedExamDataRaw)
            .filter(
                SimulatedExamDataRaw.id.in_(ids_to_process),
                SimulatedExamDataRaw.is_processed.is_(None)  # only NULL
            )
            .all()
        )

        # Preload DB mappings
        result = (
            db.query(User.id, User.email, Profile.id.label("profile_id"))
            .outerjoin(Profile, Profile.user_id == User.id)
            .all()
        )
        email_map = {email: (user_id, profile_id) for user_id, email, profile_id in result}

        dag_map = {d.title: d.id for d in db.query(DAG).all()}
        kc_map = {k.title: k.id for k in db.query(KC).all()}
        question_map = {q.title: q.id for q in db.query(Question).all()}

        # Map options for quick lookup by question_id
        options_map = {}
        for opt in db.query(Option).all():
            options_map.setdefault(opt.question_id, []).append((opt.id, opt.text))

        try:
        
            for entry in raw_entries:
                email = entry.email

                # --- USER & PROFILE CREATION ---
                if email in email_map:
                    user_id, profile_id = email_map[email]
                else:
                    # Create new user
                    # Hash the password
                    password_hash = get_password_hash("123456")
                    
                    # Create new user with first_name, last_name, user_name = email
                    new_user = User(
                        email=email,
                        hashed_password=password_hash,
                        first_name=email,
                        last_name=email,
                        user_name=email,
                        role="student"
                    )
                    db.add(new_user)
                    db.flush()  # flush to get new_user.id
                    user_id = new_user.id

                    # Create new profile
                    new_profile = Profile(user_id=user_id, is_active=True, dag_id=dag_map.get(entry.dag_title))
                    db.add(new_profile)
                    db.flush()
                    profile_id = new_profile.id

                    # Update email_map
                    email_map[email] = (user_id, profile_id)

                # --- VALIDATION ---
                dag_id = dag_map.get(entry.dag_title)
                kc_id = kc_map.get(entry.kc_title)
                question_id = question_map.get(entry.question)

                if not (dag_id and kc_id and question_id):
                    continue  # skip invalid entries 

                # Match selected option
                selected_option_id = None
                for opt_id, opt_text in options_map.get(question_id, []):
                    if opt_text == entry.selected_option:
                        selected_option_id = opt_id
                        break

                # Adjust metrics
                def clamp(val, min_val, max_val):
                    return max(min_val, min(val, max_val))

                time_taken = clamp(entry.time_taken, 0, 120)
                screen_weight = clamp(entry.screen_movement_weight, 0, 1)
                expression_weight = clamp(entry.facial_expression_weight, 0, 1)
                help_taken = clamp(entry.help_taken, 0, 10)

                # Mastery
                mastery = round(
                    (1 - (help_taken / 10)) *
                    (1 - expression_weight) *
                    (1 - screen_weight) *
                    (time_taken / 120), 2
                )

                # --- INSERT INTO SIMULATED_EXAM_DATA ---
                exam_entry = SimulatedExamData(
                    master_id=entry.id,
                    dag_id=dag_id,
                    kc_id=kc_id,
                    question_id=question_id,
                    selected_option_id=selected_option_id,
                    time_taken=time_taken,
                    help_taken=help_taken,
                    screen_movement_weight=screen_weight,
                    facial_expression_weight=expression_weight,
                    calculated_mastery=mastery
                )
                db.add(exam_entry)
                created_entries.append({
                    "email": email,
                    "user_id": user_id,
                    "profile_id": profile_id,
                    "dag_id": dag_id,
                    "kc_id": kc_id,
                    "question_id": question_id,
                    "selected_option_id": selected_option_id,
                    "mastery": mastery
                })
                
                # Make the original entry processed
                entry.is_processed=True 
                
            db.commit()
        
        except Exception as e: 
            db.rollback() 
            if logger: 
                logger.error(f"Error creating student profiles: {e}") 
            raise  

        return created_entries

    
        
