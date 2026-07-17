from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas, security
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import set_committed_value

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

async def get_users_offers(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Offer).where(models.Offer.user_id == user_id).options(selectinload(models.Offer.prices)))
    return result.scalars().all()

async def create_user_offer(db: AsyncSession, offer: schemas.OfferCreate, user_id: int, title: str = None, current_price: float = None):
    new_offer = models.Offer(
        url = offer.url,
        user_id = user_id,
        title = title,
        current_price = current_price
    )

    db.add(new_offer)
    await db.flush()

    historical_prices = []
    if current_price is not None:
        new_price = models.PriceHistory(
            offer_id = new_offer.id,
            price = current_price
        )

        db.add(new_price)
        historical_prices.append(new_price)

    await db.commit()
    await db.refresh(new_offer)

    set_committed_value(new_offer, 'prices', historical_prices)
    
    return new_offer