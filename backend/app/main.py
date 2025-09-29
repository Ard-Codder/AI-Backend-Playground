"""
Main FastAPI application file
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .routes import auth, ml, tasks, users


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
    app.include_router(
        users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"]
    )
    app.include_router(
        tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"]
    )
    app.include_router(
        ml.router, prefix=f"{settings.API_V1_STR}/ml", tags=["machine-learning"]
    )

    return app


# Create application
app = create_application()


@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint"""
    return JSONResponse(
        content={
            "message": "ML-Backend Playground API",
            "version": settings.VERSION,
            "docs": "/docs",
            "redoc": "/redoc",
        }
    )


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint"""
    return JSONResponse(
        content={"status": "healthy", "environment": settings.ENVIRONMENT}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG, log_level="info"
    )
