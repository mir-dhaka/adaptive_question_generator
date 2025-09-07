from sqlalchemy import Column, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.infra.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    dag_id = Column(Integer, ForeignKey("dags.id"), nullable=True)

   # user = relationship("User", backref="profiles")
  #  dag = relationship("DAG")
  #  masteries = relationship("Mastery", back_populates="profile", cascade="all, delete-orphan")

class Mastery(Base):
    __tablename__ = "masteries"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    dag_id=Column(Integer, ForeignKey("dags.id"), nullable=False)
    kc_id = Column(Integer, ForeignKey("kcs.id"), nullable=False)
    mastery = Column(Float, nullable=False)

  #  profile = relationship("Profile", back_populates="masteries")
  #  kc = relationship("KC")
