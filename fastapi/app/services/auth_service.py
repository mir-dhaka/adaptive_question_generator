import logging
from logging import Logger
from sqlalchemy.orm import Session
from app.infra.auth import create_access_token, get_password_hash, verify_password 
from app.infra.response_handlers import InvalidCredentialsException, OkResponse
from app.models.auth_models import User
from app.schemas.auth_schemas import Token, UserCreate, UserLogin, UserLogout, UserOut 
from app.infra.response_handlers import OkResponse, BadRequestException


class UserService:
    @staticmethod
    def register_user(user_data: UserCreate, db: Session, logger:Logger = None) -> dict:
        logger = logger or logging.getLogger(__name__) 
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            user_name=user_data.user_name,
            email=user_data.email,
            hashed_password=hashed_password,
            role=user_data.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access_token = create_access_token({"sub": new_user.id, "role": new_user.role}) 
        data= {"status":200, "success":True, "message":"User registered successfully", 
               "data":{"access_token": access_token, "token_type": "bearer", "user_data": new_user.email}
        }
        return data
    
    @staticmethod
    def login_user(username: str, password: str, db: Session, logger:Logger = None): 
        logger = logger or logging.getLogger(__name__) 
        logger.info(f"Login attempt for user: {username}")
        user = db.query(User).filter(User.user_name == username).first()

        if not user or not verify_password(password, user.hashed_password):
            logger.info(f"Login attempt failed for user: {username}")
            raise InvalidCredentialsException()

        access_token = create_access_token({"sub": user.id, "role": user.role})
         
        data= {"status":200, "success":True, "message":"User loggedin successfully", 
               "data":{"token": access_token, "token_type": "bearer", "user_data":UserOut.from_orm(user).dict()}
            }
        return data 
    
    @staticmethod
    def logout_user(token: str, db: Session, logger: Logger = None) -> dict:
        """
        Logout user by blacklisting the provided token (if using stateful auth).
        For stateless JWT, the client should just delete the token locally.
        """
        logger = logger or logging.getLogger(__name__)
        logger.info("User logout requested")

        # If using a token blacklist table:
        # revoked_token = RevokedToken(token=token)
        # db.add(revoked_token)
        # db.commit()

        # For stateless JWT, just return success
        data= {"status":200, "success":True, "message":"User logged out successfully", 
               "data":{}
            }
        return data