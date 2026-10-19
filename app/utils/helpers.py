import bcrypt
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone, timedelta
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / '.env')


SECRET_KEY = os.getenv('JWT_SECRET')
if not SECRET_KEY:
    raise RuntimeError(
        f'DB_URL is not configured.'
        'or in the process environment.'
    )

ALGORITHM = "HS256"



def hash_password(password:str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password:str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_jwt_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        'sub': str(user_id),
        'iat': now,
        'exp': now + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid Token')








