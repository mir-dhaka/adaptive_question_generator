import logging
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.schemas.auth_schemas import SettingCreate, SettingUpdate, SettingOut
from app.services.settings_service import SettingsService
from app.infra.response_handlers import BadRequestException, ResourceNotFoundException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/",
    summary="Create a new setting",
    response_model=SettingOut,
)
def create_setting(
    setting_data: SettingCreate = Body(...), db: Session = Depends(get_db)
):
    try:
        return SettingsService.create_setting(setting_data, db, logger)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{setting_id}",
    summary="Get a setting by ID",
    response_model=SettingOut,
)
def get_setting(
    setting_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    try:
        return SettingsService.get_setting(setting_id, db, logger)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{setting_id}",
    summary="Update a setting by ID",
    response_model=SettingOut,
)
def update_setting(
    setting_id: int = Path(..., gt=0),
    setting_data: SettingUpdate = Body(...),
    db: Session = Depends(get_db),
):
    try:
        return SettingsService.update_setting(setting_id, setting_data, db, logger)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{setting_id}",
    summary="Delete a setting by ID",
)
def delete_setting(
    setting_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    try:
        return SettingsService.delete_setting(setting_id, db, logger)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/",
    summary="List all settings",
)
def list_settings(db: Session = Depends(get_db)):
    return SettingsService.list_settings(db, logger)
