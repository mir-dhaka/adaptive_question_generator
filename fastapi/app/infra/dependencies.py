from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .auth import decode_access_token
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class RoleChecker:
    def __init__(self, required_role: str = None, required_permission: str = None):
        self.required_role = required_role
        self.required_permission = required_permission

    def __call__(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_role = payload.get("role")
        user_permissions = payload.get("permissions", [])

        if self.required_role and user_role != self.required_role:
            raise HTTPException(status_code=403, detail="Insufficient role")

        if self.required_permission and self.required_permission not in user_permissions:
            raise HTTPException(status_code=403, detail="Insufficient permission")