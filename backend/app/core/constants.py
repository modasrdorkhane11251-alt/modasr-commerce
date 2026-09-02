"""Application constants."""

# User roles
class UserRole:
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    TENANT_OWNER = "TENANT_OWNER"
    TENANT_ADMIN = "TENANT_ADMIN"
    MANAGER = "MANAGER"
    SUPPORT = "SUPPORT"
    FINANCE = "FINANCE"
    PRODUCT_MANAGER = "PRODUCT_MANAGER"
    RESELLER = "RESELLER"
    CUSTOMER = "CUSTOMER"


# Permissions
class Permission:
    # Tenant management
    TENANT_CREATE = "tenant:create"
    TENANT_READ = "tenant:read"
    TENANT_UPDATE = "tenant:update"
    TENANT_DELETE = "tenant:delete"
    
    # Product management
    PRODUCT_CREATE = "product:create"
    PRODUCT_READ = "product:read"
    PRODUCT_UPDATE = "product:update"
    PRODUCT_DELETE = "product:delete"
    
    # Order management
    ORDER_CREATE = "order:create"
    ORDER_READ = "order:read"
    ORDER_UPDATE = "order:update"
    ORDER_CANCEL = "order:cancel"
    ORDER_REFUND = "order:refund"
    
    # Wallet/Finance
    WALLET_READ = "wallet:read"
    WALLET_ADJUST = "wallet:adjust"
    WALLET_WITHDRAW = "wallet:withdraw"
    
    # User management
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_BLOCK = "user:block"
    
    # Provider management
    PROVIDER_CREATE = "provider:create"
    PROVIDER_READ = "provider:read"
    PROVIDER_UPDATE = "provider:update"
    PROVIDER_DELETE = "provider:delete"
    
    # Analytics
    ANALYTICS_READ = "analytics:read"
    
    # Settings
    SETTINGS_UPDATE = "settings:update"


# Order statuses
class OrderStatus:
    PENDING = "PENDING"
    AWAITING_PAYMENT = "AWAITING_PAYMENT"
    PAID = "PAID"
    PROCESSING = "PROCESSING"
    FULFILLING = "FULFILLING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"


# Product types
class ProductType:
    DIGITAL_PRODUCT = "DIGITAL_PRODUCT"
    SERVICE = "SERVICE"
    SUBSCRIPTION = "SUBSCRIPTION"
    API_PRODUCT = "API_PRODUCT"
    MANUAL_PRODUCT = "MANUAL_PRODUCT"
    STOCK_PRODUCT = "STOCK_PRODUCT"
    CONFIGURATION_PRODUCT = "CONFIGURATION_PRODUCT"


# Payment status
class PaymentStatus:
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"


# Ticket status
class TicketStatus:
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_USER = "WAITING_USER"
    WAITING_ADMIN = "WAITING_ADMIN"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


# Tenant status
class TenantStatus:
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    INACTIVE = "INACTIVE"
    TRIAL = "TRIAL"


# Currency
class Currency:
    IRT = "IRT"  # Iranian Toman
    USD = "USD"
    EUR = "EUR"


# Language
class Language:
    FA = "fa"
    EN = "en"
