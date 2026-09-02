#!/bin/bash

# MODASR Commerce - Backup Script
# Backup PostgreSQL database

set -e

BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/modasr_commerce_$DATE.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "💾 Backing up database..."
pg_dump -U modasr -h postgres modasr_commerce | gzip > "$BACKUP_FILE"

echo "✅ Backup completed: $BACKUP_FILE"

# Keep only last 7 days of backups
echo "🧹 Cleaning old backups (keeping last 7 days)..."
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete

echo "✅ Backup cleanup completed!"
