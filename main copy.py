import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db
from backend.z.gmailhandlerautomation import router as gmail_automation_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown
    # Add any cleanup code here if needed
    pass


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Gmail Automation Dashboard API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set up CORS - Use environment variables for production
cors_origins = []
if settings.BACKEND_CORS_ORIGINS:
    cors_origins.extend(settings.BACKEND_CORS_ORIGINS)

# Add default development origins if not in production
if not os.getenv("ENVIRONMENT") == "production":
    cors_origins.extend(
        [
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:5175",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "http://127.0.0.1:5175",
        ]
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(gmail_automation_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Gmail Automation Dashboard API", "version": settings.VERSION}


@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}


@app.get("/health")
async def health_check_root():
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
