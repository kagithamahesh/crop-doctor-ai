
from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.core.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.crop import router as crop_router
from app.api.v1.review import router as review_router
from app.api.v1.farm import router as farm_router
from app.api.v1.detection import router as detection_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)
app.include_router(
    detection_router,
    prefix="/api/v1/detection",
    tags=["Disease Detection"],
)

app.include_router(
    farm_router,
    prefix="/api/v1/farms",
    tags=["Farms"],
)

app.include_router(
    review_router,
    prefix="/api/v1/reviews",
    tags=["Review"],
)
app.include_router(
    crop_router,
    prefix="/api/v1/crops",
    tags=["Crop"],
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