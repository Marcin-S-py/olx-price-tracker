from fastapi import APIRouter, Depends, status
from app import schemas, database, crud, deps, models
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/offer", tags=["offers"])

@router.post("/add", response_model=schemas.Offer, status_code=status.HTTP_201_CREATED)
async def add_offer(offer: schemas.OfferCreate, current_user: models.User = Depends(deps.get_current_user), db: AsyncSession = Depends(database.get_db)):
    return await crud.create_user_offer(db=db, offer=offer, user_id=current_user.id)

@router.get('/my-offers', response_model=list[schemas.Offer], status_code=status.HTTP_200_OK)
async def my_offers(current_user: models.User = Depends(deps.get_current_user), db: AsyncSession = Depends(database.get_db)):
    return await crud.get_users_offers(db=db, user_id=current_user.id)