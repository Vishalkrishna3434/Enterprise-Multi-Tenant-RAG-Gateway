Enterprise Multi-Tenant RAG Gateway

A backend-focused Retrieval-Augmented Generation (RAG) system built with FastAPI. The project uses a multi-stage retrieval pipeline to improve document search and context selection before generating answers with an LLM.

Status: Under active development.

WHAT IT DOES

The system processes documents into searchable representations and uses multiple retrieval and ranking stages to find relevant context for LLM generation.

Documents
    ↓
Validation
    ↓
Extraction
    ↓
Chunking
    ↓
Embeddings
    ↓
Storage


User Query
    ↓
Guardrails
    ↓
Vector Search + BM25
    ↓
Reciprocal Rank Fusion
    ↓
Cross-Encoder Reranking
    ↓
Context Selection
    ↓
LLM Generation
    ↓
Response


```text
Documents
    ↓
Validation → Extraction → Chunking → Embeddings → Storage

User Query
    ↓
Guardrails
    ↓
Vector Search + BM25
    ↓
Reciprocal Rank Fusion
    ↓
Cross-Encoder Reranking
    ↓
Context Selection
    ↓
LLM Generation
    ↓
Response
````

---

## Architecture

```text
                              ┌───────────────┐
                              │    Client     │
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │    FastAPI    │
                              │   API Layer   │
                              └───────┬───────┘
                                      │
                     ┌────────────────┴────────────────┐
                     │                                 │
                     ▼                                 ▼
            ┌─────────────────┐               ┌─────────────────┐
            │    Ingestion    │               │   Query Pipeline │
            └────────┬────────┘               └────────┬────────┘
                     │                                 │
                     ▼                                 ▼
             File Validation                       Guardrails
                     │                                 │
                     ▼                                 ▼
              Text Extraction                     User Query
                     │                                 │
                     ▼                                 ▼
           Parent-Child Chunking            Hybrid Retrieval
                     │                        │          │
                     ▼                        ▼          ▼
                Embeddings              Vector Search   BM25
                     │                        │          │
                     ▼                        └────┬─────┘
              Vector Storage                        │
                                                    ▼
                                             Rank Fusion (RRF)
                                                    │
                                                    ▼
                                         Cross-Encoder Reranking
                                                    │
                                                    ▼
                                            Context Selection
                                                    │
                                                    ▼
                                             LLM Generation
                                                    │
                                                    ▼
                                                 Response
```

---

## Features

* Semantic vector search
* BM25 keyword search
* Hybrid retrieval
* Reciprocal Rank Fusion (RRF)
* Cross-encoder reranking
* Parent-child chunking
* File validation and guardrails
* Async LLM generation
* Modular FastAPI backend architecture

---

## Key Architecture Decisions

### FastAPI

FastAPI provides request validation, type hints, async support, and a clean API layer.

```text
Request → Router → Service → RAG Components
```

### Modular Architecture

The application separates responsibilities:

```text
Routers  → HTTP handling
Schemas  → Data validation
Services → RAG and business logic
```

This makes individual components easier to test, modify, and replace independently.

### Parent-Child Chunking

Small chunks improve retrieval precision but may lose surrounding context. Parent-child chunking retrieves smaller, precise chunks while preserving access to larger surrounding context.

### Hybrid Retrieval

The system combines semantic and keyword retrieval:

```text
Query
  │
  ├── Vector Search → Semantic Matches
  │
  └── BM25 Search   → Keyword Matches
             │
             ▼
          Fusion
```

This reduces dependence on a single retrieval strategy.

### Reciprocal Rank Fusion

Vector search and BM25 produce different score ranges. RRF combines their rankings instead of directly comparing incompatible scores.

### Cross-Encoder Reranking

Fast retrieval finds candidate documents first. A more expensive cross-encoder then reranks only the top candidates.

```text
Large Corpus
     ↓
Fast Retrieval
     ↓
Top Candidates
     ↓
Cross-Encoder Reranking
```

This balances retrieval speed and ranking quality.

### Guardrails and Validation

Requests and files are validated before expensive processing.

```text
Request
   ↓
Validation / Guardrails
   ├── Invalid → Reject
   └── Valid → RAG Pipeline
```

### Async Generation

LLM API calls are I/O-bound. Async handling helps the backend handle concurrent requests efficiently while waiting for external services.

---

## API Endpoints

| Method   | Endpoint                   | Description                                                      |
| -------- | -------------------------- | ---------------------------------------------------------------- |
| `GET`    | `/health`                  | Checks whether the API is running and healthy.                   |
| `POST`   | `/documents/upload`        | Uploads and processes a document for retrieval.                  |
| `POST`   | `/query`                   | Runs the RAG retrieval and generation pipeline for a user query. |
| `GET`    | `/documents`               | Retrieves document metadata.                                     |
| `DELETE` | `/documents/{document_id}` | Deletes a document and its associated data.                      |

---

## Why Multi-Stage Retrieval?

A basic RAG system often looks like:

```text
Document → Embedding → Vector Database → LLM
```

This project uses:

```text
Multiple Retrieval Methods
        ↓
Rank Fusion
        ↓
Precise Reranking
        ↓
Context Selection
        ↓
LLM
```

> **Retrieval is treated as a multi-stage process rather than a single search operation.**

---

## Future Improvements

* Real multi-tenant isolation
* Authentication and authorization
* Tenant-scoped document retrieval
* Background document ingestion
* Observability and tracing
* Retrieval evaluation and benchmarking
* Production deployment and reliability improvements

### Evaluation

Retrieval approaches can be compared using:

```text
Vector Search
      vs
Hybrid Retrieval
      vs
Hybrid + Reranking
```

Possible metrics include:

* Recall@K
* Precision@K
* MRR
* NDCG
* Latency

---

## Summary

Enterprise Multi-Tenant RAG Gateway is a FastAPI-based RAG backend built around a **multi-stage retrieval architecture**.

```text
Retrieve Broadly
      ↓
Combine Retrieval Signals
      ↓
Rank More Precisely
      ↓
Select Relevant Context
      ↓
Generate an Answer
```

The project focuses on retrieval quality, ranking, modularity, and reliability rather than simply connecting an LLM to a vector database.

```
```
