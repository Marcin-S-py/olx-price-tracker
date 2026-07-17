from fastapi import FastAPI, HTTPException, status, Depends
from app import schemas, crud, database, deps, models
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers import auth, offers

app = FastAPI()

app.include_router(auth.router)
app.include_router(offers.router)

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):

    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    return await crud.create_user(db=db, user=user)

@app.post("/me/")
async def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    return current_user