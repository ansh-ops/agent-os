from __future__ import annotations

import csv
from pathlib import Path

from app.agents.contracts import DataColumnProfile, DataOutput
from app.permissions.roles import Permission
from app.tools.base import BaseTool, ToolInvocationContext


class CSVProfilerTool(BaseTool):
    name = "csv_profiler"
    required_permission = Permission.READ_CSV

    def _invoke(self, context: ToolInvocationContext, **kwargs: object) -> DataOutput:
        if not context.task.uploaded_file_path:
            raise ValueError("CSV profiler requires an uploaded CSV file.")

        file_path = Path(context.task.uploaded_file_path)
        with file_path.open("r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            headers = reader.fieldnames or []

        profiles: list[DataColumnProfile] = []
        for header in headers:
            values = [row.get(header, "") for row in rows]
            non_empty = [value for value in values if value not in ("", None)]
            numeric_values: list[float] = []
            for value in non_empty:
                try:
                    numeric_values.append(float(value))
                except ValueError:
                    continue

            profile = DataColumnProfile(
                column=header,
                non_empty=len(non_empty),
                unique_values=len(set(non_empty)),
                sample_values=non_empty[:3],
            )
            if numeric_values:
                profile.numeric_min = min(numeric_values)
                profile.numeric_max = max(numeric_values)
                profile.numeric_avg = round(sum(numeric_values) / len(numeric_values), 2)
            profiles.append(profile)

        return DataOutput(
            file_name=context.task.uploaded_file_name,
            row_count=len(rows),
            column_count=len(headers),
            columns=profiles,
            observations=[
                "Check sparse columns before using them in automation or reporting.",
                "Wide numeric ranges may hide cohorts or outliers worth splitting.",
                "Identifier-like columns should be separated from analytical features.",
            ],
            next_steps=[
                "Validate the business meaning of each high-value column.",
                "Create a compact dashboard around the most important numeric metrics.",
                "Investigate missing values before forecasting or segmentation.",
            ],
        )
