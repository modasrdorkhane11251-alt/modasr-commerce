"""Order models."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric, DateTime, JSON, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from app.db.base import Base


class Order(Base):
    """Order model."""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Order info
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Pricing
    subtotal = Column(Numeric(18, 2), nullable=False)  # Before discount/tax
    discount_amount = Column(Numeric(18, 2), default=0)  # Coupon discount
    tax_amount = Column(Numeric(18, 2), default=0)
    total_amount = Column(Numeric(18, 2), nullable=False)  # Final amount
    
    # Status
    status = Column(String(50), default="PENDING", nullable=False, index=True)
    
    # Payment
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Fulfillment
    fulfillment_status = Column(String(50), default="PENDING", nullable=False)
    fulfilled_at = Column(DateTime, nullable=True)
    
    # Customer info
    customer_email = Column(String(255), nullable=True)
    customer_phone = Column(String(20), nullable=True)
    customer_notes = Column(Text, nullable=True)
    
    # Internal notes
    internal_notes = Column(Text, nullable=True)
    
    # Metadata
    metadata = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # Payment expiration
    
    # Relationships
    tenant = relationship("Tenant", back_populates="orders")
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order")
    
    __table_args__ = (
        Index('ix_order_tenant_status', 'tenant_id', 'status'),
        Index('ix_order_user_created', 'user_id', 'created_at'),
    )


class OrderItem(Base):
    """Order item - line item in an order."""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    # Product snapshot
    product_name = Column(String(255), nullable=False)
    product_type = Column(String(50), nullable=False)
    
    # Pricing
    unit_price = Column(Numeric(18, 2), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    subtotal = Column(Numeric(18, 2), nullable=False)
    
    # Fulfillment
    fulfillment_status = Column(String(50), default="PENDING", nullable=False)
    fulfilled_at = Column(DateTime, nullable=True)
    
    # Fulfillment data (keys, credentials, etc.)
    fulfillment_data = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
