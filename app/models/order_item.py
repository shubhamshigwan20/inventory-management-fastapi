from sqlalchemy import Column, String, ForeignKey, Uuid, Integer, CheckConstraint, Numeric, DateTime, func, UniqueConstraint
import uuid
from db.base import Base

class OrderItems(Base):
    __tablename__ = 'order_items'

    __table_args__ = (CheckConstraint('quantity >= 1', "check_quantity_positive"), CheckConstraint('unit_price > 0', 'check_positive_unit_price'), CheckConstraint('line_total >= 0', 'check_line_total_positive'), UniqueConstraint('order_id', 'product_id',name='unique_order_product_id'))

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Uuid, ForeignKey('orders.id', ondelete='RESTRICT'), nullable=False, index=True)
    product_id = Column(Uuid, ForeignKey('products.id', ondelete='RESTRICT'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12,2), nullable=False)
    line_total = Column(Numeric(12,2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
