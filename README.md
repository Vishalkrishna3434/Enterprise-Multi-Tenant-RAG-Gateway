````md
# Enterprise Multi-Tenant RAG Gateway

A backend-focused **Retrieval-Augmented Generation (RAG)** system built with **FastAPI**. The project uses a multi-stage retrieval pipeline to improve document search and context selection before generating answers with an LLM.

> **Status:** Under active development.

---

## Overview

The system processes documents into searchable representations and uses multiple retrieval and ranking stages to find relevant context before generating an answer.

```text
Documents
    ↓
File Validation
    ↓
Text Extraction
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
Hybrid Retrieval
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

The core approach is:

```text
Retrieve Broadly
      ↓
Combine Multiple Signals
      ↓
Rank More Precisely
      ↓
Generate Using Relevant Context
```

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

* **Ingestion Pipeline:** Validates, processes, chunks, embeds, and stores documents.
* **Query Pipeline:** Retrieves candidates, combines retrieval signals, reranks results, selects context, and generates a response.

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

Using multiple retrieval methods reduces dependence on a single retrieval strategy.

### Reciprocal Rank Fusion

Vector search and BM25 produce different score ranges. RRF combines their rankings instead of directly comparing incompatible scores.

```text
Vector Ranking + BM25 Ranking
              ↓
             RRF
              ↓
      Combined Results
```

### Cross-Encoder Reranking

Fast retrieval finds candidate chunks first. A more expensive cross-encoder then reranks only the top candidates.

```text
Large Corpus
     ↓
Fast Retrieval
     ↓
Top Candidates
     ↓
Cross-Encoder Reranking
```

This improves ranking precision while avoiding the cost of applying the cross-encoder to the entire corpus.

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

This project treats retrieval as a sequence of stages:

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

Cheaper retrieval methods first identify a broader candidate set, while more expensive ranking methods are applied to a smaller set of potentially relevant results.

---

## Tradeoffs

### Hybrid Retrieval

Combining vector search and BM25 improves retrieval robustness but adds additional retrieval and fusion complexity.

### Cross-Encoder Reranking

Reranking can improve ranking precision but adds inference latency and computational cost. It is therefore applied only to a limited set of retrieved candidates.

### Parent-Child Chunking

Parent-child chunking balances retrieval precision and context quality but requires maintaining relationships between child chunks and their parent context.

---

## Evaluation

Retrieval approaches can be compared to measure whether additional complexity improves results.

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
* Retrieval latency
* End-to-end response latency

The goal is to measure whether each additional retrieval stage provides meaningful improvements rather than assuming that a more complex pipeline automatically produces better results.

---

## Future Improvements

* Multi-tenant isolation
* Authentication and authorization
* Tenant-scoped document retrieval
* Background document ingestion
* Observability and tracing
* Retrieval evaluation and benchmarking
* Production deployment and reliability improvements

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