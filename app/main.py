from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.router import router as api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Finance Dashboard Backend with RBAC",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(api_router)


# Root endpoint (health check)
@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to Finance Dashboard API"}