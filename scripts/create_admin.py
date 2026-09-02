"""Create initial admin user."""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.models.user import User
from app.models.tenant import Tenant
from app.security.password import hash_password
import uuid
from datetime import datetime


async def create_initial_admin():
    """Create initial platform admin."""
    async with SessionLocal() as session:
        # Create platform tenant
        platform_tenant = Tenant(
            name="MODASR Platform",
            slug="modasr-platform",
            description="MODASR Commerce Platform",
            telegram_bot_token="placeholder-token-will-be-updated",
        )
        session.add(platform_tenant)
        await session.flush()
        
        # Create admin user
        admin = User(
            tenant_id=platform_tenant.id,
            username="admin",
            email="admin@modasr.top",
            hashed_password=hash_password("ChangeMe123!"),
            first_name="Admin",
            last_name="User",
            is_active=True,
            is_verified=True,
        )
        session.add(admin)
        
        await session.commit()
        
        print("✅ Admin user created successfully!")
        print(f"   Username: admin")
        print(f"   Email: admin@modasr.top")
        print(f"   Password: ChangeMe123!")
        print("   ⚠️  CHANGE PASSWORD IMMEDIATELY IN PRODUCTION")


if __name__ == "__main__":
    asyncio.run(create_initial_admin())
