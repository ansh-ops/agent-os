import { TaskCollection } from "@/types";

import { StatusBadge } from "./StatusBadge";

interface TaskListSidebarProps {
  tasks: TaskCollection["items"];
  selectedTaskId: string | null;
  onSelectTask: (taskId: string) => void;
}

export function TaskListSidebar({ tasks, selectedTaskId, onSelectTask }: TaskListSidebarProps) {
  return (
    <aside className="min-w-0 overflow-hidden rounded-[28px] border border-line bg-panel p-6 shadow-panel">
      <p className="text-xs uppercase tracking-[0.24em] text-accent">Task Registry</p>
      <h2 className="mt-2 text-2xl font-semibold text-ink">Recent workflows</h2>
      <div className="mt-5 space-y-3">
        {tasks.length === 0 ? (
          <p className="text-sm text-stone-600">No tasks yet. Create one to populate the workflow registry.</p>
        ) : (
          tasks.map((task) => (
            <button
              key={task.id}
              className={`w-full rounded-2xl border px-4 py-4 text-left transition ${
                selectedTaskId === task.id ? "border-accent bg-emerald-50" : "border-line bg-white hover:border-accent"
              }`}
              onClick={() => onSelectTask(task.id)}
            >
              <div className="flex min-w-0 flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <p className="min-w-0 break-words text-sm font-medium text-ink">{task.prompt}</p>
                <StatusBadge status={task.status} />
              </div>
              <p className="mt-3 break-words text-xs uppercase tracking-[0.14em] text-stone-500">
                {task.inferred_task_type ?? task.task_type} • {new Date(task.updated_at).toLocaleString()}
              </p>
            </button>
          ))
        )}
      </div>
    </aside>
  );
}
