# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from app.core import validation_exception_handler
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.api.v1 import user_router, auth_router, topic_router, note_router, tag_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully!")
    yield
    # Shutdown (add cleanup if needed)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(user_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(topic_router, prefix=settings.API_V1_STR)
app.include_router(note_router, prefix=settings.API_V1_STR)
app.include_router(tag_router, prefix=settings.API_V1_STR)

# Serve static files (frontend build)
static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/", include_in_schema=False)
    async def read_index():
        return FileResponse(os.path.join(static_dir, "index.html"))

    @app.get("/{catchall:path}", include_in_schema=False)
    async def read_index_catchall():
        return FileResponse(os.path.join(static_dir, "index.html"))
else:
    @app.get("/")
    async def root():
        """Health check endpoint."""
        return {
            "message": f"Welcome to {settings.PROJECT_NAME}",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT
        }


@app.get("/health")
async def health_check():
    """Health check for monitoring."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", settings.PORT))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True if settings.ENVIRONMENT == "development" else False
    )