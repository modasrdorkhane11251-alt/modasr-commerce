"""Provider/Integration models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Provider(Base):
    """Provider/Panel (e.g., VPN panel, SMM panel)."""
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    
    # Provider info
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # vpn_panel, smm_panel, api, etc.
    
    # Configuration
    config = Column(JSON, default=dict)  # API endpoint, etc. (not secrets)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    status = Column(String(50), default="ACTIVE", nullable=False)
    
    # Health
    last_health_check = Column(DateTime, nullable=True)
    is_healthy = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    
    # Statistics
    total_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="providers")
    credentials = relationship("ProviderCredential", back_populates="provider", cascade="all, delete-orphan")


class ProviderCredential(Base):
    """Provider credentials (encrypted)."""
    __tablename__ = "provider_credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False, index=True)
    
    # Credential
    label = Column(String(255), nullable=False)
    username = Column(String(255), nullable=True)  # Encrypted
    password = Column(String(255), nullable=True)  # Encrypted
    api_key = Column(String(255), nullable=True)  # Encrypted
    api_secret = Column(String(255), nullable=True)  # Encrypted
    token = Column(Text, nullable=True)  # Encrypted
    extra_data = Column(JSON, default=dict)  # Encrypted
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_default = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    provider = relationship("Provider", back_populates="credentials")
