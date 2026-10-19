from sqlalchemy import Column, String, Text, Numeric, CheckConstraint, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from db.base import Base

class Products(Base):
    __tablename__ = 'products'

    __table_args__ = (CheckConstraint("price > 0", name="check_price_positive"), CheckConstraint('stock_quantity >= 0', name="check_positive_stock_quantity"))

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    sku = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Numeric(12,2), nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_onupdate=func.now(), nullable=False)
