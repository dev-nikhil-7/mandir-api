from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, cast, Date
from datetime import date
from app.db.session import get_db
from app.models.contributor import Contributor
from app.models.pledge import Pledge
from app.models.financial_year import FinancialYear
from app.models.tolas import Tolas
from app.models.contribution import Contribution  # ✅ new import

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def get_dashboard(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Dashboard API:
    - Total contributor count
    - Sum of pledge amount for current year
    - Tola-wise pledge sum for current year
    - Total collected from contributions (current year)
    - Today's collected
    - % of pledge collected
    """

    # 1. Contributor count
    contributor_count_query = select(func.count(Contributor.id))
    contributor_count = (await db.execute(contributor_count_query)).scalar_one()

    # 2. Current financial year
    current_year_query = select(FinancialYear).where(
        FinancialYear.is_current == True)
    current_year = (await db.execute(current_year_query)).scalar_one_or_none()

    if not current_year:
        raise HTTPException(
            status_code=404,
            detail="No current financial year set."
        )

    # 3. Total pledge for current year
    total_pledge_query = select(func.coalesce(func.sum(Pledge.amount), 0)).where(
        Pledge.financial_year_id == current_year.id
    )
    total_pledge = (await db.execute(total_pledge_query)).scalar_one()

    # 4. Tola-wise pledge sum for current year
    tol_wise_query = (
        select(
            Tolas.tola_name,
            func.coalesce(func.sum(Pledge.amount), 0).label("total_amount")
        )
        .join(Contributor, Contributor.tola_id == Tolas.id)
        .join(Pledge, Pledge.contributor_id == Contributor.id)
        .where(Pledge.financial_year_id == current_year.id)
        .group_by(Tolas.id)
    )
    tol_wise_results = (await db.execute(tol_wise_query)).all()

    # 5. Total collected for current year (join via event_id if needed, else direct)
    total_collected_query = select(
        func.coalesce(func.sum(Contribution.amount), 0))
    total_collected = (await db.execute(total_collected_query)).scalar_one()

    # 6. Today's collected
    today_collected_query = select(
        func.coalesce(func.sum(Contribution.amount), 0)
    ).where(
        cast(Contribution.payment_date, Date) == date.today()
    )
    today_collected = (await db.execute(today_collected_query)).scalar_one()

    # 7. Percentage collected vs pledged
    collected_percent = (float(total_collected) /
                         float(total_pledge) * 100) if total_pledge > 0 else 0

    return {
        "contributor_count": contributor_count,
        "total_pledge": float(total_pledge),
        "total_collected": float(total_collected),
        "today_collected": float(today_collected),
        "collected_percent": round(collected_percent, 2),
        "tol_wise_pledge": [
            {"tola_name": row.tola_name,
                "total_amount": float(row.total_amount)}
            for row in tol_wise_results
        ],
    }
