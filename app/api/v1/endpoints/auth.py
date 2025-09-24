from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, Token
from app.utils.utils import create_access_token, create_refresh_token
from app.crud.user import create_user, authenticate_user

router = APIRouter()


@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await create_user(db, user)
    return db_user


@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.username})
    refresh_token = create_refresh_token({"sub": db_user.username})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
