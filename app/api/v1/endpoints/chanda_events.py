from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.chanda_event import ChandaEventResponse
from app.crud.chanda_event import get_chanda_events

router = APIRouter()


@router.get(
    "",
    response_model=List[ChandaEventResponse],
    status_code=status.HTTP_200_OK
)
async def read_chanda_events(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Get all Chanda Events with pagination.
    """
    events = await get_chanda_events(db, skip=skip, limit=limit)
    return events
