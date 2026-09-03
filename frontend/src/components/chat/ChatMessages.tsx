import { Bot, User } from "lucide-react";


interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  time: string;
  isThinking?: boolean;
}

export default function ChatMessage({
  role,
  content,
  time,
  isThinking = false,
}: ChatMessageProps)  {
  const isUser = role === "user";

  return (
    <div
      className={`flex gap-3 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {!isUser && !isThinking && (
  <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-sz-primary/30 bg-sz-primary/10 text-sz-primary">
    <Bot size={16} />
  </div>
)}

      <div
        className={`max-w-3xl ${
          isUser ? "items-end" : "items-start"
        }`}
      >
        <div
          className={
            isUser
              ? "rounded-2xl rounded-br-md bg-sz-primary px-4 py-3 text-sm leading-6 text-white"
              : "rounded-2xl rounded-bl-md bg-sz-surface px-4 py-4 text-sm leading-6 text-sz-text-primary"
          }
        >
          <p className="whitespace-pre-line">
            {content}
          </p>
        </div>

        <div
          className={`mt-1.5 flex items-center gap-2 text-[10px] text-sz-text-muted ${
            isUser ? "justify-end" : "justify-start"
          }`}
        >
          {isUser && <User size={11} />}
          <span>{time}</span>
        </div>
      </div>

      {isUser && (
        <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-sz-surface-secondary text-sz-text-secondary">
          <User size={15} />
        </div>
      )}
    </div>
  );
}