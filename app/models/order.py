from sqlalchemy import Column, String, Uuid, ForeignKey, Enum, Numeric, CheckConstraint, DateTime, func, Index
from db.base import Base
import uuid
import enum

class OrderStatus(enum.Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class Orders(Base):
    __tablename__ = 'orders'

    __table_args__ = (CheckConstraint('total_amount >= 0', name="check_total_amount_positive"), Index("composite_index_user_id_created_at", 'user_id', 'created_at'))
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String(30), nullable=False, unique=True)
    user_id = Column(Uuid, ForeignKey('users.id'), nullable=False)
    status = Column(Enum(OrderStatus, name='order_status'), nullable=False, default=OrderStatus.PENDING, index=True)
    total_amount = Column(Numeric(12,2), nullable=False)
    notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_onupdate=func.now(), nullable=False)
