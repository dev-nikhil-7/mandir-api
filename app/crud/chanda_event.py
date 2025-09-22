from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.chanda_event import ChandaEvent


async def get_chanda_events(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(ChandaEvent).offset(skip).limit(limit))
    return result.scalars().all()
