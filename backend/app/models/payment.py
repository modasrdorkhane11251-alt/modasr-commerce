"""Payment models."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric, DateTime, JSON, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from app.db.base import Base


class PaymentMethod(Base):
    """Payment method (gateway configuration)."""
    __tablename__ = "payment_methods"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Method info
    name = Column(String(255), nullable=False)
    provider = Column(String(50), nullable=False)  # zarinpal, pasargad, iranpay, etc.
    code = Column(String(50), nullable=False)  # For internal reference
    
    # Credentials (encrypted)
    credentials = Column(JSON, nullable=False)  # Will be encrypted
    
    # Configuration
    is_active = Column(Boolean, default=True, index=True)
    is_test_mode = Column(Boolean, default=False)
    
    # Display
    icon_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    
    # Fee
    fee_percentage = Column(Numeric(5, 2), default=0)  # Percentage fee
    fee_fixed = Column(Numeric(18, 2), default=0)  # Fixed fee
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant")
    payments = relationship("Payment", back_populates="payment_method")


class Payment(Base):
    """Payment record."""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=False)
    
    # Payment info
    transaction_id = Column(String(255), unique=True, nullable=True, index=True)  # Gateway transaction ID
    
    # Amount
    amount = Column(Numeric(18, 2), nullable=False)
    fee_amount = Column(Numeric(18, 2), default=0)
    net_amount = Column(Numeric(18, 2), nullable=False)  # amount - fee
    
    # Status
    status = Column(String(50), default="pending", nullable=False, index=True)
    
    # Gateway response
    gateway_response = Column(JSON, default=dict)  # Store full gateway response
    
    # Verification
    verified_at = Column(DateTime, nullable=True)
    verification_data = Column(JSON, default=dict)
    
    # Idempotency
    idempotency_key = Column(String(255), unique=True, nullable=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="payments")
    order = relationship("Order", back_populates="payment")
    payment_method = relationship("PaymentMethod", back_populates="payments")
    
    __table_args__ = (
        Index('ix_payment_tenant_status', 'tenant_id', 'status'),
        Index('ix_payment_order', 'order_id'),
    )
