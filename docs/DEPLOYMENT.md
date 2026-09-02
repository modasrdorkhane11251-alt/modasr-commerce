# MODASR Commerce - Deployment Guide

## Production Environment Setup

### Prerequisites

- Ubuntu 24.04 LTS or similar Linux distribution
- 4GB+ RAM
- 40GB+ SSD storage
- Docker & Docker Compose installed
- Domain name pointing to server
- Telegram Bot Token

### Step 1: Server Preparation

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y \
    curl \
    wget \
    git \
    docker.io \
    docker-compose \
    ufw \
    fail2ban

# Create application user
sudo useradd -m -s /bin/bash modasr
sudo usermod -aG docker modasr

# Create data directories
sudo mkdir -p /data/modasr/{postgres,redis,backups}
sudo chown -R modasr:modasr /data/modasr
```

### Step 2: Clone and Configure

```bash
cd /home/modasr
git clone https://github.com/modasrdorkhane11251-alt/modasr-commerce.git
cd modasr-commerce

# Generate strong credentials
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32)}')" > .env
echo "ENCRYPTION_KEY=$(python3 -c 'import secrets; import base64; print(base64.b64encode(secrets.token_bytes(32)).decode())}')" >> .env

# Copy production template
cat .env.example | grep -v "^#" | grep -v "^$" >> .env

# Edit with real values
sudo -u modasr nano .env
```

### Step 3: SSL/TLS Setup

```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Generate certificate (for each domain)
sudo certbot certonly --standalone \
    -d hosting.modasr.top \
    -d api.hosting.modasr.top \
    -d admin.hosting.modasr.top \
    --non-interactive \
    --agree-tos \
    -m admin@modasr.top

# Copy certificates
sudo cp /etc/letsencrypt/live/hosting.modasr.top/fullchain.pem ./nginx/certs/cert.pem
sudo cp /etc/letsencrypt/live/hosting.modasr.top/privkey.pem ./nginx/certs/key.pem
sudo chown modasr:modasr ./nginx/certs/*

# Update nginx.conf with real certificate paths
# (uncomment SSL lines and update paths)
```

### Step 4: Firewall Configuration

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

### Step 5: Deploy Application

```bash
cd /home/modasr/modasr-commerce

# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Initialize database
docker-compose -f docker-compose.prod.yml exec backend bash scripts/init-db.sh

# Create admin user
docker-compose -f docker-compose.prod.yml exec backend python scripts/create_admin.py
```

### Step 6: Verify Installation

```bash
# Check services
docker-compose -f docker-compose.prod.yml ps

# Test health endpoints
curl https://api.hosting.modasr.top/health
curl https://hosting.modasr.top

# Check logs
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Step 7: Configure Auto-Renewal for SSL

```bash
# Create renewal script
sudo tee /etc/cron.daily/certbot-renew > /dev/null <<'EOF'
#!/bin/bash
certbot renew --quiet
cd /home/modasr/modasr-commerce
docker-compose -f docker-compose.prod.yml exec -T nginx nginx -s reload
EOF

sudo chmod +x /etc/cron.daily/certbot-renew
```

### Step 8: Setup Automated Backups

```bash
# Create backup script
sudo tee /etc/cron.daily/modasr-backup > /dev/null <<'EOF'
#!/bin/bash
cd /home/modasr/modasr-commerce
docker-compose -f docker-compose.prod.yml exec -T backend bash scripts/backup.sh
EOF

sudo chmod +x /etc/cron.daily/modasr-backup

# Test backup
sudo /etc/cron.daily/modasr-backup
```

## Monitoring

### System Metrics

```bash
# Monitor logs
docker-compose -f docker-compose.prod.yml logs -f

# Check Docker stats
docker stats

# Monitor disk space
df -h /data/modasr
```

### Database Maintenance

```bash
# Vacuum database (cleanup)
docker-compose -f docker-compose.prod.yml exec postgres vacuum analyze;

# Check database size
docker-compose -f docker-compose.prod.yml exec postgres psql -c "SELECT pg_size_pretty(pg_database_size('modasr_commerce'));"
```

## Scaling

### Increase Worker Capacity

```bash
# Edit docker-compose.prod.yml
# Change celery_worker concurrency:
# command: celery -A app.workers worker -l info --concurrency=8

docker-compose -f docker-compose.prod.yml up -d celery_worker
```

### Multiple Celery Workers

```bash
# Add to docker-compose.prod.yml
  celery_worker_2:
    image: modasr-commerce-backend:latest
    command: celery -A app.workers worker -l info --concurrency=4 -n worker2@%h
    # ...
```

## Troubleshooting

### Services Won't Start

```bash
# Check Docker logs
docker-compose -f docker-compose.prod.yml logs backend

# Verify environment variables
docker-compose -f docker-compose.prod.yml config | grep DATABASE_URL

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

### Database Connection Issues

```bash
# Check PostgreSQL
docker-compose -f docker-compose.prod.yml exec postgres psql -U modasr -d modasr_commerce -c "SELECT 1;"

# Check Redis
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
```

### High CPU/Memory Usage

```bash
# Check what's consuming resources
docker stats

# Adjust resource limits in docker-compose.prod.yml
# Add deploy.resources.limits sections

# Optimize Celery workers
# Reduce concurrency or number of workers
```

## Backup & Recovery

### Manual Backup

```bash
docker-compose -f docker-compose.prod.yml exec backend bash scripts/backup.sh
ls -lh /data/modasr/backups/
```

### Restore from Backup

```bash
# List backups
ls -lh /data/modasr/backups/

# Restore
docker-compose -f docker-compose.prod.yml exec backend bash scripts/restore.sh /backups/postgres/modasr_commerce_20240101_120000.sql.gz
```

### Offsite Backup

```bash
# Sync to S3 (example)
aws s3 sync /data/modasr/backups/ s3://my-backup-bucket/modasr/ --delete
```

## Upgrading

### Update Application

```bash
cd /home/modasr/modasr-commerce

# Pull latest code
git pull origin main

# Stop services
docker-compose -f docker-compose.prod.yml down

# Backup database
docker-compose -f docker-compose.prod.yml exec backend bash scripts/backup.sh

# Build new images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Verify
docker-compose -f docker-compose.prod.yml logs backend
```

## Security Hardening

### Rate Limiting

Update API rate limits in `.env`:
```
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60
```

### CORS Configuration

Set allowed origins in `.env`:
```
CORS_ORIGINS=https://hosting.modasr.top,https://admin.hosting.modasr.top
```

### Database Backups

- Automated daily backups configured
- Keep 7-day rotation
- Test restore procedures monthly

### Secrets Rotation

- Rotate `SECRET_KEY` quarterly
- Change database passwords quarterly
- Audit API keys monthly

## Monitoring Services

### Setup Sentry (Error Tracking)

```bash
# Add to .env
SENTRY_DSN=https://your-key@sentry.io/project-id

# Restart backend
docker-compose -f docker-compose.prod.yml restart backend
```

### Setup Prometheus (Metrics)

```bash
# Configure in docker-compose.prod.yml
# Add prometheus service
```

---

**For support:** support@modasr.top  
**Documentation:** https://github.com/modasrdorkhane11251-alt/modasr-commerce
