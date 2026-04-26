from __future__ import annotations

from app.tools.context_reader import ContextReaderTool
from app.tools.csv_profiler import CSVProfilerTool


class ToolRegistry:
    def __init__(self) -> None:
        self.context_reader = ContextReaderTool()
        self.csv_profiler = CSVProfilerTool()
