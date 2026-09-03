import { useState } from "react";
import Sidebar from "./Sidebar";
import MobileHeader from "./MobileHeader";
import MobileBottomNav from "./MobileBottomNav";

interface AppShellProps {
  children: React.ReactNode;
  theme: "light" | "dark";
  onToggleTheme: () => void;
}

export default function AppShell({
  children,
  theme,
  onToggleTheme,
}: AppShellProps) {
  const [mobileMenuOpen, setMobileMenuOpen] =
    useState(false);

  return (
    <div className="min-h-screen bg-sz-background text-sz-text-primary">
      <div className="flex min-h-screen">
        <Sidebar />

        <div className="flex min-w-0 flex-1 flex-col">
          <MobileHeader
            theme={theme}
            onToggleTheme={onToggleTheme}
            onOpenMenu={() => setMobileMenuOpen(true)}
          />

          <main className="min-w-0 flex-1 pb-16 lg:pb-0">
            {children}
          </main>
        </div>
      </div>

      <MobileBottomNav />

      {/* Temporary mobile menu */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div
            className="absolute inset-0 bg-black/50"
            onClick={() => setMobileMenuOpen(false)}
          />

          <div className="relative h-full w-72 border-r border-sz-border bg-sz-surface p-5">
            <div className="flex items-center justify-between">
              <span className="font-semibold">
                sub<span className="text-sz-primary">
                  Zero
                </span>
              </span>

              <button
                onClick={() => setMobileMenuOpen(false)}
                className="text-sz-text-muted"
              >
                ✕
              </button>
            </div>

            <div className="mt-8 text-sm text-sz-text-secondary">
              Subject navigation will appear here.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}