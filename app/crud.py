from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas, security
from sqlalchemy import select

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        hashed_password = hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalar_one_or_none()