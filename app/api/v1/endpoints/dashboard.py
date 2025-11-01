from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, cast, Date
from datetime import date
from app.db.session import get_db
from app.models.contributor import Contributor
from app.models.pledge import Pledge
from app.models.financial_year import FinancialYear
from app.models.expenses import Expense
from app.models.tolas import Tolas
from app.models.contribution import Contribution  # ✅ new import

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def get_dashboard(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Dashboard API:
    - Total contributor count
    - Total pledge for current financial year
    - Total collected amount
    - Total expenses (all time or per year)
    - % of pledge collected
    """

    # 1️⃣ Contributor count
    contributor_count_query = select(func.count(Contributor.id))
    contributor_count = (await db.execute(contributor_count_query)).scalar_one()

    # 2️⃣ Current financial year
    current_year_query = select(FinancialYear).where(
        FinancialYear.is_current == True)
    current_year = (await db.execute(current_year_query)).scalar_one_or_none()
    if not current_year:
        raise HTTPException(
            status_code=404, detail="No current financial year set.")

    # 3️⃣ Total pledge (for current year)
    total_pledge_query = select(func.coalesce(func.sum(Pledge.amount), 0)).where(
        Pledge.financial_year_id == current_year.id
    )
    total_pledge = (await db.execute(total_pledge_query)).scalar_one()

    # 4️⃣ Total collected (for current year)
    total_collected_query = select(func.coalesce(func.sum(Contribution.amount), 0)).where(
        Contribution.financial_year_id == current_year.id
    )
    total_collected = (await db.execute(total_collected_query)).scalar_one()

    # 5️⃣ Total expenses (for current year)
    total_expense_query = select(func.coalesce(func.sum(Expense.amount), 0))
    total_expense = (await db.execute(total_expense_query)).scalar_one()

    # 6️⃣ Percentage collected vs pledged
    collected_percent = (float(total_collected) /
                         float(total_pledge) * 100) if total_pledge > 0 else 0

    # 7️⃣ Tola-wise pledge
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

    # 8️⃣ Tola-wise collection
    tol_wise_collection_query = (
        select(
            Tolas.tola_name,
            func.coalesce(func.sum(Contribution.amount),
                          0).label("total_collected")
        )
        .join(Contributor, Contributor.tola_id == Tolas.id)
        .join(
            Contribution,
            (Contribution.contributor_id == Contributor.id)
            & (Contribution.financial_year_id == current_year.id),
            isouter=True
        )
        .group_by(Tolas.id)
    )
    tol_wise_collection_results = (await db.execute(tol_wise_collection_query)).all()

    # ✅ Final Dashboard Response
    return {
        "contributor_count": contributor_count,
        "total_pledge": float(total_pledge),
        "total_collected": float(total_collected),
        "total_expense": float(total_expense),  # 👈 added
        "collected_percent": round(collected_percent, 2),
        "tol_wise_pledge": [
            {"tola_name": row.tola_name,
                "total_amount": float(row.total_amount)}
            for row in tol_wise_results
        ],
        "tol_wise_collection": [
            {"tola_name": row.tola_name,
                "total_collected": float(row.total_collected)}
            for row in tol_wise_collection_results
        ],
    }


async def get_tola_collections(db: AsyncSession, financial_year_id: int = 5):
    result = await db.execute(
        select(
            Tolas.id,
            Tolas.tola_name,
            func.coalesce(func.sum(Pledge.amount),
                          0).label("total_pledged"),
            func.coalesce(func.sum(Contribution.amount),
                          0).label("total_paid"),
        )
        .join(Contributor, Contributor.tola_id == Tolas.id)
        .outerjoin(
            Pledge,
            (Pledge.contributor_id == Contributor.id)
            & (Pledge.financial_year_id == financial_year_id)   # ✅ filter pledges
        )
        .outerjoin(
            Contribution,
            (Contribution.contributor_id == Contributor.id)
            # ✅ filter contributions
            & (Contribution.financial_year_id == financial_year_id)
        )
        .group_by(Tolas.id, Tolas.tola_name)
        .order_by(Tolas.tola_name)
    )
    return result.mappings().all()


@router.get("/tola-wise/collection")
async def tola_wise_collection(db: AsyncSession = Depends(get_db)):
    data = await get_tola_collections(db)
    return {"tolas": data}
