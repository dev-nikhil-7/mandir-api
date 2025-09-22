from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.tolas import Tolas
from app.models.villages import Village
from sqlalchemy.orm import joinedload


async def get_all_tola(db: AsyncSession):
    result = await db.execute(select(Tolas).options(joinedload(Tolas.village)))
    return result.scalars().all()
