import { TaskStatus } from "@/types";

const STATUS_STYLES: Record<TaskStatus, string> = {
  queued: "bg-stone-200 text-stone-700",
  planning: "bg-amber-100 text-amber-800",
  running: "bg-sky-100 text-sky-800",
  waiting_on_agent: "bg-orange-100 text-orange-800",
  under_review: "bg-violet-100 text-violet-800",
  completed: "bg-emerald-100 text-emerald-800",
  failed: "bg-rose-100 text-rose-800",
};

export function StatusBadge({ status }: { status: TaskStatus }) {
  return (
    <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${STATUS_STYLES[status]}`}>
      {status.replaceAll("_", " ")}
    </span>
  );
}
