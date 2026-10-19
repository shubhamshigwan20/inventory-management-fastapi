from db.base import Base 
from sqlalchemy import Column, String, Enum, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from datetime import datetime, timezone

class UserRole(enum.Enum):
    ADMIN = 'admin'
    STAFF = 'staff'
    CUSTOMER = 'customer'


class Users(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable = False)
    role = Column(Enum(UserRole, name='user_role'),default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

