from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.routes.health import router as health_router
from app.api.routes.timetable import router as timetable_router
from app.api.routes.auth import router as auth_router
from app.api.routes.attendance import router as attendance_router


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(timetable_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(attendance_router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }
