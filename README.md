````md
# Enterprise Multi-Tenant RAG Gateway

A backend-focused **Retrieval-Augmented Generation (RAG) system** built with FastAPI. The project uses a multi-stage retrieval pipeline to improve document search and context selection before generating answers with an LLM.

> **Status:** Under active development.

---

## What It Does

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

The core idea is:

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

FastAPI provides request validation, async support, type hints, and a clean API layer for document ingestion and querying.

```text
Request → Router → Service → RAG Components
```

---

### Modular Architecture

The application separates:

```text
Routers  → HTTP handling
Schemas  → Data validation
Services → RAG and business logic
```

This makes ingestion, retrieval, reranking, and generation easier to test and modify independently.

---

### Parent-Child Chunking

Small chunks improve retrieval precision but can lose surrounding context. Larger parent chunks preserve more context.

The system retrieves precise child chunks while retaining access to larger parent context.

---

### Hybrid Retrieval

The system combines:

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

This avoids depending entirely on either semantic or keyword retrieval.

---

### Reciprocal Rank Fusion

Vector search and BM25 produce different scoring systems. RRF combines their **rankings** instead of directly comparing incompatible scores.

```text
Vector Ranking + BM25 Ranking
              ↓
             RRF
              ↓
      Combined Results
```

---

### Cross-Encoder Reranking

Fast retrieval first finds candidate documents. A more expensive cross-encoder then reranks only the top candidates.

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

---

### Guardrails and Validation

Validation happens before expensive processing.

```text
Request
   ↓
Validation / Guardrails
   ├── Invalid → Reject
   └── Valid → RAG Pipeline
```

---

### Async Generation

LLM API calls are I/O-bound. Async handling helps the backend handle concurrent requests more efficiently while waiting for external services.

---

## Why This Is More Than a Basic RAG System

A basic RAG pipeline is often:

```text
Document → Embedding → Vector DB → LLM
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

The main architectural principle is:

> **Retrieval should be treated as a multi-stage process, not a single search operation.**

---

## Current Strengths

* Multiple retrieval signals
* Cost-aware reranking
* Clear separation of responsibilities
* Modular and replaceable components
* Backend-first architecture
* Validation before expensive operations

---

## Future Improvements

The most valuable next steps are:

* Real multi-tenant isolation
* Authentication and authorization
* Tenant-scoped document retrieval
* Background document ingestion
* Observability and tracing
* Retrieval evaluation and benchmarking
* Production deployment and reliability improvements

### Evaluation

Advanced retrieval techniques should be measured rather than assumed to improve results.

Possible comparisons:

```text
Vector Search
      vs
Hybrid Retrieval
      vs
Hybrid + Reranking
```

Possible metrics:

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
6. Measure improvements instead of assuming them
```

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

The project focuses on the engineering layers around retrieval quality, ranking, modularity, and reliability rather than simply connecting an LLM to a vector database.

> Advanced techniques such as hybrid search, parent-child chunking, and reranking add complexity and cost. Their value should be demonstrated through evaluation on representative data.

```
```
