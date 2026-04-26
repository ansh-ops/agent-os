import { TaskRecord } from "@/types";

import { StatusBadge } from "./StatusBadge";

export function WorkflowView({ task }: { task: TaskRecord | null }) {
  return (
    <section className="min-w-0 overflow-hidden rounded-[28px] border border-line bg-panel p-6 shadow-panel">
      <div className="mb-5 flex min-w-0 flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0">
          <p className="text-xs uppercase tracking-[0.24em] text-accent">Agent Workflow</p>
          <h2 className="mt-2 text-2xl font-semibold text-ink">Execution trace</h2>
        </div>
        {task ? <StatusBadge status={task.status} /> : null}
      </div>

      {!task ? (
        <p className="text-sm text-stone-600">Submit or select a task to inspect orchestration state, agent ordering, and step summaries.</p>
      ) : (
        <div className="min-w-0 space-y-4">
          <div className="min-w-0 overflow-hidden rounded-2xl border border-line bg-white px-4 py-4">
            <p className="break-words text-sm font-medium text-ink">{task.prompt}</p>
            <p className="mt-2 text-xs uppercase tracking-[0.16em] text-stone-500">
              Requested: {task.task_type} • Routed: {task.inferred_task_type ?? task.task_type}
            </p>
          </div>
          <div className="min-w-0 space-y-3">
            {task.traces.map((trace) => (
              <article key={trace.id} className="min-w-0 overflow-hidden rounded-2xl border border-line bg-white px-4 py-4">
                <div className="flex min-w-0 flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div className="min-w-0">
                    <p className="break-words text-sm font-semibold capitalize text-ink">{trace.agent.replaceAll("_", " ")}</p>
                    <p className="break-words text-xs uppercase tracking-[0.16em] text-stone-500">{trace.step_name.replaceAll("_", " ")}</p>
                  </div>
                  <span className="w-fit shrink-0 rounded-full bg-stone-100 px-3 py-1 text-xs font-medium text-stone-700">{trace.status}</span>
                </div>
                <p className="mt-3 break-words text-sm text-stone-700">{trace.prompt_summary}</p>
                <p className="mt-2 break-words text-sm text-ink">{trace.output_summary ?? "Execution in progress..."}</p>
                {trace.error ? <p className="mt-2 break-words text-sm text-rose-700">{trace.error}</p> : null}
                <p className="mt-3 break-words text-xs text-stone-500">
                  {new Date(trace.started_at).toLocaleString()} {trace.finished_at ? `→ ${new Date(trace.finished_at).toLocaleString()}` : ""}
                </p>
              </article>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
