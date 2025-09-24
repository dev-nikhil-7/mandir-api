from app.api.v1.endpoints import contributions
from fastapi import APIRouter
from app.api.v1.endpoints import tola
from app.api.v1.endpoints import contributors  # Import the new router
from app.api.v1.endpoints import dashboard  # Import the new router
from app.api.v1.endpoints import chanda_events  # Import the new router
from app.api.v1.endpoints import contributions
from app.api.v1.endpoints import auth
api_router = APIRouter()

api_router.include_router(tola.router, prefix="/tolas", tags=["tolas"])
api_router.include_router(
    contributors.router, prefix="/contributors", tags=["Contributors"])
api_router.include_router(
    dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(
    chanda_events.router, prefix="/chanda-events", tags=["Chanda Events"])

api_router.include_router(
    contributions.router,
    prefix="/contributions",
    tags=["contributions"]
)

api_router.include_router(
    auth.router,
    prefix="/users",
    tags=["Auth"]
)
