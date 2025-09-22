from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession  # Use AsyncSession

# Import your dependencies
from app.crud import contributor as crud_contributor
from app.schemas import contributor as schemas_contributor
from app.db.session import get_db

router = APIRouter()


@router.get(
    "/",
    response_model=List[schemas_contributor.Contributor],
    status_code=status.HTTP_200_OK
)
async def read_contributors(skip: int = 0, limit: int = 10000000, db: AsyncSession = Depends(get_db)):
    """
    Get all contributors with pagination.
    """
    # Use await to call the asynchronous CRUD function
    contributors = await crud_contributor.get_contributors(db, skip=skip, limit=limit)
    return contributors


@router.get(
    "/{contributor_id}",
    status_code=status.HTTP_200_OK
)
async def read_contributor(contributor_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single contributor by ID.
    """
    # Use await to call the asynchronous CRUD function
    db_contributor = await crud_contributor.get_contributor(db, contributor_id=contributor_id)
    if db_contributor is None:
        raise HTTPException(
            status_code=404,
            detail="Contributor not found"
        )
    return db_contributor
