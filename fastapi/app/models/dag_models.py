from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.infra.database import Base

class KC(Base):
    __tablename__ = "kcs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(Text)

   # topics = relationship("KCTopic", back_populates="kc")
   # questions = relationship("kc", back_populates="kcs")


class KCTopic(Base):
    __tablename__ = "kc_topics"

    id = Column(Integer, primary_key=True)
    kc_id = Column(Integer, ForeignKey("kcs.id"), nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    details = Column(Text)
    order = Column(Integer)

   # kc = relationship("KC", back_populates="topics")


class DAG(Base):
    __tablename__ = "dags"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(Text)

  #  edges = relationship("DAGEdge", back_populates="dag", cascade="all, delete-orphan")


class DAGEdge(Base):
    __tablename__ = "dag_edges"

    id = Column(Integer, primary_key=True)
    dag_id = Column(Integer, ForeignKey("dags.id"), nullable=False)
    from_kc_id = Column(Integer, ForeignKey("kcs.id"), nullable=False)
    to_kc_id = Column(Integer, ForeignKey("kcs.id"), nullable=False)

  #  dag = relationship("DAG", back_populates="edges")
  #  from_kc = relationship("KC", foreign_keys=[from_kc_id])
   # to_kc = relationship("KC", foreign_keys=[to_kc_id])
