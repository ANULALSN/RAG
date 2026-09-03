import { Menu, MessageSquare, Moon, Sun } from "lucide-react";

interface MobileHeaderProps {
  theme: "light" | "dark";
  onToggleTheme: () => void;
  onOpenMenu: () => void;
}

export default function MobileHeader({
  theme,
  onToggleTheme,
  onOpenMenu,
}: MobileHeaderProps) {
  return (
    <header className="flex h-16 items-center justify-between border-b border-sz-border bg-sz-surface px-4 lg:hidden">
      <button
        onClick={onOpenMenu}
        aria-label="Open menu"
        className="rounded-lg p-2 text-sz-text-secondary hover:bg-sz-surface-secondary"
      >
        <Menu size={20} />
      </button>

      <div className="flex items-center gap-2">
        <div className="flex h-7 w-7 items-center justify-center rounded-md bg-sz-primary/10">
          <MessageSquare
            size={14}
            className="text-sz-primary"
          />
        </div>

        <span className="font-semibold">
          sub<span className="text-sz-primary">Zero</span>
        </span>
      </div>

      <button
        onClick={onToggleTheme}
        aria-label="Toggle theme"
        className="rounded-lg p-2 text-sz-text-secondary hover:bg-sz-surface-secondary"
      >
        {theme === "dark" ? (
          <Sun size={18} />
        ) : (
          <Moon size={18} />
        )}
      </button>
    </header>
  );
}