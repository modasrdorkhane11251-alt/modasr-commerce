"""Wallet and ledger models."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, Numeric, String, DateTime, Text, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from app.db.base import Base


class Wallet(Base):
    """User wallet - account balance."""
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    
    # Balance - use NUMERIC for precision
    balance = Column(Numeric(18, 2), default=0, nullable=False)
    
    # Hold/reserved amount
    hold_amount = Column(Numeric(18, 2), default=0, nullable=False)
    
    # Available balance = balance - hold_amount
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="wallet")
    transactions = relationship("WalletTransaction", back_populates="wallet", cascade="all, delete-orphan")
    ledger_entries = relationship("LedgerTransaction", back_populates="wallet", cascade="all, delete-orphan")


class WalletTransaction(Base):
    """Wallet transaction - high-level transaction record."""
    __tablename__ = "wallet_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False, index=True)
    
    # Transaction type
    type = Column(String(50), nullable=False)  # deposit, withdrawal, purchase, refund, etc.
    
    # Amount
    amount = Column(Numeric(18, 2), nullable=False)
    balance_before = Column(Numeric(18, 2), nullable=False)
    balance_after = Column(Numeric(18, 2), nullable=False)
    
    # Description
    description = Column(Text, nullable=True)
    
    # Related entity
    related_type = Column(String(50), nullable=True)  # order, payment, refund, etc.
    related_id = Column(Integer, nullable=True)
    
    # Idempotency
    idempotency_key = Column(String(255), unique=True, nullable=True, index=True)
    
    # Status
    status = Column(String(50), default="completed", nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    wallet = relationship("Wallet", back_populates="transactions")
    
    __table_args__ = (
        Index('ix_wallet_transaction_created', 'wallet_id', 'created_at'),
    )


class LedgerTransaction(Base):
    """Ledger transaction - immutable audit trail for financials."""
    __tablename__ = "ledger_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False, index=True)
    
    # Entry type
    entry_type = Column(String(50), nullable=False)  # debit, credit
    
    # Amount
    amount = Column(Numeric(18, 2), nullable=False)
    
    # Account codes for accounting
    account_code = Column(String(50), nullable=True)
    
    # Description
    description = Column(Text, nullable=False)
    
    # Reference
    reference_type = Column(String(50), nullable=True)  # order, payment, etc.
    reference_id = Column(Integer, nullable=True)
    
    # Idempotency key - prevent duplicate entries
    idempotency_key = Column(String(255), unique=True, nullable=True, index=True)
    
    # Metadata
    metadata = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    wallet = relationship("Wallet", back_populates="ledger_entries")
    
    __table_args__ = (
        Index('ix_ledger_created', 'wallet_id', 'created_at'),
        Index('ix_ledger_reference', 'reference_type', 'reference_id'),
    )
