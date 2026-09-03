const API_BASE_URL = "http://127.0.0.1:8000";

/* =========================================================
   Sources
   ========================================================= */

export interface Source {
  id: number;
  document: string;
  slide: number | string;
  subject: string | null;
  module: string | null;
  title: string | null;
}

/* =========================================================
   Existing RAG /ask types
   ========================================================= */

export interface QuestionRequest {
  question: string;
}

export interface QuestionResponse {
  question: string;
  answer: string;
  abstained: boolean;
  best_score: number;
  sources: Source[];
}

/* =========================================================
   Chat Session
   ========================================================= */

export interface ChatResponse {
  id: string;
  subject_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

/* =========================================================
   Chat Message
   ========================================================= */

export interface ChatMessageResponse {
  id: string;
  chat_id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;

  abstained: boolean | null;
  best_score: number | null;
  relevance_threshold: number | null;
  retrieved_count: number | null;

  sources: Source[];
}

/* =========================================================
   Create Chat
   ========================================================= */

export async function createChat(
  subjectId: string,
  title = "New Chat",
): Promise<ChatResponse> {
  const response = await fetch(
    `${API_BASE_URL}/subjects/${encodeURIComponent(
      subjectId,
    )}/chats`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        title,
      }),
    },
  );

  if (!response.ok) {
    let message = "Failed to create chat.";

    try {
      const error = await response.json();

      if (error?.detail) {
        message = error.detail;
      }
    } catch {
      // Keep default message.
    }

    throw new Error(message);
  }

  return response.json();
}

/* =========================================================
   Get Chats For Subject
   ========================================================= */

export async function getChats(
  subjectId: string,
): Promise<ChatResponse[]> {
  const response = await fetch(
    `${API_BASE_URL}/subjects/${encodeURIComponent(
      subjectId,
    )}/chats`,
  );

  if (!response.ok) {
    let message = "Failed to load chats.";

    try {
      const error = await response.json();

      if (error?.detail) {
        message = error.detail;
      }
    } catch {
      // Keep default message.
    }

    throw new Error(message);
  }

  return response.json();
}

/* =========================================================
   Get Specific Chat
   ========================================================= */

export async function getChat(
  chatId: string,
): Promise<ChatResponse> {
  const response = await fetch(
    `${API_BASE_URL}/chats/${encodeURIComponent(
      chatId,
    )}`,
  );

  if (!response.ok) {
    let message = "Failed to load chat.";

    try {
      const error = await response.json();

      if (error?.detail) {
        message = error.detail;
      }
    } catch {
      // Keep default message.
    }

    throw new Error(message);
  }

  return response.json();
}

/* =========================================================
   Delete Chat
   ========================================================= */

export async function deleteChat(
  chatId: string,
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/chats/${encodeURIComponent(
      chatId,
    )}`,
    {
      method: "DELETE",
    },
  );

  if (!response.ok) {
    let message = "Failed to delete chat.";

    try {
      const error = await response.json();

      if (error?.detail) {
        message = error.detail;
      }
    } catch {
      // Keep default message.
    }

    throw new Error(message);
  }
}

/* =========================================================
   Get Chat Messages
   ========================================================= */

export async function getChatMessages(
  chatId: string,
): Promise<ChatMessageResponse[]> {
  const response = await fetch(
    `${API_BASE_URL}/chats/${encodeURIComponent(
      chatId,
    )}/messages`,
  );

  if (!response.ok) {
    let message = "Failed to load chat messages.";

    try {
      const error = await response.json();

      if (error?.detail) {
        message = error.detail;
      }
    } catch {
      // Keep default message.
    }

    throw new Error(message);
  }

  return response.json();
}

/* =========================================================
   Send Chat Message
   ========================================================= */

export async function sendChatMessage(
  chatId: string,
  content: string,
): Promise<ChatMessageResponse[]> {
  const response = await fetch(
    `${API_BASE_URL}/chats/${encodeURIComponent(
      chatId,
    )}/messages`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        content,
      }),
    },
  );

  if (!response.ok) {
    let message = "Failed to send message.";

    try {
      const error = await response.json();

      if (error?.detail) {
        message = error.detail;
      }
    } catch {
      // Keep default message.
    }

    throw new Error(message);
  }

  return response.json();
}

/* =========================================================
   Existing /ask
   ========================================================= */

export async function askQuestion(
  question: string,
): Promise<QuestionResponse> {
  const response = await fetch(
    `${API_BASE_URL}/ask`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        question,
      }),
    },
  );

  if (!response.ok) {
    let message = "Failed to get a response.";

    try {
      const error = await response.json();

      if (error?.detail) {
        message = error.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.json();
}