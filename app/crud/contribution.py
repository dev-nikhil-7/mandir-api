from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contribution import Contribution
from app.schemas.contribution import ContributionCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.contribution import Contribution
from app.models.tolas import Tolas
from app.models.contributor import Contributor
from app.models.payment_mode import PaymentMode
from app.models.pledge import Pledge


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


async def create_contribution(db: AsyncSession, contribution_in):
    contributor_id = contribution_in.contributor_id

    # 🟢 Branch: New Contributor
    if contribution_in.is_new_contributor:
        # 1. Insert Contributor
        new_contributor = Contributor(
            tola_id=contribution_in.tola_id,
            name=contribution_in.contributor_name,
            father_or_spouse_name=contribution_in.father_or_spouse_name,
            contact=contribution_in.contact,
        )
        db.add(new_contributor)
        await db.flush()  # ensures ID is available
        contributor_id = new_contributor.id

        # 2. Insert Pledge (auto for current financial year)
        pledge = Pledge(
            contributor_id=contributor_id,
            financial_year_id=contribution_in.financial_year_id,
            amount=contribution_in.amount,
            notes=f"Auto-pledge from new contribution {contribution_in.receipt_id}",
        )
        db.add(pledge)
        await db.flush()

    else:
        # 🟡 Branch: Existing Contributor → update contact if provided
        if contribution_in.contact:
            await db.execute(
                update(Contributor)
                .where(Contributor.id == contributor_id)
                .values(contact=contribution_in.contact)
            )

    # 🔵 3. Insert Contribution (common for both cases)
    contribution = Contribution(
        contributor_id=contributor_id,
        tola_id=contribution_in.tola_id,
        event_id=contribution_in.event_id,
        payment_mode_id=contribution_in.payment_mode_id,
        financial_year_id=contribution_in.financial_year_id,
        payment_date=contribution_in.payment_date,
        amount=contribution_in.amount,
        receipt_id=contribution_in.receipt_id,
    )
    db.add(contribution)

    # Commit all changes in one go
    await db.commit()
    await db.refresh(contribution)

    return contribution
