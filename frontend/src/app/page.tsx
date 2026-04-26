"use client";

import { useEffect, useState } from "react";

import { FinalOutputView } from "@/components/FinalOutputView";
import { MemoryView } from "@/components/MemoryView";
import { ProviderStatusBadge } from "@/components/ProviderStatusBadge";
import { TaskListSidebar } from "@/components/TaskListSidebar";
import { TaskSubmissionPanel } from "@/components/TaskSubmissionPanel";
import { WorkflowView } from "@/components/WorkflowView";
import { fetchProviderStatus, fetchTask, fetchTasks } from "@/lib/api";
import { ProviderStatus, TaskCollection, TaskRecord } from "@/types";

export default function HomePage() {
  const [tasks, setTasks] = useState<TaskCollection["items"]>([]);
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [selectedTask, setSelectedTask] = useState<TaskRecord | null>(null);
  const [providerStatus, setProviderStatus] = useState<ProviderStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    async function loadTasks() {
      const [collection, status] = await Promise.all([fetchTasks(), fetchProviderStatus()]);
      if (!mounted) {
        return;
      }
      setTasks(collection.items);
      setProviderStatus(status);
      if (!selectedTaskId && collection.items[0]) {
        setSelectedTaskId(collection.items[0].id);
      }
      setLoading(false);
    }

    void loadTasks();
    const interval = window.setInterval(() => {
      void loadTasks();
    }, 3000);

    return () => {
      mounted = false;
      window.clearInterval(interval);
    };
  }, [selectedTaskId]);

  useEffect(() => {
    if (!selectedTaskId) {
      return;
    }

    let mounted = true;
    async function loadTask() {
      const task = await fetchTask(selectedTaskId);
      if (mounted) {
        setSelectedTask(task);
      }
    }

    void loadTask();
    const interval = window.setInterval(() => {
      void loadTask();
    }, 2000);

    return () => {
      mounted = false;
      window.clearInterval(interval);
    };
  }, [selectedTaskId]);

  const handleTaskCreated = (task: TaskRecord) => {
    setSelectedTaskId(task.id);
    setSelectedTask(task);
    setTasks((current) => [task, ...current]);
  };

  return (
    <main className="relative min-h-screen overflow-x-hidden bg-grid bg-[size:28px_28px]">
      <div className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 sm:py-10">
        <section className="mb-8 min-w-0 rounded-[32px] border border-line bg-panel/90 p-6 shadow-panel backdrop-blur-sm sm:p-8">
          <p className="text-xs uppercase tracking-[0.28em] text-accent">Agent OS</p>
          <div className="mt-4 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div className="min-w-0 max-w-3xl">
              <h1 className="break-words text-3xl font-semibold tracking-tight text-ink md:text-5xl">
                A multi-agent operating system for autonomous task orchestration, shared memory, and visible execution.
              </h1>
              <p className="mt-4 max-w-2xl text-sm leading-6 text-stone-700 md:text-base">
                Submit a task, let the supervisor route it through a graph-driven workflow, inspect shared memory and
                permission-aware tools, and review the final merged artifact with a full execution trace.
              </p>
            </div>
            <div className="min-w-0 shrink-0 flex flex-col gap-3 md:items-end">
              <div className="rounded-[24px] border border-line bg-white px-5 py-4 text-sm text-stone-700">
                {loading ? "Loading tasks..." : `${tasks.length} workflows tracked`}
              </div>
              <ProviderStatusBadge status={providerStatus} />
            </div>
          </div>
        </section>

        <div className="grid min-w-0 gap-6 xl:grid-cols-[320px_minmax(0,1fr)]">
          <TaskListSidebar tasks={tasks} selectedTaskId={selectedTaskId} onSelectTask={setSelectedTaskId} />

          <div className="grid min-w-0 gap-6">
            <TaskSubmissionPanel onTaskCreated={handleTaskCreated} />
            <div className="grid min-w-0 gap-6 lg:grid-cols-2">
              <WorkflowView task={selectedTask} />
              <MemoryView task={selectedTask} />
            </div>
            <FinalOutputView task={selectedTask} />
          </div>
        </div>
      </div>
    </main>
  );
}
