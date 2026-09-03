import {
  BarChart3,
  BookOpen,
  MessageSquare,
  MoreHorizontal,
} from "lucide-react";

export default function MobileBottomNav() {
  return (
    <nav className="fixed inset-x-0 bottom-0 z-40 flex h-16 border-t border-sz-border bg-sz-surface/95 backdrop-blur lg:hidden">
      <button className="flex flex-1 flex-col items-center justify-center gap-1 text-sz-primary">
        <MessageSquare size={19} />
        <span className="text-[10px] font-medium">
          Chat
        </span>
      </button>

      <button className="flex flex-1 flex-col items-center justify-center gap-1 text-sz-text-muted">
        <BookOpen size={19} />
        <span className="text-[10px]">
          Materials
        </span>
      </button>

      <button className="flex flex-1 flex-col items-center justify-center gap-1 text-sz-text-muted">
        <BarChart3 size={19} />
        <span className="text-[10px]">
          Progress
        </span>
      </button>

      <button className="flex flex-1 flex-col items-center justify-center gap-1 text-sz-text-muted">
        <MoreHorizontal size={19} />
        <span className="text-[10px]">
          More
        </span>
      </button>
    </nav>
  );
}