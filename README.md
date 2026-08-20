# MSc RAG

### Local, Grounded Retrieval-Augmented Generation for MSc Computer Science Course Materials

MSc RAG is a local Retrieval-Augmented Generation (RAG) system designed to answer academic questions using **course materials as the sole knowledge source**.

The system processes lecture PowerPoint files, extracts and chunks their content, generates semantic embeddings, stores them in a local Qdrant vector database, retrieves relevant course material, filters irrelevant context, and generates grounded answers using a locally hosted **Qwen 2.5 0.5B** model through Ollama.

The primary goal is not simply to generate answers, but to build a RAG pipeline that is:

- **Grounded** — answers are based on retrieved course material
- **Local** — no external LLM API is required
- **Traceable** — answers expose the source slides used for generation
- **Retrieval-aware** — irrelevant questions can be rejected
- **Evaluated** — retrieval and abstention are measured quantitatively
- **Modular** — ingestion, retrieval, generation, and evaluation are separated

---

## ✨ Features

- 📚 **PowerPoint course-material ingestion**
- 🧩 **Slide-level chunking**
- 🔢 **Semantic text embeddings**
- 🗄️ **Local Qdrant vector database**
- 🔎 **Top-K semantic retrieval**
- 🎯 **Relevance threshold / retrieval gate**
- 🛑 **Out-of-domain question abstention**
- 🧠 **Context selection before generation**
- 🤖 **Local Qwen 2.5 0.5B generation through Ollama**
- 📎 **Source slide tracking**
- 🧪 **Retrieval evaluation**
- 📊 **Generation evaluation**
- 🛡️ **Abstention evaluation**
- 🔬 **Debugging and evaluation utilities**

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   Course Material   │
                    │      (.pptx)        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   PPTX Extraction   │
                    │   Slide Processing   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Chunking       │
                    │   Slide → Chunks    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Embeddings      │
                    │  Semantic Vectors   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Qdrant        │
                    │   Vector Database   │
                    └──────────┬──────────┘
                               │
                        User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Query Embedding     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Top-K Retrieval    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Relevance Gate      │
                    │ Threshold = 0.70    │
                    └───────┬───────┬─────┘
                            │       │
                     Relevant      Irrelevant
                            │       │
                            │       ▼
                            │   ┌────────────┐
                            │   │  Abstain   │
                            │   └────────────┘
                            │
                            ▼
                    ┌─────────────────────┐
                    │ Context Selection   │
                    │ Top relevant chunks │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Grounded Prompt     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Qwen 2.5 0.5B    │
                    │      Ollama         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Grounded Answer +   │
                    │ Source References   │
                    └─────────────────────┘