from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from schemas.auth import RegisterReq, LoginReq
from models.user import Users
from utils.helpers import hash_password, verify_password, create_jwt_token
from datetime import timedelta
from typing import Annotated
from utils.dependencies import user_dependancy, db_dependancy

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(req: RegisterReq, db: db_dependancy):
    print(f'Register Request: {req}')
    hashed_password = hash_password(req.password)
    # duplicate email error
    data = Users(full_name=req.full_name, email=req.email, password_hash=hashed_password)
    print(f"data: {data}")

    db.add(data)
    db.commit()
    
    response = {
        'id': data.id,
        'full_name': data.full_name,
        'email': data.email,
        'role': data.role,
        'is_active': data.is_active,
        'created_at': data.created_at
    }
    return response

@router.post('/login')
async def login_user(req: LoginReq, db:db_dependancy):
    print(f'Login Request: email={req.email}')
    data = db.query(Users).filter(Users.email == req.email).first()

    if data is None or not verify_password(req.password, data.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password',
        )

    # SQLAlchemy ORM instances do not provide to_dict(). Build a dictionary
    # from the mapped columns, excluding the password hash from logs.
    user_data = {
        column.name: getattr(data, column.name)
        for column in data.__table__.columns
        if column.name != 'password_hash'
    }
    print(f'db-data: {user_data}')

    # generate jwt token

    jwt_token = create_jwt_token(data.id)
    print(f'access token: {jwt_token}')

    return {
        'access_token': jwt_token,
        'token_type': 'bearer',
        'expires_in': timedelta(minutes=30)
    }

@router.get('/me')
async def get_me(current_user: user_dependancy):
    return {
        'id': current_user.id,
        'full_name': current_user.full_name,
        'email': current_user.email,
        'role': current_user.role,
        'is_active': current_user.is_active,
        'created_at': current_user.created_at
    }
