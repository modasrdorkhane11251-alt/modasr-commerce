"""Audit logging models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base


class AuditLog(Base):
    """Audit log for tracking sensitive operations."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Action
    action = Column(String(255), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False)  # user, product, order, payment, etc.
    resource_id = Column(Integer, nullable=False)
    
    # Change tracking
    changes_before = Column(JSON, default=dict)
    changes_after = Column(JSON, default=dict)
    
    # Request context
    request_id = Column(String(255), nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # Description
    description = Column(Text, nullable=True)
    
    # Status
    status = Column(String(50), default="SUCCESS", nullable=False)  # SUCCESS, FAILED
    error_message = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="audit_logs")
    user = relationship("User")
