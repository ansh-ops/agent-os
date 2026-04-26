import { ProviderStatus, TaskCollection, TaskRecord, TaskType } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

export async function fetchTasks(): Promise<TaskCollection> {
  const response = await fetch(`${API_BASE_URL}/tasks`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to load tasks");
  }
  return response.json();
}

export async function fetchProviderStatus(): Promise<ProviderStatus> {
  const response = await fetch(`${API_BASE_URL}/system/status`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to load provider status");
  }
  return response.json();
}

export async function fetchTask(taskId: string): Promise<TaskRecord> {
  const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to load task");
  }
  return response.json();
}

export async function createTask(input: {
  prompt: string;
  taskType: TaskType;
  contextText?: string;
  uploadedFile?: File | null;
}): Promise<TaskRecord> {
  const formData = new FormData();
  formData.append("prompt", input.prompt);
  formData.append("task_type", input.taskType);
  if (input.contextText) {
    formData.append("context_text", input.contextText);
  }
  if (input.uploadedFile) {
    formData.append("uploaded_file", input.uploadedFile);
  }

  const response = await fetch(`${API_BASE_URL}/tasks`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) {
    throw new Error("Failed to create task");
  }
  return response.json();
}

export function buildDownloadUrl(taskId: string, format: "text" | "json") {
  return `${API_BASE_URL}/tasks/${taskId}/download?format=${format}`;
}
