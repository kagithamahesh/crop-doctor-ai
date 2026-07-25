
from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.core.config import settings
from app.api.v1.auth import router as auth_router



app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)
@app.get("/")
def root():
    return {"message": "Hello Crop Doctor AI"}