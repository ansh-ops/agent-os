import { buildDownloadUrl } from "@/lib/api";
import { TaskRecord } from "@/types";

export function FinalOutputView({ task }: { task: TaskRecord | null }) {
  return (
    <section className="min-w-0 overflow-hidden rounded-[28px] border border-line bg-panel p-6 shadow-panel">
      <div className="flex min-w-0 flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0">
          <p className="text-xs uppercase tracking-[0.24em] text-accent">Final Output</p>
          <h2 className="mt-2 text-2xl font-semibold text-ink">Merged response</h2>
        </div>
        {task ? (
          <div className="flex shrink-0 gap-2">
            <a
              className="rounded-full border border-line px-4 py-2 text-xs font-semibold text-ink"
              href={buildDownloadUrl(task.id, "text")}
              target="_blank"
              rel="noreferrer"
            >
              Text
            </a>
            <a
              className="rounded-full border border-line px-4 py-2 text-xs font-semibold text-ink"
              href={buildDownloadUrl(task.id, "json")}
              target="_blank"
              rel="noreferrer"
            >
              JSON
            </a>
          </div>
        ) : null}
      </div>

      {!task ? (
        <p className="mt-5 text-sm text-stone-600">Final artifacts are published here after the specialist run and critic review complete.</p>
      ) : (
        <div className="mt-5 min-w-0 space-y-4">
          {task.result_sections.map((section) => (
            <article key={section.title} className="min-w-0 overflow-hidden rounded-2xl border border-line bg-white px-4 py-4">
              <p className="break-words text-sm font-semibold text-ink">{section.title}</p>
              <p className="mt-3 whitespace-pre-wrap break-words text-sm text-stone-700">{section.content}</p>
              {section.details ? (
                <pre className="mt-4 max-w-full overflow-x-auto whitespace-pre-wrap break-words rounded-2xl bg-ink px-4 py-4 text-xs text-stone-100">
                  {JSON.stringify(section.details, null, 2)}
                </pre>
              ) : null}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
