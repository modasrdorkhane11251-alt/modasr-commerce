#!/bin/bash

# MODASR Commerce - Restore Script
# Restore PostgreSQL database from backup

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup-file>"
    echo "Example: ./restore.sh /backups/postgres/modasr_commerce_20240101_120000.sql.gz"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "⚠️  WARNING: This will overwrite the current database!"
read -p "Continue? (yes/no): " -r CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Restore cancelled"
    exit 1
fi

echo "📥 Restoring database..."
gunzip -c "$BACKUP_FILE" | psql -U modasr -h postgres modasr_commerce

echo "✅ Database restore completed!"
