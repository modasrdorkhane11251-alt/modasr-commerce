# MODASR Commerce - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                            │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│   │   Web UI     │  │ Telegram Bot │  │ Mini App     │    │
│   │  (Next.js)   │  │  (aiogram)   │  │  (TMA)       │    │
│   └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (Nginx)                      │
│         Load Balancing, SSL/TLS, Rate Limiting             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │           FastAPI Application                       │  │
│  │                                                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │  │
│  │  │   API    │  │ Telegram │  │  Middleware      │ │  │
│  │  │ Handlers │  │   Bot    │  │  - Auth          │ │  │
│  │  │          │  │  Handler │  │  - RBAC          │ │  │
│  │  └──────────┘  └──────────┘  │  - Error Handler │ │  │
│  │                              │  - Logging       │ │  │
│  │  ┌──────────────────────────┼──────────────────┤ │  │
│  │  │    Service Layer                            │ │  │
│  │  │  - Orders                                   │ │  │
│  │  │  - Products                                 │ │  │
│  │  │  - Payments                                 │ │  │
│  │  │  - Wallet/Ledger                            │ │  │
│  │  │  - Fulfillment                              │ │  │
│  │  │  - Providers                                │ │  │
│  │  └───────���──────────────────────────────────────┤ │  │
│  │                                                 │ │  │
│  │  ┌──────────────────────────────────────────────┤ │  │
│  │  │    Repository/Data Layer                     │ │  │
│  │  │  - SQLAlchemy ORM                            │ │  │
│  │  │  - Database Queries                          │ │  │
│  │  │  - Caching                                   │ │  │
│  │  └──────────────────────────────────────────────┤ │  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
└─────────────────────────────────────────────────────────┘
         ↓               ↓               ↓
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │PostgreSQL│   │  Redis  │    │ External │
    │Database  │   │  Cache  │    │ Services │
    └─────────┘     └─────────┘     └─────────┘
                          ↓
                   ┌──────────────┐
                   │ Celery Worker│
                   │ Background   │
                   │ Jobs Queue   │
                   └──────────────┘
```

## Multi-Tenancy Architecture

### Data Isolation

Every table has a `tenant_id` foreign key:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id),
    email VARCHAR(255) NOT NULL,
    UNIQUE(tenant_id, email)  -- Unique per tenant
);
```

### Query Isolation

All queries filtered by current tenant:

```python
# Repository layer
async def get_user(db: AsyncSession, user_id: int, tenant_id: int):
    return await db.execute(
        select(User).where(
            (User.id == user_id) & (User.tenant_id == tenant_id)
        )
    )
```

### Middleware Tenant Context

```python
# Middleware sets tenant context from JWT token
@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    # Extract tenant from token
    tenant_id = get_tenant_from_token(request)
    request.state.tenant_id = tenant_id
    return await call_next(request)
```

## Financial System Architecture

### Ledger-Based Accounting

```
User Wallet
├── Balance: 10,000 IRT
├── Hold Amount: 2,000 IRT
└── Available: 8,000 IRT

Ledger Entries (Immutable):
1. Deposit: +5,000 IRT (2024-01-01 10:00)
2. Purchase: -3,000 IRT (2024-01-01 10:30)
3. Refund: +3,000 IRT (2024-01-01 11:00)
...
```

### Transaction Flow

```
1. Order Created
   ├── Status: PENDING
   ├── Wallet: No change
   └── Ledger: No entry

2. Payment Initiated
   ├── Status: AWAITING_PAYMENT
   ├── Wallet: Hold amount locked
   └── Ledger: No entry (pending)

3. Payment Verified
   ├── Status: PAID
   ├── Wallet: Amount deducted
   └── Ledger: Debit entry created (idempotent key)

4. Order Fulfilled
   ├── Status: COMPLETED
   ├── Wallet: No change
   └── Ledger: No change
```

### Idempotency

Every transaction has an `idempotency_key` (UUID):

```python
# Client generates UUID
idempotency_key = str(uuid.uuid4())

# Server stores and checks
if LedgerTransaction.query.filter_by(
    idempotency_key=idempotency_key
).first():
    # Already processed, return cached result
    return cached_response

# Process new transaction
ledger_entry = LedgerTransaction(
    idempotency_key=idempotency_key,
    ...
)
```

## Authentication & Authorization

### JWT Token Flow

```
1. Login
   ├── Email + Password → Server
   └── Verify credentials

2. Generate Tokens
   ├── Access Token (30 min expiry)
   │  └── Contains: user_id, tenant_id, roles
   └── Refresh Token (7 day expiry)
      └── Contains: user_id

3. API Request
   ├── Header: Authorization: Bearer <access_token>
   └── Middleware: Verify & extract claims

4. Token Refresh
   ├── Send: Refresh Token
   └── Return: New Access + Refresh Tokens

5. Logout
   └── Revoke: Tokens in Redis blacklist
```

### Role-Based Access Control

```
Roles:
├── SUPER_ADMIN (Platform)
├── TENANT_OWNER (Business owner)
├── TENANT_ADMIN (Manager)
├── MANAGER (Staff)
├── SUPPORT (Support team)
├── FINANCE (Accounting)
├── PRODUCT_MANAGER (Product team)
├── RESELLER (Reseller account)
└── CUSTOMER (End user)

Permissions (granular):
├── tenant:create, tenant:read, tenant:update, tenant:delete
├── product:create, product:read, product:update, product:delete
├── order:create, order:read, order:cancel, order:refund
├── wallet:read, wallet:adjust
├── user:create, user:read, user:delete, user:block
└── ...

Policy Evaluation:
1. Get user roles for tenant
2. Collect all permissions from roles
3. Check if required permission present
4. Enforce at API endpoint (400+ errors)
```

## Payment Processing Architecture

### Provider Abstraction

```python
class PaymentProvider(ABC):
    @abstractmethod
    async def create_payment(self, amount, order_id, ...):
        pass
    
    @abstractmethod
    async def verify_payment(self, transaction_id):
        pass
    
    @abstractmethod
    async def refund_payment(self, transaction_id, amount):
        pass
    
    @abstractmethod
    async def handle_webhook(self, payload):
        pass

class ZarinpalProvider(PaymentProvider):
    # Zarinpal-specific implementation
    pass

class PassargadProvider(PaymentProvider):
    # Pasargad-specific implementation
    pass
```

### Payment State Machine

```
PENDING
  ↓
PROCESSING (awaiting gateway response)
  ↓
├─→ COMPLETED (successful)
│    └→ Order fulfilled
│
├─→ FAILED (gateway rejected)
│    └→ Wallet refunded
│
├─→ CANCELLED (user cancelled)
│    └→ Wallet refunded
│
└─→ EXPIRED (timeout)
     └→ Wallet refunded
```

## Telegram Bot Architecture

### Per-Tenant Bot Instance

Each tenant has isolated bot:

```
Webhook Handler
  ↓
┌──────────────────────────────┐
│ Message Router               │
│ - Extract tenant from chat   │
│ - Route to tenant handler    │
└──────────────────────────────┘
  ↓
Tenant-Specific Handler
  ├─ Commands: /start, /products, /orders
  ├─ Callbacks: Buy, View details
  ├─ Inline Keyboards: Navigation
  └─ Session State: Shopping cart
  ↓
API Calls (Authenticated)
  ├─ Fetch products
  ├─ Create orders
  ├─ Process payments
  └─ Send notifications
```

## Caching Strategy

```
Redis Cache Layers:
├── Session Cache
│   ├─ User sessions (30 min TTL)
│   └─ Telegram session state
│
├── Data Cache
│   ├─ Products (1 hour TTL)
│   ├─ Categories (1 hour TTL)
│   ├─ User wallet (5 min TTL)
│   └─ Prices (15 min TTL)
│
├── Lock Cache
│   ├─ Order processing locks (30 sec)
│   └─ Payment idempotency locks (10 min)
│
└── Rate Limit Cache
    ├─ API request counts (1 min window)
    └─ Login attempts (15 min window)
```

## Deployment Architecture

```
Cloudflare (Optional)
  ├─ DDoS Protection
  ├─ DNS
  └─ SSL/TLS
      ↓
Nginx (Reverse Proxy)
  ├─ Load Balancing
  ├─ Rate Limiting
  ├─ SSL/TLS Termination
  └─ Static Asset Caching
      ↓
┌─────────────────────────────────────────┐
│       Application Layer                 │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  FastAPI Backend (Scaled)        │  │
│  │  - Multiple instances via PM2    │  │
│  │  - Auto-restart on crash         │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Next.js Frontend                │  │
│  │  - Static generation             │  │
│  │  - ISR (Incremental)             │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
    ↓        ↓        ↓        ↓
┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
│PostgreSQL│Redis   │ Celery  │ Monitoring
│Cluster  │ Cluster │ Workers │ (Prometheus)
└────────┘ └────────┘ └────────┘ └──────────┘
```

---

For more details, see source code and API documentation.
