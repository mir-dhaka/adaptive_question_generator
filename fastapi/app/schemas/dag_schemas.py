from pydantic import BaseModel
from typing import List, Optional

class KCTopicBase(BaseModel):
    title: str
    summary: Optional[str] = None
    details: Optional[str] = None
    order: Optional[int] = None

class KCTopicOut(KCTopicBase):
    id: int
    kc_id: int

    class Config:
        orm_mode = True

class KCBase(BaseModel):
    title: str
    summary: Optional[str] = None

class KCOut(KCBase):
    id: int
    topics: List[KCTopicOut] = []

    class Config:
        orm_mode = True

class DAGEdgeBase(BaseModel):
    dag_id: int
    from_kc_id: int
    to_kc_id: int

class DAGEdgeOut(DAGEdgeBase):
    id: int
    # Optionally include nested KC info:
    from_kc: Optional[KCOut] = None
    to_kc: Optional[KCOut] = None

    class Config:
        orm_mode = True

class DAGBase(BaseModel):
    title: str
    summary: Optional[str] = None

class DAGOut(DAGBase):
    id: int
    edges: List[DAGEdgeOut] = []

    class Config:
        orm_mode = True
