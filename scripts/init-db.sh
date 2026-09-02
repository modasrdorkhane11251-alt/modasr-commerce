#!/bin/bash

# MODASR Commerce - Database Initialization Script
# Run migrations and create initial data

set -e

echo "🚀 MODASR Commerce - Database Initialization"
echo "============================================="

# Check if we're in Docker
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL not set"
    exit 1
fi

echo "📦 Running migrations..."
cd /app
alembic upgrade head

echo "✅ Database initialized successfully!"
echo ""
echo "Next steps:"
echo "1. Create admin user: python scripts/create_admin.py"
echo "2. Create initial tenant: python scripts/create_tenant.py"
