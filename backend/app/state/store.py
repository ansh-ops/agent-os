from __future__ import annotations

import json
from pathlib import Path

from app.core.config import settings
from app.schemas.task import TaskCollection, TaskListItem, TaskRecord, utc_now


class TaskStore:
    def __init__(self) -> None:
        settings.tasks_dir.mkdir(parents=True, exist_ok=True)

    def _task_path(self, task_id: str) -> Path:
        return settings.tasks_dir / f"{task_id}.json"

    def save(self, task: TaskRecord) -> TaskRecord:
        task.updated_at = utc_now()
        self._task_path(task.id).write_text(
            task.model_dump_json(indent=2),
            encoding="utf-8",
        )
        return task

    def get(self, task_id: str) -> TaskRecord:
        path = self._task_path(task_id)
        if not path.exists():
            raise FileNotFoundError(f"Task {task_id} was not found")
        return TaskRecord.model_validate_json(path.read_text(encoding="utf-8"))

    def list(self) -> TaskCollection:
        items: list[TaskListItem] = []
        for path in sorted(settings.tasks_dir.glob("*.json"), reverse=True):
            task = TaskRecord.model_validate_json(path.read_text(encoding="utf-8"))
            items.append(
                TaskListItem(
                    id=task.id,
                    prompt=task.prompt,
                    task_type=task.task_type,
                    inferred_task_type=task.inferred_task_type,
                    status=task.status,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                )
            )
        return TaskCollection(items=items)

    def export_json(self, task_id: str) -> str:
        return json.dumps(self.get(task_id).model_dump(mode="json"), indent=2)
