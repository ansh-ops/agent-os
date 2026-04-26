from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse

from app.core.config import settings
from app.memory.store import SharedMemoryStore
from app.schemas.task import ArtifactType, TaskCreate, TaskDownloadResponse, TaskType
from app.services.system_status import SystemStatusService
from app.services.task_executor import TaskExecutionService
from app.state.store import TaskStore

router = APIRouter(prefix="/tasks", tags=["tasks"])
system_router = APIRouter(prefix="/system", tags=["system"])

task_store = TaskStore()
memory_store = SharedMemoryStore()
task_service = TaskExecutionService(task_store, memory_store)
system_status_service = SystemStatusService()


async def persist_upload(uploaded_file: UploadFile | None) -> tuple[Path | None, str | None]:
    if not uploaded_file:
        return None, None

    settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(uploaded_file.filename or "").suffix
    file_name = f"{uuid4()}{suffix}"
    file_path = settings.uploads_dir / file_name
    content = await uploaded_file.read()
    file_path.write_bytes(content)
    return file_path, uploaded_file.filename


@router.get("")
def list_tasks():
    return task_store.list()


@system_router.get("/status")
def get_system_status():
    return system_status_service.get_provider_status()


@router.get("/{task_id}")
def get_task(task_id: str):
    try:
        return task_store.get(task_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("")
async def create_task(
    background_tasks: BackgroundTasks,
    prompt: str = Form(...),
    task_type: TaskType = Form(TaskType.AUTO),
    context_text: str | None = Form(None),
    uploaded_file: UploadFile | None = File(default=None),
):
    payload = TaskCreate(prompt=prompt, task_type=task_type, context_text=context_text)
    upload_path, upload_name = await persist_upload(uploaded_file)
    task = await task_service.create_task(payload, upload_path=upload_path, upload_name=upload_name)
    background_tasks.add_task(task_service.execute_task, task.id)
    return task


@router.get("/{task_id}/download", response_model=TaskDownloadResponse)
def download_task(task_id: str, format: ArtifactType = ArtifactType.TEXT):
    task = task_store.get(task_id)
    if format == ArtifactType.JSON:
        return TaskDownloadResponse(task_id=task_id, format=format, content=task_store.export_json(task_id))
    return TaskDownloadResponse(task_id=task_id, format=format, content=task.result or "")


@router.get("/{task_id}/download/text")
def download_task_text(task_id: str):
    task = task_store.get(task_id)
    return PlainTextResponse(task.result or "")
