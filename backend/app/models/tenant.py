"""Tenant model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Tenant(Base):
    """Tenant model - represents a business/organization."""
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Branding
    logo_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)
    website_url = Column(String(500), nullable=True)
    
    # Telegram Bot
    telegram_bot_token = Column(String(500), nullable=False)  # Will be encrypted
    telegram_bot_username = Column(String(255), nullable=True, index=True)
    
    # Status
    status = Column(String(50), default="ACTIVE", nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    
    # Settings (JSON)
    settings = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    members = relationship("TenantMember", back_populates="tenant", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="tenant", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="tenant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="tenant", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="tenant", cascade="all, delete-orphan")
    providers = relationship("Provider", back_populates="tenant", cascade="all, delete-orphan")
    coupons = relationship("Coupon", back_populates="tenant", cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="tenant", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="tenant", cascade="all, delete-orphan")


class TenantMember(Base):
    """Tenant member - user role within a tenant."""
    __tablename__ = "tenant_members"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Role and permissions
    role = Column(String(50), nullable=False, index=True)  # TENANT_OWNER, TENANT_ADMIN, etc.
    permissions = Column(JSON, default=list)  # List of permission strings
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="members")
    user = relationship("User")
