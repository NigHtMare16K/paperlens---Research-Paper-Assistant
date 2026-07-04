<div align="center">

# 📄 PaperLens

**Your AI-powered research companion — discover, read, and chat with scientific papers.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Qdrant](https://img.shields.io/badge/Vector%20DB-Qdrant-DC244C)](https://qdrant.tech/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack) • [Getting Started](#-getting-started) • [Roadmap](#-roadmap)

</div>

---

## 🧠 Overview

**PaperLens** is a research assistant that helps you *discover* the papers worth reading and *understand* them faster once you're in them.

It combines a personalized recommendation engine (built on paper embeddings, not tags) with a RAG-powered reader that lets you chat with any paper — ask it to explain a section in plain English, summarize the methodology, or generate a visual diagram of a concept.

> Built for researchers and students drowning in arXiv notifications who want a feed that actually learns what they care about — and a reader that answers questions instead of making them Ctrl+F through 40 pages.

---

## ✨ Features

- **🎯 Personalized recommendations** — Onboard by picking a few papers you like. PaperLens builds a taste vector from their embeddings and finds semantically similar work — no manual tagging required.
- **💬 Chat with any paper** — RAG-powered Q&A grounded in the actual paper content, with an "ELI5 mode" for plain-English explanations.
- **📊 Visual explanations** — Ask for a diagram and get an auto-generated visual breakdown of a concept.
- **🔥 Trending papers** — A daily-refreshed feed pulling from Hugging Face Papers, arXiv new submissions, and Semantic Scholar's influential papers, ranked with a recency-decayed trending score.
- **🏷️ Interest filters** — Predefined topic pills (AI, NLP, CV, Blockchain, Bioinformatics, etc.) that filter both your recommendations and the trending feed.
- **🔗 Citation chaining** — Explore a "related papers" panel showing what a paper cites and what cites it, powered by the Semantic Scholar citation graph.
- **🔔 Keyword alerts** — Set an alert for a topic (e.g. "diffusion models") and get a lightweight digest of new matching papers instead of email spam.

---

## 🏗️ Architecture

```mermaid
flowchart LR
    subgraph Sources
        A[arXiv API]
        B[Semantic Scholar API]
        C[HF Papers]
    end

    subgraph Backend [FastAPI Backend]
        D[Ingestion Service]
        E[Recommendation Engine]
        F[RAG Reader]
        G[Scheduler - APScheduler]
    end

    subgraph Storage
        H[(PostgreSQL)]
        I[(Qdrant)]
        J[(Redis)]
    end

    subgraph Frontend
        K[React + Tailwind]
    end

    A & B & C --> D
    D --> H
    D --> I
    E --> I
    E --> H
    F --> I
    F --> L[Groq: Llama 3.3 70B]
    G --> D
    J --> E
    J --> D
    K <--> Backend
```

**How it fits together:**
1. **Ingestion** pulls papers from arXiv, Semantic Scholar, and HF Papers on a schedule, embeds them with SPECTER2, and stores vectors in Qdrant + metadata in Postgres.
2. **Recommendations** average a user's liked-paper embeddings into a taste vector, then do nearest-neighbor search in Qdrant — updated continuously via exponential weighted averaging as the user reads/rates more papers.
3. **RAG Reader** chunks a paper's PDF into overlapping sections, embeds each chunk, and retrieves the top-k relevant chunks to ground Groq's answers when you ask a question.
4. **Redis** caches external API responses (avoiding rate limits) and trending scores.

---

## 🛠️ Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Frontend | React + Tailwind | Fast to build, great ecosystem |
| Backend | FastAPI | Async, Python-native, ML-friendly |
| LLM | Groq (Llama 3.3 70B) | Free tier, ~300 tokens/sec, no local GPU needed |
| Embeddings | SPECTER2 (HuggingFace) | Purpose-built for scientific paper similarity |
| Vector DB | Qdrant | Open-source, self-hostable, excellent Python SDK |
| Relational DB | PostgreSQL | Users, notes, alerts, reading history |
| Cache | Redis | API response caching + trending score computation |
| PDF Parsing | PyMuPDF (fitz) | Fast, accurate text extraction |
| Chunking / RAG | LangChain | Well-tested retrieval primitives |
| Background Jobs | APScheduler | Daily paper fetches, alert digests |
| Data Sources | arXiv, Semantic Scholar, HF Papers | All have free, official APIs |

---

## 📁 Project Structure

```
paperlens/
├── backend/
│   ├── api/
│   │   └── routes/
│   │       ├── reader.py
│   │       ├── recommendations.py
│   │       └── auth.py
│   ├── services/
│   │   ├── ingestion/       # data pipeline: fetch, parse, embed
│   │   ├── recommendation/  # taste vectors, nearest-neighbor search
│   │   └── rag/
│   │       ├── prompts.py   # all LLM prompt templates
│   │       └── retriever.py
│   ├── vector_store/
│   │   └── collections.py   # Qdrant collection definitions
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── store/           # Zustand: client state
│   │   ├── components/
│   │   └── pages/
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose

### Setup

```bash
# Clone the repo
git clone https://github.com/NigHtMare16K/paperlens.git
cd paperlens

# Copy environment template and fill in your keys
cp .env.example .env
```

Required environment variables:

```env
GROQ_API_KEY=your_groq_key
SEMANTIC_SCHOLAR_API_KEY=your_s2_key
DATABASE_URL=postgresql://user:password@localhost:5432/paperlens
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379
```

```bash
# Spin up the full stack (Postgres, Qdrant, Redis, backend, frontend)
docker-compose up --build
```

The app will be available at `http://localhost:5173`, with the API at `http://localhost:8000`.

---

## 🗺️ Roadmap

- [x] Core RAG reader with chat + ELI5 mode
- [x] Taste-vector recommendation engine
- [x] Trending feed with recency-decay scoring
- [x] Citation chaining panel
- [ ] Cold-start fallback (category-based recs for new users)
- [ ] Cross-encoder reranking on retrieved chunks
- [ ] OCR fallback for scanned/older PDFs
- [ ] Section-aware chunking (methods/results/references-aware)
- [ ] Reading streaks & history dashboard

---

## 🤝 Contributing

Issues and PRs are welcome. If you're adding a new data source or embedding model, please open an issue first to discuss the approach.

## 📄 License

MIT © [NigHtMare16K](https://github.com/NigHtMare16K)
