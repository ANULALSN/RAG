import {
  ArrowRight,
  BookOpen,
  Brain,
  FileQuestion,
  MessageSquare,
  Target,
  TrendingUp,
} from "lucide-react";
import { useParams } from "react-router-dom";
import { subjects } from "../data/subjects";
import { Link } from "react-router-dom";

interface StatCardProps {
  label: string;
  value: string;
  description: string;
  icon: React.ReactNode;
  accent?: "primary" | "blue" | "cyan" | "success" | "warning";
}

function StatCard({
  label,
  value,
  description,
  icon,
  accent = "primary",
}: StatCardProps) {
  const accentStyles = {
    primary:
      "bg-sz-primary/10 text-sz-primary",
    blue:
      "bg-sz-blue/10 text-sz-blue",
    cyan:
      "bg-sz-cyan/10 text-sz-cyan",
    success:
      "bg-sz-success/10 text-sz-success",
    warning:
      "bg-sz-warning/10 text-sz-warning",
  };

  return (
    <div className="rounded-xl border border-sz-border bg-sz-surface p-5 transition-colors hover:border-sz-border-strong">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-medium text-sz-text-muted">
            {label}
          </p>

          <p className="mt-2 text-2xl font-semibold tracking-tight">
            {value}
          </p>

          <p className="mt-1 text-xs text-sz-text-muted">
            {description}
          </p>
        </div>

        <div
          className={`flex h-9 w-9 items-center justify-center rounded-lg ${accentStyles[accent]}`}
        >
          {icon}
        </div>
      </div>
    </div>
  );
}

interface SectionHeaderProps {
  title: string;
  action?: string;
}

function SectionHeader({
  title,
  action,
}: SectionHeaderProps) {
  return (
    <div className="mb-4 flex items-center justify-between">
      <h2 className="text-base font-semibold">
        {title}
      </h2>

      {action && (
        <button className="text-xs font-medium text-sz-primary hover:text-sz-primary-hover">
          {action}
        </button>
      )}
    </div>
  );
}

export default function Subject() {
  const { subjectId } = useParams();

  const subject = subjects.find(
    (item) => item.id === Number(subjectId),
  );

  if (!subject) {
    return (
      <div className="flex min-h-full items-center justify-center p-6">
        <div className="text-center">
          <h1 className="text-xl font-semibold">
            Subject not found
          </h1>

          <p className="mt-2 text-sm text-sz-text-secondary">
            The subject you're looking for doesn't exist.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl p-6 lg:p-8">
      {/* Header */}
      <header>
        <div className="flex items-center gap-2 text-sm text-sz-text-muted">
          <BookOpen size={15} />
          <span>Subject</span>
        </div>

        <h1 className="mt-2 text-3xl font-semibold tracking-tight">
          {subject.name}
        </h1>

        <p className="mt-2 text-sm text-sz-text-secondary">
          Ask anything about your study materials.
        </p>
      </header>

      {/* Statistics */}
      <section className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="Materials"
          value="12"
          description="Total Documents"
          icon={<BookOpen size={18} />}
          accent="primary"
        />

        <StatCard
          label="Questions"
          value="48"
          description="In Question Bank"
          icon={<FileQuestion size={18} />}
          accent="blue"
        />

        <StatCard
          label="Quiz Score"
          value="78%"
          description="Average Score"
          icon={<TrendingUp size={18} />}
          accent="success"
        />

        <StatCard
          label="Weak Topics"
          value="3"
          description="Need Focus"
          icon={<Target size={18} />}
          accent="warning"
        />
      </section>

      {/* Continue Studying */}
      <section className="mt-10">
        <SectionHeader title="Continue Studying" />

        <Link
  to={`/subjects/${subject.id}/chat`}
  className="group block w-full rounded-xl border border-sz-border bg-sz-surface p-5 text-left transition hover:border-sz-primary/50"
>
          <div className="flex items-center gap-4">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-sz-primary/10 text-sz-primary">
              <MessageSquare size={19} />
            </div>

            <div className="min-w-0 flex-1">
              <p className="font-medium">
                Explain MapReduce
              </p>

              <p className="mt-1 text-sm text-sz-text-secondary">
                Continue your recent conversation
              </p>
            </div>

            <ArrowRight
              size={18}
              className="shrink-0 text-sz-text-muted transition group-hover:translate-x-1 group-hover:text-sz-primary"
            />
          </div>
        </Link>
      </section>

      {/* FAQ */}
      <section className="mt-10">
        <SectionHeader
          title="Frequently Asked Questions"
          action="View all"
        />

        <div className="grid gap-4 md:grid-cols-2">
          <QuestionCard
            question="What is Hadoop?"
            frequency="Asked frequently"
          />

          <QuestionCard
            question="What is HDFS?"
            frequency="Asked frequently"
          />

          <QuestionCard
            question="Explain MapReduce."
            frequency="Asked frequently"
          />

          <QuestionCard
            question="What are the characteristics of Big Data?"
            frequency="Asked frequently"
          />
        </div>
      </section>

      {/* Important Topics */}
      <section className="mt-10 pb-10">
        <SectionHeader
          title="Important Topics"
          action="View analysis"
        />

        <div className="rounded-xl border border-sz-border bg-sz-surface p-5">
          <TopicBar
            topic="Volume"
            frequency="Very Frequent"
            percentage={92}
          />

          <TopicBar
            topic="Velocity"
            frequency="Frequent"
            percentage={76}
          />

          <TopicBar
            topic="Hadoop"
            frequency="Frequent"
            percentage={68}
          />

          <TopicBar
            topic="MapReduce"
            frequency="Moderate"
            percentage={54}
          />
        </div>
      </section>
    </div>
  );
}

interface QuestionCardProps {
  question: string;
  frequency: string;
}

function QuestionCard({
  question,
  frequency,
}: QuestionCardProps) {
  return (
    <button className="group rounded-xl border border-sz-border bg-sz-surface p-5 text-left transition hover:border-sz-primary/40">
      <div className="flex items-start gap-3">
        <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-sz-primary/10 text-sz-primary">
          <Brain size={15} />
        </div>

        <div className="min-w-0">
          <p className="font-medium leading-6">
            {question}
          </p>

          <p className="mt-1 text-xs text-sz-text-muted">
            {frequency}
          </p>
        </div>

        <ArrowRight
          size={15}
          className="ml-auto mt-1 shrink-0 text-sz-text-muted opacity-0 transition group-hover:translate-x-1 group-hover:opacity-100"
        />
      </div>
    </button>
  );
}

interface TopicBarProps {
  topic: string;
  frequency: string;
  percentage: number;
}

function TopicBar({
  topic,
  frequency,
  percentage,
}: TopicBarProps) {
  return (
    <div className="py-3">
      <div className="mb-2 flex items-center justify-between gap-4">
        <span className="text-sm font-medium">
          {topic}
        </span>

        <span className="text-xs text-sz-text-muted">
          {frequency}
        </span>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-sz-surface-secondary">
        <div
          className="h-full rounded-full bg-sz-primary transition-all"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}