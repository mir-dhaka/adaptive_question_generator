from . import (
    auth_models,
    dag_models,
    question_models,
    student_models
)

# Build a registry manually
model_registry = {
    # auth models
    "users": auth_models.User,
    "settings": auth_models.Setting,

    # DAG models
    "dags": dag_models.DAG,
    "dag_edges": dag_models.DAGEdge,
    "kcs": dag_models.KC,
    "kc_topics": dag_models.KCTopic,

    # Question models
    "questions": question_models.Question,
    "options": question_models.Option,
    "exams": question_models.Exam,
    "exam_details": question_models.ExamDetail,    
    
    # Synthetic data models
    "simulated_student_data": question_models.SimulatedStudentData,
    "simulated_exam_data": question_models.SimulatedExamData,
    "simulated_exam_data_raw": question_models.SimulatedExamDataRaw,

    # Student / Exam models
    "profiles": student_models.Profile,
    "masteries": student_models.Mastery
}