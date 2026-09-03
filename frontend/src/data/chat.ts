export interface ChatMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  time: string;
}

export const mockMessages: ChatMessage[] = [
  {
    id: 1,
    role: "user",
    content:
      "Explain MapReduce in simple terms.",
    time: "10:30 AM",
  },
  {
    id: 2,
    role: "assistant",
    content:
      "MapReduce is a programming model and processing technique used for handling large datasets in a distributed environment.\n\nIt works using two main functions:\n\n1. Map — Processes input data and generates intermediate key-value pairs.\n2. Reduce — Combines the intermediate values associated with the same key.\n\nIn simple terms, Map breaks the large problem into smaller pieces, while Reduce combines the results.",
    time: "10:30 AM",
  },
];
export const mockSources = [
  {
    id: 1,
    document: "Hadoop Fundamentals",
    module: "Module 2",
    location: "Slide 14",
    relevance: 0.84,
  },
  {
    id: 2,
    document: "Big Data Concepts",
    module: "Module 1",
    location: "Slide 8",
    relevance: 0.79,
  },
];