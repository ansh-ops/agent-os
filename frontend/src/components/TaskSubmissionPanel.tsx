"use client";

import { useState, useTransition } from "react";

import { createTask } from "@/lib/api";
import { SAMPLE_TASK_PRESETS } from "@/lib/sampleTasks";
import { TaskRecord, TaskType } from "@/types";

interface TaskSubmissionPanelProps {
  onTaskCreated: (task: TaskRecord) => void;
}

const OPTIONS: Array<{ label: string; value: TaskType }> = [
  { label: "Auto route", value: "auto" },
  { label: "Research", value: "research" },
  { label: "Planning", value: "planning" },
  { label: "Data", value: "data" },
];

export function TaskSubmissionPanel({ onTaskCreated }: TaskSubmissionPanelProps) {
  const [prompt, setPrompt] = useState("Research AI agent operating systems and summarize the strongest MVP patterns.");
  const [taskType, setTaskType] = useState<TaskType>("auto");
  const [contextText, setContextText] = useState(
    "Focus on orchestration, shared memory, permissions, and execution visibility. Prioritize production-style tradeoffs."
  );
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const applyPreset = (presetId: string) => {
    const preset = SAMPLE_TASK_PRESETS.find((item) => item.id === presetId);
    if (!preset) {
      return;
    }
    setTaskType(preset.taskType);
    setPrompt(preset.prompt);
    setContextText(preset.contextText);
    setError(null);
  };

  const handleSubmit = () => {
    setError(null);
    startTransition(async () => {
      try {
        const task = await createTask({ prompt, taskType, contextText, uploadedFile });
        onTaskCreated(task);
      } catch (submissionError) {
        setError(submissionError instanceof Error ? submissionError.message : "Task submission failed.");
      }
    });
  };

  return (
    <section className="min-w-0 overflow-hidden rounded-[28px] border border-line bg-panel p-6 shadow-panel">
      <div className="mb-5 flex min-w-0 flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <p className="text-xs uppercase tracking-[0.24em] text-accent">Task Submission</p>
          <h2 className="mt-2 break-words text-2xl font-semibold text-ink">Dispatch work into the agent runtime</h2>
        </div>
        <div className="w-fit shrink-0 rounded-full border border-line px-4 py-2 text-xs text-stone-600">LangGraph-ready routing</div>
      </div>

      <div className="grid min-w-0 gap-4">
        <div className="grid min-w-0 gap-3">
          <span className="text-sm font-medium text-ink">Quick demo tasks</span>
          <div className="grid min-w-0 gap-3 md:grid-cols-3">
            {SAMPLE_TASK_PRESETS.map((preset) => (
              <button
                key={preset.id}
                type="button"
                className="min-w-0 rounded-2xl border border-line bg-white px-4 py-4 text-left transition hover:border-accent hover:bg-emerald-50"
                onClick={() => applyPreset(preset.id)}
              >
                <p className="break-words text-sm font-semibold text-ink">{preset.label}</p>
                <p className="mt-2 break-words text-sm text-stone-700">{preset.prompt}</p>
                <p className="mt-3 break-words text-xs uppercase tracking-[0.16em] text-stone-500">
                  {preset.taskType}
                  {preset.fileHint ? ` • ${preset.fileHint}` : ""}
                </p>
              </button>
            ))}
          </div>
        </div>

        <label className="grid min-w-0 gap-2">
          <span className="text-sm font-medium text-ink">Task prompt</span>
          <textarea
            className="min-h-36 rounded-2xl border border-line bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-accent"
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
          />
        </label>

        <div className="grid min-w-0 gap-4 md:grid-cols-[minmax(0,1fr)_minmax(0,1.4fr)]">
          <label className="grid min-w-0 gap-2">
            <span className="text-sm font-medium text-ink">Task type</span>
            <select
              className="rounded-2xl border border-line bg-white px-4 py-3 text-sm text-ink outline-none focus:border-accent"
              value={taskType}
              onChange={(event) => setTaskType(event.target.value as TaskType)}
            >
              {OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          <label className="grid min-w-0 gap-2">
            <span className="text-sm font-medium text-ink">Optional file upload</span>
            <input
              className="rounded-2xl border border-dashed border-line bg-white px-4 py-3 text-sm text-stone-600 file:mr-4 file:rounded-full file:border-0 file:bg-accent file:px-4 file:py-2 file:text-white"
              type="file"
              accept=".csv,.txt,.md,.markdown,.pdf,.docx"
              onChange={(event) => setUploadedFile(event.target.files?.[0] ?? null)}
            />
            <span className="break-words text-xs text-stone-500">Research: PDF, DOCX, MD, TXT. Data: CSV.</span>
          </label>
        </div>

        <label className="grid min-w-0 gap-2">
          <span className="text-sm font-medium text-ink">Shared context</span>
          <textarea
            className="min-h-28 rounded-2xl border border-line bg-white px-4 py-3 text-sm text-ink outline-none transition focus:border-accent"
            value={contextText}
            onChange={(event) => setContextText(event.target.value)}
          />
        </label>

        {error ? <p className="break-words text-sm text-rose-700">{error}</p> : null}

        <button
          className="inline-flex items-center justify-center rounded-full bg-ink px-5 py-3 text-sm font-semibold text-white transition hover:bg-accent disabled:cursor-not-allowed disabled:bg-stone-400"
          onClick={handleSubmit}
          disabled={isPending || prompt.trim().length < 3}
        >
          {isPending ? "Starting workflow..." : "Create Task"}
        </button>
      </div>
    </section>
  );
}
