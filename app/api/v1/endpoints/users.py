from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user, get_user_by_email

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_new_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, username=user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db, user_in)
