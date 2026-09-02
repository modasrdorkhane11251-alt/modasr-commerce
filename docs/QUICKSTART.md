# MODASR Commerce - Quick Start Guide

## Prerequisites

- Docker & Docker Compose
- Git
- 4GB RAM minimum
- 2 vCPU minimum

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/modasrdorkhane11251-alt/modasr-commerce.git
cd modasr-commerce
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set required values:
- `SECRET_KEY`: Generate strong random key
- `ENCRYPTION_KEY`: Base64-encoded 32-byte key
- `TELEGRAM_BOT_TOKEN_MAIN`: Your Telegram bot token
- Database credentials
- Payment gateway credentials

### 3. Start Services

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Initialize Database

```bash
docker-compose exec backend bash scripts/init-db.sh
```

### 5. Create Admin User

```bash
docker-compose exec backend python scripts/create_admin.py
```

### 6. Access Services

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **Admin**: http://localhost:3000/admin

## Management Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

### Database

```bash
# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback
docker-compose exec backend alembic downgrade -1
```

### Backup & Restore

```bash
# Backup
docker-compose exec backend bash scripts/backup.sh

# Restore
docker-compose exec backend bash scripts/restore.sh /backups/postgres/file.sql.gz
```

### Celery Tasks

```bash
# Monitor tasks
docker-compose exec celery_worker celery -A app.workers inspect active

# Purge queue
docker-compose exec celery_worker celery -A app.workers purge
```

## Production Deployment

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed production deployment guide.

## Troubleshooting

### Port Already in Use

```bash
# Change ports in docker-compose.yml or .env
export BACKEND_PORT=9000
export FRONTEND_PORT=3001
```

### Database Connection Failed

```bash
# Check if postgres is running
docker-compose logs postgres

# Recreate volumes
docker-compose down -v
docker-compose up -d
```

### Out of Memory

```bash
# Increase Docker memory limit
# Edit docker-compose.yml and add:
# services:
#   backend:
#     deploy:
#       resources:
#         limits:
#           memory: 2G
```

## Security Checklist

- [ ] Change admin password
- [ ] Update `SECRET_KEY`
- [ ] Update `ENCRYPTION_KEY`
- [ ] Configure payment gateways
- [ ] Setup SSL/TLS certificates
- [ ] Configure Cloudflare (optional)
- [ ] Enable CORS for your domains
- [ ] Setup backup schedule
- [ ] Configure email/SMTP
- [ ] Review audit logs

## Support

- Docs: https://github.com/modasrdorkhane11251-alt/modasr-commerce
- Issues: https://github.com/modasrdorkhane11251-alt/modasr-commerce/issues
- Email: support@modasr.top
