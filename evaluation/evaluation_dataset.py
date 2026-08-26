evaluation_dataset = [

    {
        "question": "What are the two core components of RAG?",
        "ground_truth": "RAG has two core components: the retriever, which indexes your data upfront and queries it at inference time to fetch relevant context, and the generator, usually an LLM, which produces the final response using the query and retrieved context."
    },

    {
        "question": "What is term-based retrieval?",
        "ground_truth": "Term-based retrieval finds documents containing the query's keywords and is also called lexical retrieval."
    },

    {
        "question": "What is embedding-based retrieval?",
        "ground_truth": "Embedding-based retrieval ranks documents by how closely their meaning aligns with the query and is also called semantic retrieval."
    },

    {
        "question": "Why is hybrid search used in RAG?",
        "ground_truth": "Hybrid retrieval combines term-based and embedding-based retrieval and is a safe default when queries mix exact-match needs such as IDs, names, and codes with semantic or paraphrased queries."
    },

    {
        "question": "What is Reciprocal Rank Fusion (RRF)?",
        "ground_truth": "Reciprocal Rank Fusion is an algorithm for combining rankings produced by different retrievers into one final ranking using Score(D) = Σ 1 / (k + ri(D)), where k is typically 60."
    },

    {
        "question": "Why is parent-child chunking used in RAG?",
        "ground_truth": "Parent-child chunking indexes small child chunks for precise matching but passes the larger parent chunk to the generator when a child is retrieved, thereby decoupling what gets matched from what gets read."
    },

    {
        "question": "What is context precision?",
        "ground_truth": "Context precision measures, out of all documents retrieved, what percentage is actually relevant to the query."
    },

    {
        "question": "What is context recall?",
        "ground_truth": "Context recall measures, out of all documents truly relevant to the query, what percentage the retriever actually retrieved."
    },

    {
        "question": "What happens when k is increased during retrieval?",
        "ground_truth": "Fetching more documents with a higher k tends to raise recall but can lower precision by pulling in irrelevant chunks, which also increases generator context cost and noise."
    },

    {
        "question": "Why is reranking used in a RAG pipeline?",
        "ground_truth": "Reranking is the refining step in which a more precise but more expensive mechanism narrows a broad candidate set retrieved by a cheaper and less precise retriever to the best candidates."
    }
]