import { ArrowRight, BookOpen } from "lucide-react";
import { Link } from "react-router-dom";
import { subjects } from "../data/subjects";

export default function Home() {
  return (
    <div className="mx-auto max-w-6xl p-6 lg:p-8">
      <div className="max-w-2xl">
        <p className="text-sm font-medium text-sz-primary">
          Welcome to subZero
        </p>

        <h1 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">
          What are you studying?
        </h1>

        <p className="mt-3 text-sm leading-6 text-sz-text-secondary">
          Choose a subject to continue studying with your
          course materials.
        </p>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {subjects.map((subject) => (
          <Link
            key={subject.id}
            to={`/subjects/${subject.id}`}
            className="group rounded-xl border border-sz-border bg-sz-surface p-5 transition duration-200 hover:-translate-y-0.5 hover:border-sz-primary/50 hover:shadow-[var(--sz-shadow)]"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-sz-primary/10 text-sm font-semibold text-sz-primary">
              {subject.shortName}
            </div>

            <h2 className="mt-5 font-semibold">
              {subject.name}
            </h2>

            <div className="mt-4 flex items-center gap-1 text-xs font-medium text-sz-primary opacity-0 transition group-hover:opacity-100">
              Open subject
              <ArrowRight size={13} />
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}