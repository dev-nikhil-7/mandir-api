from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contribution import Contribution
from app.schemas.contribution import ContributionCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.contribution import Contribution
from app.models.tolas import Tolas
from app.models.contributor import Contributor
from app.models.payment_mode import PaymentMode


async def get_contributions(db: AsyncSession):
    result = await db.execute(
        select(
            Contribution.id,
            Contribution.amount,
            Contribution.payment_date,
            Tolas.tola_name.label("tola_name"),
            Contributor.name.label("contributor_name"),
            PaymentMode.name.label("payment_mode"),
        )
        .join(Tolas, Contribution.tola_id == Tolas.id)
        .join(Contributor, Contribution.contributor_id == Contributor.id)
        .join(PaymentMode, Contribution.payment_mode_id == PaymentMode.id)
    )
    return result.all()


async def create_contribution(db: AsyncSession, contribution_in: ContributionCreate):
    contribution = Contribution(**contribution_in.dict())
    db.add(contribution)
    await db.commit()
    await db.refresh(contribution)
    return contribution
