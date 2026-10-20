from fastapi import Depends, HTTPException
from typing import Annotated
from uuid import UUID
from .helpers import decode_jwt_token
from starlette import status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.user import Users
from db.session import SessionLocal
from sqlalchemy.orm import Session

bearer_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependancy = Annotated[Session, Depends(get_db)]

def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)], db: db_dependancy) -> Users:
    token = credentials.credentials

    payload = decode_jwt_token(token)
    user_id = payload['sub']

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token payload', headers={"WWW-Authenticate": "Bearer"})

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user Id in token', headers={"WWW-Authenticate": "Bearer"})

    user = db.query(Users).filter(Users.id == user_uuid).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive User")
    return user

user_dependancy = Annotated[Users, Depends(get_current_user)]
