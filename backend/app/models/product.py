"""Product models."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.base import Base


class Category(Base):
    """Product category."""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    icon_url = Column(String(500), nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Display
    order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="categories")
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_category_tenant_slug', 'tenant_id', 'slug', unique=True),
    )


class Product(Base):
    """Product model."""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    
    # Basic info
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Type
    type = Column(String(50), nullable=False)  # DIGITAL_PRODUCT, SERVICE, SUBSCRIPTION, etc.
    
    # Pricing - Using NUMERIC for precision
    base_price = Column(Numeric(18, 2), nullable=False)  # Price in IRT
    min_price = Column(Numeric(18, 2), nullable=True)
    max_price = Column(Numeric(18, 2), nullable=True)
    
    # Inventory
    quantity_total = Column(Integer, nullable=True)  # NULL for unlimited
    quantity_sold = Column(Integer, default=0)
    is_unlimited = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False)
    
    # Images
    thumbnail_url = Column(String(500), nullable=True)
    images = Column(JSON, default=list)  # List of image URLs
    
    # Metadata
    attributes = Column(JSON, default=dict)  # Custom attributes
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="products")
    category = relationship("Category", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product")
    
    __table_args__ = (
        Index('ix_product_tenant_slug', 'tenant_id', 'slug', unique=True),
    )


class ProductVariant(Base):
    """Product variant - for options like color, size, etc."""
    __tablename__ = "product_variants"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    # Variant info
    name = Column(String(255), nullable=False)
    sku = Column(String(255), nullable=True, unique=True, index=True)
    
    # Pricing override
    price = Column(Numeric(18, 2), nullable=True)  # NULL means use product price
    
    # Inventory
    quantity = Column(Integer, nullable=True)
    
    # Attributes (color, size, etc.)
    attributes = Column(JSON, default=dict)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="variants")
