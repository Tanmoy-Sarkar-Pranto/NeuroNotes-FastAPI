from app.api.v1.routes.user import router as user_router
from app.api.v1.routes.auth import router as auth_router

__all__ = ["user_router", "auth_router"]