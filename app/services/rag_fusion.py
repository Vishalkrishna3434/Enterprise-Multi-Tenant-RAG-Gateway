from collections import defaultdict

def reciprocal_rank_fusion(rankings: list[list[int]], k_constant: int = 60) -> list[int]:
    """Combines any number of ranked-index lists into one fused ranking via RRF."""
    rrf_scores = defaultdict(float)
    for ranking in rankings:
        for rank, doc_idx in enumerate(ranking):
            rrf_scores[doc_idx] += 1.0 / (k_constant + rank + 1)
    return sorted(rrf_scores.keys(), key=lambda idx: rrf_scores[idx], reverse=True)