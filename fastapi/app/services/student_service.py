import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.student_models import Profile, Mastery
from app.schemas.student_schemas import (
    ProfileCreate, ProfileUpdate, MasteryCreate, MasteryUpdate
)
from app.infra.response_handlers import (
    ResourceNotFoundException, OkResponse
)

logger = logging.getLogger(__name__)


class StudentService:

    # ------------------ Profile Methods ------------------
    @staticmethod
    def create_profile(profile_data: ProfileCreate, db: Session) -> Profile:
        logger.debug(f"Creating profile for user_id={profile_data.user_id}")

        profile = Profile(
            user_id=profile_data.user_id,
            is_active=profile_data.is_active,
            dag_id=profile_data.dag_id
        )

        # Add masteries if provided
        if profile_data.masteries:
            for m in profile_data.masteries:
                mastery = Mastery(**m.dict())
                profile.masteries.append(mastery)

        db.add(profile)
        db.commit()
        db.refresh(profile)

        logger.info(f"Profile created with id={profile.id}")
        return profile

    @staticmethod
    def get_profile(profile_id: int, db: Session) -> Profile:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            logger.warning(f"Profile not found: id={profile_id}")
            raise ResourceNotFoundException("Profile not found")
        return profile

    @staticmethod
    def update_profile(profile_id: int, profile_data: ProfileUpdate, db: Session) -> Profile:
        profile = StudentService.get_profile(profile_id, db)

        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(profile, field, value)

        db.commit()
        db.refresh(profile)
        logger.info(f"Profile updated: id={profile.id}")
        return profile

    @staticmethod
    def delete_profile(profile_id: int, db: Session) -> OkResponse:
        profile = StudentService.get_profile(profile_id, db)
        db.delete(profile)
        db.commit()
        logger.info(f"Profile deleted: id={profile.id}")
        return OkResponse(message="Profile deleted successfully")

    # ------------------ Mastery Methods ------------------
    @staticmethod
    def create_mastery(mastery_data: MasteryCreate, db: Session) -> Mastery:
        mastery = Mastery(**mastery_data.dict())
        db.add(mastery)
        db.commit()
        db.refresh(mastery)
        logger.info(f"Mastery created: id={mastery.id}")
        return mastery

    @staticmethod
    def update_mastery(mastery_id: int, mastery_data: MasteryUpdate, db: Session) -> Mastery:
        mastery = db.query(Mastery).filter(Mastery.id == mastery_id).first()
        if not mastery:
            logger.warning(f"Mastery not found: id={mastery_id}")
            raise ResourceNotFoundException("Mastery not found")

        for field, value in mastery_data.dict(exclude_unset=True).items():
            setattr(mastery, field, value)

        db.commit()
        db.refresh(mastery)
        logger.info(f"Mastery updated: id={mastery.id}")
        return mastery

    @staticmethod
    def delete_mastery(mastery_id: int, db: Session) -> OkResponse:
        mastery = db.query(Mastery).filter(Mastery.id == mastery_id).first()
        if not mastery:
            logger.warning(f"Mastery not found: id={mastery_id}")
            raise ResourceNotFoundException("Mastery not found")

        db.delete(mastery)
        db.commit()
        logger.info(f"Mastery deleted: id={mastery.id}")
        return OkResponse(message="Mastery deleted successfully")
