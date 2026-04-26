export type TaskType = "auto" | "research" | "data" | "planning";
export type TaskStatus =
  | "queued"
  | "planning"
  | "running"
  | "waiting_on_agent"
  | "under_review"
  | "completed"
  | "failed";

export type AgentName =
  | "supervisor"
  | "research_agent"
  | "data_agent"
  | "planning_agent"
  | "critic_agent";

export interface TraceEntry {
  id: string;
  agent: AgentName;
  step_name: string;
  prompt_summary: string;
  status: "started" | "completed" | "failed";
  created_at: string;
  started_at: string;
  finished_at?: string | null;
  output_summary?: string | null;
  error?: string | null;
}

export interface MemoryEntry {
  id: string;
  type: string;
  title: string;
  content: string;
  source_agent?: AgentName | null;
  created_at: string;
  metadata: Record<string, string>;
}

export interface AgentResult {
  agent: AgentName;
  summary: string;
  structured_output: Record<string, unknown>;
  suggested_next_action?: string | null;
}

export interface TaskArtifact {
  name: string;
  artifact_type: "text" | "json";
  content: string;
  created_at: string;
}

export interface TaskRecord {
  id: string;
  prompt: string;
  task_type: TaskType;
  inferred_task_type?: TaskType | null;
  status: TaskStatus;
  uploaded_file_name?: string | null;
  uploaded_file_path?: string | null;
  uploaded_file_type?: string | null;
  uploaded_file_text?: string | null;
  uploaded_file_error?: string | null;
  context_text?: string | null;
  result?: string | null;
  result_sections: Array<{
    title: string;
    content: string;
    details?: Record<string, unknown>;
  }>;
  artifacts: TaskArtifact[];
  traces: TraceEntry[];
  memory: MemoryEntry[];
  agent_outputs: AgentResult[];
  error?: string | null;
  created_at: string;
  updated_at: string;
}

export interface TaskCollection {
  items: Array<Pick<TaskRecord, "id" | "prompt" | "task_type" | "inferred_task_type" | "status" | "created_at" | "updated_at">>;
}

export type RuntimeMode = "mock" | "llm_active" | "llm_misconfigured";

export interface ProviderStatus {
  mode: RuntimeMode;
  provider_key_present: boolean;
  mock_agents_enabled: boolean;
  sdk_installed: boolean;
  provider_reachable: boolean;
  provider_name: string;
  last_error?: string | null;
}
