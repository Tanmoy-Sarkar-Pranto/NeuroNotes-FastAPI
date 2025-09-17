from app.api.v1.routes.user import router as user_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.topic import router as topic_router
from app.api.v1.routes.note import router as note_router
from app.api.v1.routes.tag import router as tag_router

__all__ = ["user_router", "auth_router", "topic_router", "note_router", "tag_router"]