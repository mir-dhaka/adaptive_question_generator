from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from app.infra.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    kc_id = Column(Integer, ForeignKey("kcs.id"), nullable=False)
    title = Column(String, nullable=False)
    correct_option = Column(Integer, nullable=False)

   # kc = relationship("KC", back_populates="questions")
   # options = relationship("Option", back_populates="question", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    text = Column(String, nullable=False)
    order = Column(Integer)

  #  question = relationship("Question", back_populates="options")

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)  # this is actually profile_id
    exam_info = Column(String)  # json text

   # details = relationship("ExamDetail", back_populates="exam", cascade="all, delete-orphan")


class ExamDetail(Base):
    __tablename__ = "exam_details"

    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("options.id"), nullable=True)
    is_correct = Column(Boolean, nullable=False)
    next_suggested_question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    kc_id = Column(Integer, ForeignKey("kcs.id"), nullable=True)
    previous_mastery = Column(Float, nullable=True)
    current_mastery = Column(Float, nullable=True)

   # exam = relationship("Exam", back_populates="details")
   # question = relationship("Question", foreign_keys=[question_id])
   # option = relationship("Option", foreign_keys=[option_id])
   # next_suggested_question = relationship("Question", foreign_keys=[next_suggested_question_id])
   # kc = relationship("KC")

class SimulatedStudentData(Base):
    __tablename__ = "simulated_student_data"

    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # Store hashed passwords!
    is_processed= Column(Integer, nullable=True)

  #  simulated_exams = relationship("SimulatedExamData", back_populates="master")

class SimulatedExamDataRaw(Base):
    __tablename__ = "simulated_exam_data_raw"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    dag_title=Column(String, nullable=False)
    kc_title=Column(String, nullable=False)
    question = Column(String, nullable=False)
    selected_option = Column(String, nullable=False)
    time_taken = Column(Float, nullable=True)  # seconds or any unit
    help_taken = Column(Integer, nullable=True)  # e.g., number of helps requested
    screen_movement_weight = Column(Float, nullable=True)
    facial_expression_weight = Column(Float, nullable=True)
    is_processed= Column(Integer, nullable=True)
    
class SimulatedExamData(Base):
    __tablename__ = "simulated_exam_data"

    id = Column(Integer, primary_key=True)
    master_id = Column(Integer, ForeignKey("simulated_student_data.id"), nullable=False)
    dag_id = Column(Integer, ForeignKey("dags.id"), nullable=False)
    kc_id = Column(Integer, ForeignKey("kcs.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("options.id"), nullable=True)
    time_taken = Column(Float, nullable=True)  # seconds or any unit
    help_taken = Column(Integer, nullable=True)  # e.g., number of helps requested
    screen_movement_weight = Column(Float, nullable=True)
    facial_expression_weight = Column(Float, nullable=True)
    calculated_mastery= Column(Float, nullable=True)

   # master = relationship("SimulatedStudentData", back_populates="simulated_exams")
  #  question = relationship("Question")
   # selected_option = relationship("Option")

