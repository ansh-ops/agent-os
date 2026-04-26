import { ProviderStatus } from "@/types";

const MODE_STYLES: Record<ProviderStatus["mode"], string> = {
  mock: "bg-stone-100 text-stone-700 border-stone-200",
  llm_active: "bg-emerald-100 text-emerald-800 border-emerald-200",
  llm_misconfigured: "bg-rose-100 text-rose-800 border-rose-200",
};

const MODE_LABELS: Record<ProviderStatus["mode"], string> = {
  mock: "Mock Mode",
  llm_active: "LLM Active",
  llm_misconfigured: "LLM Misconfigured",
};

export function ProviderStatusBadge({ status }: { status: ProviderStatus | null }) {
  if (!status) {
    return (
      <div className="max-w-full rounded-[24px] border border-line bg-white px-5 py-4 text-sm text-stone-700">
        Checking provider...
      </div>
    );
  }

  return (
    <div className={`max-w-full rounded-[24px] border px-5 py-4 text-sm ${MODE_STYLES[status.mode]}`}>
      <p className="break-words font-semibold">{MODE_LABELS[status.mode]}</p>
      <p className="mt-1 break-words text-xs uppercase tracking-[0.14em]">{status.provider_name}</p>
      {status.last_error ? <p className="mt-2 max-w-64 break-words text-xs normal-case tracking-normal">{status.last_error}</p> : null}
    </div>
  );
}
