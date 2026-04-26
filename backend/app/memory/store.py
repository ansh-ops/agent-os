from __future__ import annotations

from app.schemas.task import AgentName, MemoryEntry, MemoryEntryType, TaskRecord


class SharedMemoryStore:
    def add_entry(
        self,
        task: TaskRecord,
        *,
        entry_type: MemoryEntryType,
        title: str,
        content: str,
        source_agent: AgentName | None = None,
        metadata: dict[str, str] | None = None,
    ) -> TaskRecord:
        task.memory.append(
            MemoryEntry(
                type=entry_type,
                title=title,
                content=content,
                source_agent=source_agent,
                metadata=metadata or {},
            )
        )
        return task
