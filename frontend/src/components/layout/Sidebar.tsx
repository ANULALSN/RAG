import {
  BarChart3,
  BookOpen,
  Brain,
  ChevronRight,
  FileQuestion,
  LayoutDashboard,
  MessageSquare,
  Plus,
  Settings,
  LogOut,
} from "lucide-react";
import { NavLink } from "react-router-dom";
import { subjects } from "../../data/subjects";



export default function Sidebar() {
  return (
    <aside className="hidden h-screen w-64 shrink-0 flex-col border-r border-sz-border bg-sz-surface lg:flex">
      {/* Brand */}
      <div className="flex h-16 items-center px-5">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg border border-sz-primary/40 bg-sz-primary/10">
            <MessageSquare
              size={16}
              className="text-sz-primary"
            />
          </div>

          <span className="text-lg font-semibold tracking-tight">
            sub<span className="text-sz-primary">Zero</span>
          </span>
        </div>
      </div>

      {/* New Chat */}
      <div className="px-4 pt-2">
        <button className="flex w-full items-center justify-center gap-2 rounded-lg bg-sz-primary px-4 py-2.5 text-sm font-medium text-white transition hover:bg-sz-primary-hover">
          <Plus size={17} />
          New Chat
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 py-6">
        {/* Subjects */}
        <div>
          <p className="px-2 text-[11px] font-semibold uppercase tracking-wider text-sz-text-muted">
            Subjects
          </p>

          <div className="mt-2 space-y-1">
  {subjects.map((subject) => (
    <NavLink
      key={subject.id}
      to={`/subjects/${subject.id}`}
      className={({ isActive }) =>
        `group flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm transition ${
          isActive
            ? "bg-sz-primary/10 text-sz-primary"
            : "text-sz-text-secondary hover:bg-sz-surface-secondary hover:text-sz-text-primary"
        }`
      }
    >
      <BookOpen size={16} />

      <span className="flex-1 truncate">
        {subject.name}
      </span>

      <ChevronRight
        size={14}
        className="opacity-0 transition group-hover:opacity-60"
      />
    </NavLink>
  ))}

  <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-sz-primary transition hover:bg-sz-primary/10">
    <Plus size={16} />
    Add Subject
  </button>
</div>
        </div>

        {/* Study */}
        <div className="mt-7 border-t border-sz-border pt-6">
          <div className="space-y-1">
            <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-sz-text-secondary transition hover:bg-sz-surface-secondary hover:text-sz-text-primary">
              <FileQuestion size={16} />
              Question Papers
            </button>

            <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-sz-text-secondary transition hover:bg-sz-surface-secondary hover:text-sz-text-primary">
              <Brain size={16} />
              Exam Intelligence
            </button>

            <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-sz-text-secondary transition hover:bg-sz-surface-secondary hover:text-sz-text-primary">
              <BarChart3 size={16} />
              Progress
            </button>
          </div>
        </div>
      </nav>

      {/* Bottom */}
      <div className="border-t border-sz-border p-3">
        <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-sz-text-secondary transition hover:bg-sz-surface-secondary hover:text-sz-text-primary">
          <Settings size={17} />
          Settings
        </button>

        <button className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-sz-text-secondary transition hover:bg-sz-surface-secondary hover:text-sz-text-primary">
          <LogOut size={17} />
          Logout
        </button>
      </div>
    </aside>
  );
}