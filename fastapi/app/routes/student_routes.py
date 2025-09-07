import logging
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.infra.database import get_db
from app.schemas.student_schemas import (
    ProfileCreate, ProfileUpdate, MasteryCreate, MasteryUpdate
)
from app.schemas.student_schemas import (
    ProfileOut  # you might want to add MasteryOut if needed
)
from app.services.student_service import StudentService
from app.infra.response_handlers import ResourceNotFoundException, OkResponse

logger = logging.getLogger(__name__)
router = APIRouter()


# -------- Profile Routes --------
@router.post("/", summary="Create Profile", response_model=ProfileOut)
def create_profile(
    profile_data: ProfileCreate = Body(...),
    db: Session = Depends(get_db)
):
    profile = StudentService.create_profile(profile_data, db)
    return profile


@router.get("/{profile_id}", summary="Get Profile by ID", response_model=ProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    try:
        profile = StudentService.get_profile(profile_id, db)
        return profile
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{profile_id}", summary="Update Profile", response_model=ProfileOut)
def update_profile(
    profile_id: int,
    profile_data: ProfileUpdate = Body(...),
    db: Session = Depends(get_db)
):
    try:
        profile = StudentService.update_profile(profile_id, profile_data, db)
        return profile
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{profile_id}", summary="Delete Profile")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    try:
        return StudentService.delete_profile(profile_id, db)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


# -------- Mastery Routes --------
@router.post("/masteries", summary="Create Mastery")
def create_mastery(
    mastery_data: MasteryCreate = Body(...),
    db: Session = Depends(get_db)
):
    mastery = StudentService.create_mastery(mastery_data, db)
    return mastery


@router.put("/masteries/{mastery_id}", summary="Update Mastery")
def update_mastery(
    mastery_id: int,
    mastery_data: MasteryUpdate = Body(...),
    db: Session = Depends(get_db)
):
    try:
        mastery = StudentService.update_mastery(mastery_id, mastery_data, db)
        return mastery
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/masteries/{mastery_id}", summary="Delete Mastery")
def delete_mastery(mastery_id: int, db: Session = Depends(get_db)):
    try:
        return StudentService.delete_mastery(mastery_id, db)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
