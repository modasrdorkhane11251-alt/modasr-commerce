"""Coupon models."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.db.base import Base


class Coupon(Base):
    """Coupon/Discount code."""
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Code
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Discount type
    discount_type = Column(String(50), nullable=False)  # percentage, fixed
    discount_value = Column(Numeric(18, 2), nullable=False)
    
    # Limits
    max_discount = Column(Numeric(18, 2), nullable=True)
    min_order_amount = Column(Numeric(18, 2), nullable=True)
    
    # Usage limits
    max_uses = Column(Integer, nullable=True)  # NULL = unlimited
    max_uses_per_user = Column(Integer, default=1)
    times_used = Column(Integer, default=0)
    
    # Restrictions
    applicable_products = Column(JSON, default=list)  # Empty = all products
    applicable_categories = Column(JSON, default=list)  # Empty = all categories
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Dates
    valid_from = Column(DateTime, nullable=True)
    valid_until = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="coupons")
    redemptions = relationship("CouponRedemption", back_populates="coupon", cascade="all, delete-orphan")


class CouponRedemption(Base):
    """Coupon redemption record."""
    __tablename__ = "coupon_redemptions"
    
    id = Column(Integer, primary_key=True, index=True)
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Related order
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    
    # Discount applied
    discount_amount = Column(Numeric(18, 2), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    coupon = relationship("Coupon", back_populates="redemptions")
    user = relationship("User")
    order = relationship("Order")
