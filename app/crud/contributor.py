from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.contributor import Contributor
from sqlalchemy.orm import joinedload, selectinload
from app.models.tolas import Tolas
from sqlalchemy import select, func
from app.models.pledge import Pledge
from app.models.financial_year import FinancialYear
from app.models.pledge import Pledge
from sqlalchemy import update


async def get_contributor(db: AsyncSession, contributor_id: int):
    """
    Fetches a single contributor by their ID using an asynchronous session.
    """

    # This is the correct way to query with AsyncSession
    result = await db.execute(
        select(Contributor).filter(Contributor.id == contributor_id)
    )

    # Use .scalar_one_or_none() to get a single object or None
    contributor = result.scalar_one_or_none()
    return contributor


async def get_contributors(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Fetches all contributors with optional pagination using an asynchronous session.
    """
    # Use await db.execute() with a select statement
    result = await db.execute(
        select(Contributor).options(selectinload(
            Contributor.tola), selectinload(Contributor.pledges).selectinload(Pledge.financial_year)).offset(skip).limit(limit)
    )

    # Use .scalars().all() to get a list of model instances
    return result.scalars().all()


async def get_contributors_with_current_year_pledge(db: AsyncSession, tola_id: int):
    # Get current financial year
    current_year = (
        await db.execute(select(FinancialYear).where(FinancialYear.is_current == True))
    ).scalar_one_or_none()

    if not current_year:
        return []

    # Contributors + their pledge sum for current year
    result = await db.execute(
        select(
            Contributor.id,
            Contributor.name,
            Contributor.contact,
            Contributor.tola_id,
            Contributor.created_at,
            Contributor.updated_at,
            func.coalesce(func.sum(Pledge.amount), 0).label("pledge_amount"),
        )
        .outerjoin(Pledge, (Pledge.contributor_id == Contributor.id) & (Pledge.financial_year_id == current_year.id))
        .where(Contributor.tola_id == tola_id)
        .group_by(Contributor.id)
    )
    return result.all()


async def update_contributor_with_pledge(db: AsyncSession, contributor_id: int, data: dict, financial_year_id: int):
    # 1. Update contributor
    await db.execute(
        update(Contributor)
        .where(Contributor.id == contributor_id)
        .values(
            name=data.get("name"),
            father_or_spouse_name=data.get("father_or_spouse_name"),
            contact=data.get("contact"),
        )
    )

    # 2. If pledge_amount provided → update pledge
    if data.get("pledge_amount") is not None:
        await db.execute(
            update(Pledge)
            .where(
                Pledge.contributor_id == contributor_id,
                Pledge.financial_year_id == financial_year_id
            )
            .values(amount=data["pledge_amount"])
        )

    await db.commit()
