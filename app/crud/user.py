from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.utils.utils import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(username=user.username, password_hash=hashed_pw,
                   role=user.role, is_active=True)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user
