from fastapi import FastAPI, HTTPException, APIRouter
import time
from models import user, product, order, order_item
from db.session import engine
from db.session import db_dependancy
from sqlalchemy import text
from routers import auth
from db.base import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/api/v1")
app.include_router(router)
router.include_router(auth.router)

@router.get('/health')
async def health_check(db: db_dependancy):
    result = db.execute(text("SELECT 1"))
    print(f"result: {result}")
    value = result.scalar_one()
    print(f"value: {value}")

    if value != 1: 
        raise HTTPException(status_code=503, detail='Service Unavailable')

    response =  {
        'service': 'backend',
        'timestamp': time.time(),
        'status': True,
        'database': True if value == 1 else False
    }
    return response

