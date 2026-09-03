import { FileText } from "lucide-react";
import type { Source } from "../../api/chat";

interface ChatSourcesProps {
  sources: Source[];
  relevance: number;
}

export default function ChatSources({
  sources,
  relevance,
}: ChatSourcesProps) {
  if (sources.length === 0) {
    return null;
  }

  return (
    <div className="mt-5 border-t border-sz-border pt-4">
      {/* Header */}
      <div className="mb-3 flex items-center justify-between">
        <span className="text-[11px] font-semibold uppercase tracking-wide text-sz-text-muted">
          Sources
        </span>

        <span className="text-[10px] text-sz-text-muted">
          {sources.length}{" "}
          {sources.length === 1 ? "source" : "sources"}
        </span>
      </div>

      {/* Source cards */}
      <div className="grid gap-2 sm:grid-cols-2">
        {sources.map((source) => (
          <button
            key={source.id}
            type="button"
            className="group rounded-lg border border-sz-border bg-sz-surface-secondary/50 p-3 text-left transition hover:border-sz-primary/40"
          >
            <div className="flex gap-3">
              {/* Icon */}
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-sz-primary/10 text-sz-primary">
                <FileText size={14} />
              </div>

              {/* Source information */}
              <div className="min-w-0">
                <p className="truncate text-xs font-medium text-sz-text-primary">
                  {source.document}
                </p>

                {source.title && (
                  <p className="mt-1 truncate text-[10px] text-sz-text-secondary">
                    {source.title}
                  </p>
                )}

                <p className="mt-1 text-[10px] text-sz-text-muted">
                  {source.module
                    ? `${source.module} · `
                    : ""}
                  Slide {source.slide}
                </p>
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* Retrieval relevance */}
      <div className="mt-4">
        <div className="mb-1.5 flex items-center justify-between">
          <span className="text-[10px] text-sz-text-muted">
            Retrieval relevance
          </span>

          <span className="text-[10px] font-medium text-sz-text-secondary">
            {Math.round(relevance * 100)}%
          </span>
        </div>

        <div className="h-1.5 overflow-hidden rounded-full bg-sz-surface-secondary">
          <div
            className="h-full rounded-full bg-sz-primary transition-all duration-500"
            style={{
              width: `${Math.min(
                Math.max(relevance * 100, 0),
                100,
              )}%`,
            }}
          />
        </div>
      </div>
    </div>
  );
}