import { useEffect, useRef, useState } from "react";
import {
  MessageSquare,
  MoreHorizontal,
  Plus,
} from "lucide-react";
import { useParams } from "react-router-dom";

import { subjects } from "../data/subjects";

import {
  createChat,
  deleteChat,
  getChatMessages,
  getChats,
  sendChatMessage,
  type ChatMessageResponse,
} from "../api/chat";

import ChatMessage from "../components/chat/ChatMessages";
import ChatSources from "../components/chat/ChatSources";
import ActivityStroke from "../components/ui/ActivityStroke";

import type {
  ChatMessageData,
  ChatSession,
} from "../types/chat";

export default function Chat() {
  const { subjectId } = useParams();

  // =========================================================
  // State
  // =========================================================

  const [input, setInput] = useState("");

  const [chatSessions, setChatSessions] = useState<
    ChatSession[]
  >([]);

  const [activeChatId, setActiveChatId] =
    useState<string | null>(null);

  const [messages, setMessages] = useState<
    ChatMessageData[]
  >([]);

  const [isGenerating, setIsGenerating] =
    useState(false);

  const [isLoadingChats, setIsLoadingChats] =
    useState(true);

  const [isLoadingMessages, setIsLoadingMessages] =
    useState(false);

  const [error, setError] = useState<string | null>(
    null,
  );

  // =========================================================
  // Refs
  // =========================================================

  const messagesEndRef =
    useRef<HTMLDivElement | null>(null);

  /*
   * Tracks the chat for which the current
   * generation request was started.
   *
   * This prevents a response from Chat A
   * being rendered inside Chat B.
   */
  const generatingChatIdRef =
    useRef<string | null>(null);

  /*
   * Tracks the latest message-loading request.
   *
   * If the user switches quickly between chats,
   * an older GET request must not overwrite
   * the newer chat's messages.
   */
  const messageLoadRequestRef =
    useRef(0);

  // =========================================================
  // Subject
  // =========================================================

  const subject = subjects.find(
    (item) => item.id === Number(subjectId),
  );

  /*
   * Frontend uses numeric subject IDs.
   *
   * Backend currently uses slugs.
   */
  const backendSubjectId =
    subject?.shortName === "BD"
      ? "big-data"
      : subject?.shortName === "DB"
        ? "dbms"
        : subject?.shortName === "CN"
          ? "computer-networks"
          : subject?.shortName === "OS"
            ? "operating-systems"
            : null;

  // =========================================================
  // Backend message → frontend message
  // =========================================================

  const mapBackendMessage = (
    message: ChatMessageResponse,
  ): ChatMessageData => {
    return {
      id: message.id,
      chatId: message.chat_id,

      role: message.role,

      content: message.content,

      time: new Date(
        message.created_at,
      ).toLocaleTimeString([], {
        hour: "numeric",
        minute: "2-digit",
      }),

      abstained: message.abstained,

      relevance: message.best_score,

      relevanceThreshold:
        message.relevance_threshold,

      retrievedCount:
        message.retrieved_count,

      sources: message.sources ?? [],
    };
  };

  // =========================================================
  // Load chats when subject changes
  // =========================================================

  useEffect(() => {
    if (!backendSubjectId) {
      return;
    }

    let cancelled = false;

    const loadChats = async () => {
      setIsLoadingChats(true);
      setError(null);

      try {
        const backendChats =
          await getChats(backendSubjectId);

        if (cancelled) {
          return;
        }

        const mappedChats: ChatSession[] =
          backendChats.map((chat) => ({
            id: chat.id,
            subjectId: chat.subject_id,
            title: chat.title,
            createdAt: chat.created_at,
            updatedAt: chat.updated_at,
          }));

        setChatSessions(mappedChats);

        if (mappedChats.length > 0) {
          const sortedChats = [
            ...mappedChats,
          ].sort(
            (a, b) =>
              new Date(
                b.updatedAt,
              ).getTime() -
              new Date(
                a.updatedAt,
              ).getTime(),
          );

          setActiveChatId(
            sortedChats[0].id,
          );
        } else {
          setActiveChatId(null);
        }

        setMessages([]);
        setInput("");
      } catch (err) {
        if (cancelled) {
          return;
        }

        setError(
          err instanceof Error
            ? err.message
            : "Failed to load chats.",
        );

        setChatSessions([]);
        setActiveChatId(null);
        setMessages([]);
      } finally {
        if (!cancelled) {
          setIsLoadingChats(false);
        }
      }
    };

    loadChats();

    return () => {
      cancelled = true;
    };
  }, [backendSubjectId]);

  // =========================================================
  // Load messages whenever active chat changes
  // =========================================================

  useEffect(() => {
    if (!activeChatId) {
      setMessages([]);
      setIsLoadingMessages(false);
      return;
    }

    const requestId =
      ++messageLoadRequestRef.current;

    let cancelled = false;

    const loadMessages = async () => {
      setIsLoadingMessages(true);
      setError(null);

      try {
        const backendMessages =
          await getChatMessages(
            activeChatId,
          );

        /*
         * Ignore this response if:
         *
         * - the effect was cancelled
         * - another chat-load request started later
         * - active chat has changed
         */
        if (
          cancelled ||
          requestId !==
            messageLoadRequestRef.current
        ) {
          return;
        }

        const mappedMessages =
          backendMessages.map(
            mapBackendMessage,
          );

        setMessages(mappedMessages);
      } catch (err) {
        if (
          cancelled ||
          requestId !==
            messageLoadRequestRef.current
        ) {
          return;
        }

        setMessages([]);

        setError(
          err instanceof Error
            ? err.message
            : "Failed to load messages.",
        );
      } finally {
        if (
          !cancelled &&
          requestId ===
            messageLoadRequestRef.current
        ) {
          setIsLoadingMessages(false);
        }
      }
    };

    loadMessages();

    return () => {
      cancelled = true;
    };
  }, [activeChatId]);

  // =========================================================
  // Auto-scroll
  // =========================================================

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [
    messages,
    isGenerating,
  ]);

  // =========================================================
  // New Chat
  // =========================================================

  const handleNewChat = async () => {
    if (
      isGenerating ||
      !backendSubjectId
    ) {
      return;
    }

    setError(null);

    try {
      const newChat =
        await createChat(
          backendSubjectId,
          "New Chat",
        );

      const mappedChat: ChatSession = {
        id: newChat.id,
        subjectId:
          newChat.subject_id,
        title: newChat.title,
        createdAt:
          newChat.created_at,
        updatedAt:
          newChat.updated_at,
      };

      setChatSessions(
        (current) => [
          mappedChat,
          ...current,
        ],
      );

      setActiveChatId(
        mappedChat.id,
      );

      setMessages([]);
      setInput("");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to create a new chat.",
      );
    }
  };

  // =========================================================
  // Select existing chat
  // =========================================================

  const handleSelectChat = (
    chatId: string,
  ) => {
    if (
      chatId === activeChatId
    ) {
      return;
    }

    /*
     * We intentionally allow switching
     * while another chat is generating.
     *
     * The active request remains associated
     * with its original chat through
     * generatingChatIdRef.
     */

    setActiveChatId(chatId);

    setMessages([]);

    setInput("");

    setError(null);
  };

  // =========================================================
  // Delete Chat
  // =========================================================

  const handleDeleteChat = async () => {
    if (
      !activeChatId ||
      isGenerating
    ) {
      return;
    }

    const chatIdToDelete =
      activeChatId;

    try {
      await deleteChat(
        chatIdToDelete,
      );

      const remainingChats =
        chatSessions.filter(
          (chat) =>
            chat.id !==
            chatIdToDelete,
        );

      setChatSessions(
        remainingChats,
      );

      if (
        remainingChats.length > 0
      ) {
        const nextChat =
          [...remainingChats].sort(
            (a, b) =>
              new Date(
                b.updatedAt,
              ).getTime() -
              new Date(
                a.updatedAt,
              ).getTime(),
          )[0];

        setActiveChatId(
          nextChat.id,
        );
      } else {
        setActiveChatId(null);
      }

      setMessages([]);
      setInput("");
      setError(null);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to delete chat.",
      );
    }
  };

  // =========================================================
  // Send Question
  // =========================================================

  const handleSend = async () => {
    const question =
      input.trim();

    const chatId =
      activeChatId;

    if (
      !question ||
      isGenerating ||
      !chatId
    ) {
      return;
    }

    setError(null);

    /*
     * IMPORTANT:
     *
     * Capture the chat ID at the exact
     * moment the request starts.
     *
     * Even if the user switches chats later,
     * this request still belongs to this chat.
     */
    generatingChatIdRef.current =
      chatId;

    // =======================================================
    // Temporary user message
    // =======================================================

    const temporaryUserMessage:
      ChatMessageData = {
        id: `temp-user-${Date.now()}`,
        chatId,
        role: "user",
        content: question,

        time: new Date().toLocaleTimeString(
          [],
          {
            hour: "numeric",
            minute: "2-digit",
          },
        ),
      };

    // =======================================================
    // Temporary thinking message
    // =======================================================

    const thinkingMessage:
      ChatMessageData = {
        id: `temp-thinking-${Date.now()}`,
        chatId,

        role: "assistant",

        content: "Thinking…",

        time: "",

        sources: [],

        relevance: 0,
      };

    /*
     * Only show the temporary messages
     * if the chat is still active.
     */
    setMessages(
      (current) => [
        ...current,
        temporaryUserMessage,
        thinkingMessage,
      ],
    );

    setInput("");

    setIsGenerating(true);

    try {
      // =====================================================
      // Send to backend
      // =====================================================

      const result =
        await sendChatMessage(
          chatId,
          question,
        );

      /*
       * CRITICAL:
       *
       * If the user switched to another chat
       * while the backend was generating,
       * DO NOT replace that chat's messages.
       */
      if (
        generatingChatIdRef.current !==
        chatId
      ) {
        return;
      }

      if (
        activeChatId !== chatId
      ) {
        return;
      }

      // =====================================================
      // Replace temporary messages
      // with persisted backend messages
      // =====================================================

      const persistedMessages =
        result.map(
          mapBackendMessage,
        );

      setMessages(
        persistedMessages,
      );

      // =====================================================
      // Refresh sidebar metadata
      // =====================================================

      if (backendSubjectId) {
        const latestChats =
          await getChats(
            backendSubjectId,
          );

        /*
         * User may have changed subject
         * or chat while this request was
         * completing.
         *
         * Only update the sidebar if
         * we're still on the same subject.
         */
        if (
          generatingChatIdRef.current !==
          chatId
        ) {
          return;
        }

        const mappedChats =
          latestChats.map(
            (chat) => ({
              id: chat.id,
              subjectId:
                chat.subject_id,
              title:
                chat.title,
              createdAt:
                chat.created_at,
              updatedAt:
                chat.updated_at,
            }),
          );

        setChatSessions(
          mappedChats,
        );
      }
    } catch (err) {
      /*
       * Only modify visible messages if
       * the failed request still belongs
       * to the currently selected chat.
       */
      if (
        generatingChatIdRef.current ===
          chatId &&
        activeChatId === chatId
      ) {
        setMessages(
          (current) =>
            current.filter(
              (message) =>
                message.id !==
                  temporaryUserMessage.id &&
                message.id !==
                  thinkingMessage.id,
            ),
        );

        setError(
          err instanceof Error
            ? err.message
            : "Something went wrong while asking subZero.",
        );
      }
    } finally {
      /*
       * Only clear the global generation
       * state if this is still the request
       * that owns it.
       */
      if (
        generatingChatIdRef.current ===
        chatId
      ) {
        generatingChatIdRef.current =
          null;

        setIsGenerating(false);
      }
    }
  };

  // =========================================================
  // Invalid Subject
  // =========================================================

  if (!subject) {
    return (
      <div className="flex min-h-full items-center justify-center p-6">
        <div className="text-center">

          <h1 className="text-xl font-semibold">
            Subject not found
          </h1>

          <p className="mt-2 text-sm text-sz-text-secondary">
            The subject you're looking for doesn't
            exist.
          </p>

        </div>
      </div>
    );
  }

  // =========================================================
  // UI
  // =========================================================

  return (
    <div className="flex h-[calc(100vh-4rem)] min-h-0 flex-col lg:h-screen">

      {/* =====================================================
          Header
          ===================================================== */}

      <header className="flex h-16 shrink-0 items-center justify-between border-b border-sz-border px-5 lg:px-7">

        <div className="min-w-0">

          <div className="flex items-center gap-2">

            <h1 className="truncate text-lg font-semibold">
              {subject.name}
            </h1>

            <span className="rounded-md bg-sz-primary/10 px-2 py-1 text-[11px] font-medium text-sz-primary">
              Study
            </span>

          </div>

          <p className="mt-0.5 hidden text-xs text-sz-text-muted sm:block">
            Ask anything about your study materials
          </p>

        </div>

        <div className="flex items-center gap-2">

          {/* New Chat */}

          <button
            type="button"
            onClick={handleNewChat}
            disabled={
              isLoadingChats
            }
            className="hidden items-center gap-2 rounded-lg bg-sz-primary px-3 py-2 text-xs font-medium text-white transition hover:bg-sz-primary-hover disabled:cursor-not-allowed disabled:opacity-50 sm:flex"
          >
            <Plus size={15} />
            New Chat
          </button>

          {/* Delete Chat */}

          <button
            type="button"
            aria-label="Delete chat"
            onClick={
              handleDeleteChat
            }
            disabled={
              !activeChatId ||
              isGenerating
            }
            className="rounded-lg p-2 text-sz-text-muted transition hover:bg-sz-surface-secondary hover:text-sz-text-primary disabled:opacity-40"
          >
            <MoreHorizontal size={19} />
          </button>

        </div>

      </header>

      {/* =====================================================
          Chat Body
          ===================================================== */}

      <div className="flex min-h-0 flex-1">

        {/* ===================================================
            Sidebar
            =================================================== */}

        <aside className="hidden w-64 shrink-0 border-r border-sz-border bg-sz-surface-secondary/40 lg:block">

          <div className="flex items-center justify-between border-b border-sz-border px-4 py-3">

            <span className="text-xs font-semibold text-sz-text-muted">
              Chats
            </span>

            <button
              type="button"
              aria-label="New chat"
              onClick={
                handleNewChat
              }
              disabled={
                isLoadingChats
              }
              className="rounded-md p-1.5 text-sz-text-muted transition hover:bg-sz-surface-secondary hover:text-sz-text-primary disabled:opacity-40"
            >
              <Plus size={15} />
            </button>

          </div>

          <div className="space-y-1 overflow-y-auto p-2">

            {isLoadingChats ? (

              <div className="px-3 py-4 text-center text-xs text-sz-text-muted">
                Loading chats…
              </div>

            ) : (

              chatSessions.map(
                (chat) => {

                  const isActive =
                    chat.id ===
                    activeChatId;

                  return (
                    <button
                      key={chat.id}
                      type="button"
                      onClick={() =>
                        handleSelectChat(
                          chat.id,
                        )
                      }
                      className={`w-full rounded-lg px-3 py-2.5 text-left transition ${
                        isActive
                          ? "bg-sz-primary/10"
                          : "hover:bg-sz-surface-secondary"
                      }`}
                    >

                      <p
                        className={`truncate text-xs ${
                          isActive
                            ? "font-medium text-sz-text-primary"
                            : "text-sz-text-secondary"
                        }`}
                      >
                        {chat.title}
                      </p>

                      <p className="mt-1 text-[11px] text-sz-text-muted">
                        {new Date(
                          chat.updatedAt,
                        ).toLocaleDateString(
                          [],
                          {
                            month:
                              "short",
                            day: "numeric",
                          },
                        )}
                      </p>

                    </button>
                  );
                },
              )
            )}

            {!isLoadingChats &&
              chatSessions.length ===
                0 && (
                <div className="px-3 py-4 text-center text-xs text-sz-text-muted">
                  No chats yet.
                </div>
              )}

          </div>

        </aside>

        {/* ===================================================
            Main Chat
            =================================================== */}

        <section className="flex min-w-0 flex-1 flex-col">

          {/* Messages */}

          <div className="min-h-0 flex-1 overflow-y-auto">

            <div className="mx-auto flex min-h-full max-w-4xl flex-col gap-5 px-5 py-8 lg:px-8">

              {isLoadingMessages ? (

                <div className="flex flex-1 items-center justify-center">

                  <div className="text-sm text-sz-text-muted">
                    Loading conversation…
                  </div>

                </div>

              ) : messages.length === 0 ? (

                <div className="flex min-h-full flex-1 items-center justify-center">

                  <div className="max-w-md px-6 text-center">

                    <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl border border-sz-border bg-sz-surface text-sz-primary">
                      <MessageSquare size={21} />
                    </div>

                    <h2 className="mt-5 text-lg font-semibold">
                      Study with subZero
                    </h2>

                    <p className="mt-2 text-sm leading-6 text-sz-text-secondary">
                      Ask questions about your{" "}
                      {subject.name} course
                      materials and get grounded
                      answers with sources.
                    </p>

                  </div>

                </div>

              ) : (

                messages.map(
                  (message) => {

                    const isAssistant =
                      message.role ===
                      "assistant";

                    const isCurrentThinking =
                      isAssistant &&
                      isGenerating &&
                      message.id ===
                        messages[
                          messages.length -
                            1
                        ]?.id &&
                      message.chatId ===
                        generatingChatIdRef.current;

                    return (
                      <div
                        key={message.id}
                      >

                        <ActivityStroke
                          active={
                            isCurrentThinking
                          }
                          className="max-w-3xl"
                        >

                          <ChatMessage
                            role={
                              message.role
                            }
                            content={
                              message.content
                            }
                            time={
                              message.time
                            }
                            isThinking={
                              isCurrentThinking
                            }
                          />

                        </ActivityStroke>

                        {isAssistant &&
                          message.sources &&
                          message.sources.length >
                            0 && (

                            <div className="ml-11 max-w-3xl">

                              <ChatSources
                                sources={
                                  message.sources
                                }
                                relevance={
                                  message.relevance ??
                                  0
                                }
                              />

                            </div>

                          )}

                      </div>
                    );
                  },
                )

              )}

              <div
                ref={
                  messagesEndRef
                }
              />

              {error && (
                <div className="max-w-3xl rounded-xl border border-red-500/20 bg-red-500/5 px-4 py-3 text-sm text-red-500">
                  {error}
                </div>
              )}

            </div>

          </div>

          {/* =================================================
              Input
              ================================================= */}

          <div className="border-t border-sz-border p-4">

            <div className="mx-auto flex max-w-4xl items-center gap-2 rounded-xl border border-sz-border bg-sz-surface px-4 py-2.5 transition focus-within:border-sz-primary/60">

              <textarea
                rows={1}
                value={input}
                onChange={(event) =>
                  setInput(
                    event.target.value,
                  )
                }
                onKeyDown={(event) => {
                  if (
                    event.key ===
                      "Enter" &&
                    !event.shiftKey
                  ) {
                    event.preventDefault();
                    handleSend();
                  }
                }}
                placeholder="Ask anything..."
                disabled={
                  isLoadingMessages
                }
                className="min-h-8 max-h-32 min-w-0 flex-1 resize-none bg-transparent py-1 text-sm leading-6 text-sz-text-primary outline-none placeholder:text-sz-text-muted disabled:opacity-60"
              />

              <button
                type="button"
                aria-label="Send message"
                onClick={
                  handleSend
                }
                disabled={
                  !input.trim() ||
                  isGenerating ||
                  isLoadingMessages ||
                  !activeChatId
                }
                className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-sz-primary text-white transition hover:bg-sz-primary-hover disabled:cursor-not-allowed disabled:opacity-40"
              >
                →
              </button>

            </div>

            <p className="mx-auto mt-2 max-w-4xl text-center text-[10px] text-sz-text-muted">
              Answers are grounded in your uploaded
              course material.
            </p>

          </div>

        </section>

      </div>

    </div>
  );
}