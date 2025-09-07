from pydantic import BaseModel
from typing import List, Optional

# ----- Option Schemas -----
class OptionBase(BaseModel):
    text: str
    order: Optional[int] = None

class OptionCreate(OptionBase):
    pass

class OptionOut(OptionBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True


# ----- Question Schemas -----
class QuestionBase(BaseModel):
    kc_id: int
    title: str
    correct_option: int  # Option ID or order (depends on your usage)

class QuestionCreate(QuestionBase):
    options: List[OptionCreate]

class QuestionUpdate(BaseModel):
    kc_id: Optional[int] = None
    title: Optional[str] = None
    correct_option: Optional[int] = None

class QuestionOut(QuestionBase):
    id: int
    options: List[OptionOut] = []

    class Config:
        orm_mode = True


# ----- ExamDetail Schemas -----
class ExamDetailBase(BaseModel):
    exam_id: int
    question_id: int
    option_id: Optional[int] = None
    is_correct: bool
    next_suggested_question_id: Optional[int] = None
    kc_id: Optional[int] = None
    previous_mastery: Optional[float] = None
    current_mastery: Optional[float] = None

class ExamDetailCreate(ExamDetailBase):
    pass

class ExamDetailOut(ExamDetailBase):
    id: int

    class Config:
        orm_mode = True


# ----- Exam Schemas -----
class ExamBase(BaseModel):
    student_id: int
    exam_info: Optional[str] = None

class ExamCreate(ExamBase):
    details: List[ExamDetailCreate]

class ExamOut(ExamBase):
    id: int
    details: List[ExamDetailOut] = []

    class Config:
        orm_mode = True


# ----- SimulatedStudentData Schemas -----
class SimulatedStudentDataBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str  # For creation only; never return password in responses!

class SimulatedStudentDataCreate(SimulatedStudentDataBase):
    pass

class SimulatedStudentDataOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str

    class Config:
        orm_mode = True


# ----- SimulatedExamData Schemas -----
class SimulatedExamDataBase(BaseModel):
    master_id: int
    question_id: int
    selected_option_id: Optional[int] = None
    time_taken: Optional[float] = None
    help_taken: Optional[int] = None
    screen_movement_weight: Optional[float] = None
    facial_expression_weight: Optional[float] = None
    calculated_mastery: Optional[float] = None

class SimulatedExamDataCreate(SimulatedExamDataBase):
    pass

class SimulatedExamDataOut(SimulatedExamDataBase):
    id: int

    class Config:
        orm_mode = True
