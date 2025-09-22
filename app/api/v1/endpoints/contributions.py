from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.contribution import ContributionCreate, ContributionResponse, ContributionCreateResponse
from app.crud.contribution import create_contribution
from app.crud.contribution import get_contributions
from typing import List
router = APIRouter()


@router.get(
    "/",
    response_model=List[ContributionResponse],
    status_code=status.HTTP_200_OK
)
async def read_contributions(db: AsyncSession = Depends(get_db)):
    """
    Get all contributions with Tola, Contributor, and PaymentMode details
    """
    contributions = await get_contributions(db)
    return [
        {
            "id": row.id,
            "amount": float(row.amount),
            "payment_date": row.payment_date,
            "tola_name": row.tola_name,
            "contributor_name": row.contributor_name,
            "payment_mode": row.payment_mode,
        }
        for row in contributions
    ]


@router.post(
    "/",
    response_model=ContributionCreateResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_new_contribution(
    contribution_in: ContributionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new Contribution entry
    """
    contribution = await create_contribution(db, contribution_in)
    return contribution
