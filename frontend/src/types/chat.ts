import type { Source } from "../api/chat";

export interface ChatMessageData {
  id: string;
  chatId: string;
  role: "user" | "assistant";
  content: string;
  time: string;

  abstained?: boolean | null;
  relevance?: number | null;
  relevanceThreshold?: number | null;
  retrievedCount?: number | null;

  sources?: Source[];
}

export interface ChatSession {
  id: string;
  subjectId: string;
  title: string;
  createdAt: string;
  updatedAt: string;
}