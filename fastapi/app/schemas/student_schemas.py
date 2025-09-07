from pydantic import BaseModel
from typing import List, Optional

# ----- Mastery Schemas -----
class MasteryBase(BaseModel):
    profile_id: int
    kc_id: int
    mastery: float

class MasteryCreate(MasteryBase):
    pass

class MasteryUpdate(BaseModel):
    profile_id: Optional[int] = None
    kc_id: Optional[int] = None
    mastery: Optional[float] = None

class MasteryOut(MasteryBase):
    id: int

    class Config:
        orm_mode = True


# ----- Profile Schemas -----
class ProfileBase(BaseModel):
    user_id: int
    is_active: Optional[bool] = True
    dag_id: Optional[int] = None

class ProfileCreate(ProfileBase):
    masteries: Optional[List[MasteryCreate]] = []

class ProfileUpdate(BaseModel):
    user_id: Optional[int] = None
    is_active: Optional[bool] = None
    dag_id: Optional[int] = None

class ProfileOut(ProfileBase):
    id: int
    masteries: List[MasteryOut] = []

    class Config:
        orm_mode = True
