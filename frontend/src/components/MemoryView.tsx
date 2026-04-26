import { TaskRecord } from "@/types";

export function MemoryView({ task }: { task: TaskRecord | null }) {
  return (
    <section className="min-w-0 overflow-hidden rounded-[28px] border border-line bg-panel p-6 shadow-panel">
      <p className="text-xs uppercase tracking-[0.24em] text-accent">Shared Memory</p>
      <h2 className="mt-2 text-2xl font-semibold text-ink">Context and artifacts</h2>

      {!task ? (
        <p className="mt-5 text-sm text-stone-600">Memory entries appear here as agents persist summaries, facts, outputs, and final artifacts.</p>
      ) : (
        <div className="mt-5 min-w-0 space-y-3">
          {task.memory.map((entry) => (
            <article key={entry.id} className="min-w-0 overflow-hidden rounded-2xl border border-line bg-white px-4 py-4">
              <div className="flex min-w-0 flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div className="min-w-0">
                  <p className="break-words text-sm font-semibold text-ink">{entry.title}</p>
                  <p className="break-words text-xs uppercase tracking-[0.14em] text-stone-500">
                    {entry.type.replaceAll("_", " ")} {entry.source_agent ? `• ${entry.source_agent.replaceAll("_", " ")}` : ""}
                  </p>
                </div>
                <p className="shrink-0 text-xs text-stone-500">{new Date(entry.created_at).toLocaleString()}</p>
              </div>
              <p className="mt-3 whitespace-pre-wrap break-words text-sm text-stone-700">{entry.content}</p>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
