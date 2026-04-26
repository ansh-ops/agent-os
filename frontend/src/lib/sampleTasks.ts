import { TaskType } from "@/types";

export interface SampleTaskPreset {
  id: string;
  label: string;
  taskType: TaskType;
  prompt: string;
  contextText: string;
  fileHint?: string;
}

export const SAMPLE_TASK_PRESETS: SampleTaskPreset[] = [
  {
    id: "research",
    label: "Document Research",
    taskType: "research",
    prompt: "Read the uploaded project brief and produce a concise technical research summary.",
    contextText:
      "Prioritize shared memory, supervisor routing, explicit permissions, and visible execution traces. Keep recommendations portfolio-friendly.",
    fileHint: "Attach demo-data/technical-brief-source.txt or a PDF/DOCX",
  },
  {
    id: "planning",
    label: "Project Plan",
    taskType: "planning",
    prompt: "Plan a 2-week implementation roadmap for an internal AI analyst platform with a small product team.",
    contextText:
      "Assume two engineers and one designer. Include milestones, risks, and a task checklist that can be executed immediately.",
  },
  {
    id: "data",
    label: "CSV Analysis",
    taskType: "data",
    prompt: "Analyze this CSV and recommend the most important operational next steps.",
    contextText:
      "Focus on basic profiling, data quality risks, and practical follow-up analysis. Use the bundled sales pipeline mock data for the demo.",
    fileHint: "Attach demo-data/sales_pipeline.csv",
  },
];
