from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from app.memory.store import SharedMemoryStore
from app.orchestration.supervisor import Supervisor
from app.schemas.task import AgentName, TaskCreate, TaskRecord, TaskStatus, TraceEntry, TraceStatus
from app.services.document_ingestion import DocumentIngestionError, extract_document_text
from app.state.store import TaskStore


class TaskExecutionService:
    def __init__(self, task_store: TaskStore, memory_store: SharedMemoryStore) -> None:
        self.task_store = task_store
        self.memory_store = memory_store
        self.supervisor = Supervisor(memory_store)

    async def create_task(
        self,
        payload: TaskCreate,
        *,
        upload_path: Path | None = None,
        upload_name: str | None = None,
    ) -> TaskRecord:
        uploaded_file_text = None
        uploaded_file_type = None
        uploaded_file_error = None
        if upload_path:
            try:
                uploaded_file_text, uploaded_file_type = extract_document_text(upload_path, upload_name)
            except DocumentIngestionError as exc:
                uploaded_file_error = str(exc)
            except Exception as exc:
                uploaded_file_error = f"Could not extract uploaded document text: {exc}"

        task = TaskRecord(
            prompt=payload.prompt,
            task_type=payload.task_type,
            context_text=payload.context_text,
            uploaded_file_name=upload_name,
            uploaded_file_path=str(upload_path) if upload_path else None,
            uploaded_file_type=uploaded_file_type,
            uploaded_file_text=uploaded_file_text,
            uploaded_file_error=uploaded_file_error,
        )
        self.task_store.save(task)
        return task

    def execute_task(self, task_id: str) -> TaskRecord:
        task = self.task_store.get(task_id)
        start_trace = TraceEntry(
            agent=AgentName.SUPERVISOR,
            step_name="task_dispatch",
            prompt_summary=task.prompt,
            status=TraceStatus.STARTED,
        )
        task.status = TaskStatus.RUNNING
        task.traces.append(start_trace)
        self.task_store.save(task)

        try:
            task = self.supervisor.run(task)
            start_trace.status = TraceStatus.COMPLETED
            start_trace.finished_at = datetime.now(timezone.utc)
            start_trace.output_summary = "Supervisor completed orchestration and published final artifacts."
        except Exception as exc:
            task.status = TaskStatus.FAILED
            task.error = str(exc)
            start_trace.status = TraceStatus.FAILED
            start_trace.finished_at = datetime.now(timezone.utc)
            start_trace.error = str(exc)

        self.task_store.save(task)
        return task
