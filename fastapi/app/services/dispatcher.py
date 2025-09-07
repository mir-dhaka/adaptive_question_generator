import logging
from logging import Logger
from sqlalchemy.orm import Session

from app.services.processors.get_processors import GetProcessors
from app.services.processors.post_processors import PostProcessors


class Dispatcher:
    @staticmethod
    def dispatch(data:dict, slug:str, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Processing data: slug={slug}") 

        match slug:
            case "get-question-options":
                return GetProcessors.get_question_options(data, db, logger)
            case "get-dag-url":
                return PostProcessors.get_dag_url(data, db, logger) 
            case "check-student-data-validity":
                return GetProcessors.check_student_data_validity(data, db, logger) 
            case "create-student-profiles":
                return PostProcessors.create_student_profiles(data, db, logger)  
            case "check-exam-data-validity":
                return GetProcessors.check_exam_data_validity(data, db, logger) 
            case "create-exam-profiles":
                return PostProcessors.create_exam_profiles(data, db, logger) 
            case "save-exam-details":
                return PostProcessors.save_exam_details(data, db, logger) 
            case "finish-exam":
                return PostProcessors.finish_exam(data, db, logger) 
            case "get-mastery-report":
                return GetProcessors.get_mastery_report(data, db, logger)
            case "get-student-dag-info":
                return GetProcessors.get_student_dag_info(data, db, logger)   
            case "get-exam-info":
                return GetProcessors.get_exam_info(data, db, logger)   
            case "get-exam-detail-info":
                return GetProcessors.get_exam_detail_info(data, db, logger) 
            case "get-next-question":
                return GetProcessors.get_next_question(data, db, logger) 
            
            # dashboard
            case "get-dashboard-counter-info":
                return GetProcessors.get_dashboard_counter_info(data, db, logger)
            case _:                
                raise Exception(f"Failed to process with slug: {slug}")  
            
