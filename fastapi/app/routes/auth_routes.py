import logging
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.infra.response_handlers import InvalidCredentialsException, OkResponse, ResponseBuilder
from app.schemas.auth_schemas import Token, UserCreate, UserLogin, UserLogout
from app.services.auth_service import UserService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/register",
    summary="Register a new user",
    description="Adds a new user to the system"
)
def register(user_data: UserCreate = Body(...), db: Session = Depends(get_db)):
    """
    Registers a new user account and returns an authentication token.
    """
    return UserService.register_user(user_data, db, logger) 


@router.post(
    "/token",
    summary="Issue new token",
    description="Use username/email and password to get an access token"
)
def login(dto: UserLogin = Body(...), db: Session = Depends(get_db)):
    """
    Authenticates the user and returns an access token.
    """
    try:
        UserService.logout_user("", db, logger) 
        login_identifier = dto.user_name if dto.user_name else dto.email
        return UserService.login_user(login_identifier, dto.password, db, logger)  
    
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post(
    "/logout",
    summary="Logout user",
    description="Invalidate an access token to prevent further use"
)
def logout(dto: UserLogout = Body(...), db: Session = Depends(get_db)):
    """
    Logs the user out by invalidating their token.
    """
    try:
        return UserService.logout_user(dto.token, db, logger) 
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid credentials") 