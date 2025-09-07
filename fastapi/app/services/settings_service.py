import logging
from logging import Logger
from sqlalchemy.orm import Session 
from app.models.auth_models import Setting
from app.schemas.auth_schemas import SettingCreate, SettingUpdate, SettingOut
from app.infra.response_handlers import OkResponse, BadRequestException, ResourceNotFoundException
 
class SettingsService:
    @staticmethod
    def create_setting(setting_data: SettingCreate, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Creating setting: type={setting_data.type}, group={setting_data.group}, key={setting_data.key}")

        # Optional: check for existing setting with same type/group/key to enforce uniqueness
        existing = db.query(Setting).filter(
            Setting.type == setting_data.type,
            Setting.group == setting_data.group,
            Setting.key == setting_data.key
        ).first()
        if existing:
            logger.warning("Setting already exists with this type/group/key")
            raise BadRequestException("Setting with this type/group/key already exists.")

        new_setting = Setting(
            type=setting_data.type,
            group=setting_data.group,
            key=setting_data.key,
            value=setting_data.value
        )
        db.add(new_setting)
        db.commit()
        db.refresh(new_setting)

        logger.info(f"Created setting with ID {new_setting.id}")
        return OkResponse(SettingOut.from_orm(new_setting))

    @staticmethod
    def get_setting(setting_id: int, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Fetching setting ID {setting_id}")

        setting = db.query(Setting).get(setting_id)
        if not setting:
            logger.warning(f"Setting ID {setting_id} not found")
            raise ResourceNotFoundException("Setting not found.")

        return OkResponse(SettingOut.from_orm(setting))

    @staticmethod
    def update_setting(setting_id: int, setting_data: SettingUpdate, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Updating setting ID {setting_id}")

        setting = db.query(Setting).get(setting_id)
        if not setting:
            logger.warning(f"Setting ID {setting_id} not found")
            raise ResourceNotFoundException("Setting not found.")

        for field, value in setting_data.dict(exclude_unset=True).items():
            setattr(setting, field, value)

        db.commit()
        db.refresh(setting)

        logger.info(f"Updated setting ID {setting_id}")
        return OkResponse(SettingOut.from_orm(setting))

    @staticmethod
    def delete_setting(setting_id: int, db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info(f"Deleting setting ID {setting_id}")

        setting = db.query(Setting).get(setting_id)
        if not setting:
            logger.warning(f"Setting ID {setting_id} not found")
            raise ResourceNotFoundException("Setting not found.")

        db.delete(setting)
        db.commit()

        logger.info(f"Deleted setting ID {setting_id}")
        return OkResponse(message=f"Setting ID {setting_id} deleted successfully.")

    @staticmethod
    def list_settings(db: Session, logger: Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__)
        logger.info("Listing all settings")

        settings = db.query(Setting).all()
        settings_out = [SettingOut.from_orm(s) for s in settings]

        return OkResponse({"settings": settings_out})