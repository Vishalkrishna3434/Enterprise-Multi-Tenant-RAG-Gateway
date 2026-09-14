# Enterprise Multi-Tenant RAG Gateway

A backend-focused **Retrieval-Augmented Generation (RAG)** system built with **FastAPI**. The project uses a multi-stage retrieval pipeline to improve document search and context selection before generating answers with an LLM.

> **Status:** Under active development.

---

## Overview

The system processes documents into searchable representations and uses multiple retrieval and ranking stages to find relevant context before generating an answer.

```text
Documents
    ↓
Validation
    ↓
Extraction
    ↓
Parent-Child Chunking
    ↓
Embeddings
    ↓
Vector Storage


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
            │    Ingestion    │               │  Query Pipeline │
            │    Pipeline     │               │                 │
            └────────┬────────┘               └────────┬────────┘
                     │                                 │
                     ▼                                 ▼
              File Validation                      Guardrails
                     │                                 │
                     ▼                                 ▼
              Text Extraction                    User Query
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

The system has two primary pipelines:

* **Ingestion Pipeline:** Processes documents and stores searchable representations.
* **Query Pipeline:** Retrieves, ranks, selects relevant context, and generates responses.

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
Routers
    → HTTP handling

Schemas
    → Data validation

Services
    → RAG and business logic
```

This separation makes components easier to test, modify, and replace independently.

### Parent-Child Chunking

Small chunks improve retrieval precision but can lose surrounding context. Parent-child chunking retrieves precise child chunks while preserving access to larger parent context.

### Hybrid Retrieval

The system combines semantic and keyword-based retrieval.

```text
Query
  │
  ├── Vector Search
  │       ↓
  │   Semantic Matches
  │
  └── BM25 Search
          ↓
      Keyword Matches
          │
          ▼
        Fusion
```

Using multiple retrieval methods reduces dependence on a single search strategy.

### Reciprocal Rank Fusion

Vector search and BM25 produce different scoring systems. RRF combines their rankings instead of directly comparing incompatible scores.

```text
Vector Ranking + BM25 Ranking
              ↓
             RRF
              ↓
      Combined Results
```

### Cross-Encoder Reranking

Fast retrieval finds a set of candidate chunks first. A more expensive cross-encoder then reranks only those candidates.

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
   └── Valid
          ↓
      RAG Pipeline
```

### Async Generation

LLM API calls are primarily I/O-bound. Async handling allows the backend to handle other requests while waiting for external model services.

---

## API Endpoints

| Method   | Endpoint                   | Description                                                  |
| -------- | -------------------------- | ------------------------------------------------------------ |
| `GET`    | `/health`                  | Checks whether the API is running and healthy.               |
| `POST`   | `/documents/upload`        | Uploads and processes a document for retrieval.              |
| `POST`   | `/query`                   | Runs the retrieval and generation pipeline for a user query. |
| `GET`    | `/documents`               | Retrieves document metadata.                                 |
| `DELETE` | `/documents/{document_id}` | Deletes a document and its associated data.                  |

---

## Why Multi-Stage Retrieval?

A basic RAG system often follows:

```text
Document
    ↓
Embedding
    ↓
Vector Database
    ↓
LLM
```

This project uses a multi-stage approach:

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

The retrieval process is treated as a sequence of stages where cheaper retrieval methods find candidates and more expensive ranking methods refine the results.

---

## Future Improvements

* Multi-tenant isolation
* Authentication and authorization
* Tenant-scoped document retrieval
* Background document ingestion
* Observability and tracing
* Retrieval evaluation and benchmarking
* Production deployment and reliability improvements

### Evaluation

Different retrieval strategies can be compared:

```text
Vector Search
      vs
Hybrid Retrieval
      vs
Hybrid Retrieval + Reranking
```

Possible evaluation metrics include:

* Recall@K
* Precision@K
* MRR
* NDCG
* Latency

---

## Design Principles

```text
1. Validate early
2. Separate responsibilities
3. Retrieve using multiple signals
4. Use expensive models on smaller candidate sets
5. Keep components replaceable
6. Measure improvements rather than assuming them
```
