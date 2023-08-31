from fastapi import APIRouter

from app.dummy_users.handlers.dummy_users import dummy_users_router

router = APIRouter()

# Register all routers of all the apps here
router.include_router(dummy_users_router, prefix="/dummy-users", tags=["dummy-users"])
