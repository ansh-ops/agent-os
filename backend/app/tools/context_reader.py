from __future__ import annotations

from app.permissions.roles import Permission
from app.tools.base import BaseTool, ToolInvocationContext


class ContextReaderTool(BaseTool):
    name = "context_reader"
    required_permission = Permission.READ_CONTEXT

    def _invoke(self, context: ToolInvocationContext, **kwargs: object) -> dict[str, str]:
        return {
            "prompt": context.task.prompt,
            "context_text": context.task.context_text or "",
            "uploaded_text": context.task.uploaded_file_text or "",
            "uploaded_file_name": context.task.uploaded_file_name or "",
            "uploaded_file_type": context.task.uploaded_file_type or "",
            "uploaded_file_error": context.task.uploaded_file_error or "",
        }
