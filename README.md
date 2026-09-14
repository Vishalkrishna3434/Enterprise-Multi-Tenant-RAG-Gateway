# Enterprise Multi-Tenant RAG Gateway

A backend-focused **Retrieval-Augmented Generation (RAG)** system built with **FastAPI**. The project uses a multi-stage retrieval pipeline to improve document search and context selection before generating answers with an LLM.

> **Status:** Under active development.

---

## Overview

The system processes documents into searchable representations and uses multiple retrieval and ranking stages to identify relevant context before generating an answer.

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
```

The core approach:

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
              Text Extraction                  Hybrid Retrieval
                     │                         ┌───────┴───────┐
                     ▼                         ▼               ▼
           Parent-Child Chunking         Vector Search       BM25
                     │                         │               │
                     ▼                         └───────┬───────┘
                Embeddings                            │
                     │                                ▼
                     ▼                         RRF Fusion
              Vector Storage                          │
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

The system consists of two primary pipelines:

- **Ingestion Pipeline:** Validates, extracts, chunks, embeds, and stores documents.
- **Query Pipeline:** Retrieves candidates, combines retrieval signals, reranks results, selects context, and generates a response.

---

## Features

- Semantic vector search
- BM25 keyword search
- Hybrid retrieval
- Reciprocal Rank Fusion (RRF)
- Cross-encoder reranking
- Parent-child chunking
- File validation and guardrails
- Async LLM generation
- Modular FastAPI backend architecture

---

## Key Architecture Decisions

### Modular FastAPI Architecture

The application separates responsibilities:

```text
Routers  → HTTP and request handling
Schemas  → Request and response validation
Services → Retrieval and business logic
```

This keeps the API layer separate from the RAG pipeline and makes components easier to test, modify, and replace.

### Parent-Child Chunking

Small chunks can improve retrieval precision but may lose surrounding context. Parent-child chunking retrieves precise child chunks while preserving access to larger parent context.

### Hybrid Retrieval

The system combines two retrieval signals:

```text
Query
  │
  ├── Vector Search → Semantic Matches
  │
  └── BM25 Search   → Keyword Matches
             │
             ▼
          RRF Fusion
```

Vector search captures semantic similarity, while BM25 helps with exact terms and keyword matches.

### Reciprocal Rank Fusion

Vector search and BM25 produce different scoring systems. RRF combines their rankings instead of directly comparing incompatible scores.

### Cross-Encoder Reranking

Initial retrieval is optimized for speed and recall. A more expensive cross-encoder is applied only to the top candidates.

```text
Large Corpus
     ↓
Fast Retrieval
     ↓
Top Candidates
     ↓
Cross-Encoder Reranking
```

This improves ranking precision without applying expensive inference across the entire corpus.

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

LLM calls are primarily I/O-bound. Async handling allows the backend to handle other requests while waiting for external model services.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Checks whether the API is running. |
| `POST` | `/documents/upload` | Uploads and processes a document for retrieval. |
| `POST` | `/query` | Runs retrieval and generation for a user query. |
| `GET` | `/documents` | Retrieves document metadata. |
| `DELETE` | `/documents/{document_id}` | Deletes a document and its associated data. |

---

## Why Multi-Stage Retrieval?

A basic RAG pipeline often follows:

```text
Document
    ↓
Embedding
    ↓
Vector Database
    ↓
LLM
```

This project treats retrieval as a multi-stage process:

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

The idea is to use faster retrieval methods to identify a broader candidate set and apply more expensive ranking methods only where they provide additional value.

---

## Tradeoffs

### Hybrid Retrieval

Combining vector search and BM25 can improve retrieval robustness but adds retrieval and fusion complexity.

### Cross-Encoder Reranking

Reranking can improve ranking precision but adds inference latency and computational cost. It is therefore applied only to a limited set of retrieved candidates.

### Parent-Child Chunking

Parent-child chunking balances retrieval precision and context quality but requires maintaining relationships between child chunks and their parent context.

---

## Evaluation

The retrieval pipeline can be evaluated to determine whether each additional stage provides meaningful improvements:

```text
Vector Search
      vs
Hybrid Retrieval
      vs
Hybrid Retrieval + Reranking
```

Possible metrics include:

- Recall@K
- Precision@K
- MRR
- NDCG
- Retrieval latency
- End-to-end response latency

The goal is to measure improvements rather than assume that a more complex pipeline automatically produces better results.

---

## Future Improvements

- Multi-tenant isolation
- Authentication and authorization
- Tenant-scoped document retrieval
- Background document ingestion
- Observability and tracing
- Retrieval evaluation and benchmarking
- Production deployment and reliability improvements

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