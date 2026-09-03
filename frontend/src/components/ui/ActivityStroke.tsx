import type { ReactNode } from "react";

interface ActivityStrokeProps {
  active: boolean;
  children: ReactNode;
  className?: string;
}

export default function ActivityStroke({
  active,
  children,
  className = "",
}: ActivityStrokeProps) {
  if (!active) {
    return <div className={className}>{children}</div>;
  }

  return (
    <div
      className={`sz-activity w-fit max-w-3xl ${className}`}
    >
      <div className="sz-activity-inner">
        {children}
      </div>
    </div>
  );
}