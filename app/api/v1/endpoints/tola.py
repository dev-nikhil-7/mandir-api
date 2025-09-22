from app.crud.tola import get_all_tola
from app.schemas.tola import TolaOut
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.contributor import ContributorWithPledge
from app.crud.contributor import get_contributors_with_current_year_pledge

router = APIRouter()


@router.get(
    "/{tola_id}/contributors",
    response_model=List[ContributorWithPledge],
    status_code=status.HTTP_200_OK,
)
async def read_contributors_by_tola(tola_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get all contributors for a specific Tola along with their pledge for the current year.
    """
    contributors = await get_contributors_with_current_year_pledge(db, tola_id)
    if not contributors:
        raise HTTPException(
            status_code=404,
            detail=f"No contributors found for Tola ID {tola_id} or no current financial year set."
        )

    # Convert SQLAlchemy row tuples into dicts that match schema
    return [
        {
            "id": row.id,
            "name": row.name,
            "contact": row.contact,
            "tola_id": row.tola_id,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
            "pledge_amount": float(row.pledge_amount),
        }
        for row in contributors
    ]


@router.get("/", response_model=list[TolaOut])
async def get_all_tolas(db: AsyncSession = Depends(get_db)):
    tola = await get_all_tola(db)
    return tola
