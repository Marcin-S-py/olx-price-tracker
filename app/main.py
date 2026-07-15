from fastapi import FastAPI, HTTPException, status, Depends
from . import schemas, crud, database
from sqlalchemy.orm import Session

app = FastAPI()

@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):

    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    return await crud.create_user(db=db, user=user)