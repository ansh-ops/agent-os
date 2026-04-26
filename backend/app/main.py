from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as task_router
from app.api.routes import system_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(task_router, prefix=settings.api_prefix)
app.include_router(system_router, prefix=settings.api_prefix)


@app.get("/health")
def healthcheck():
    return {"status": "ok", "app": settings.app_name}
