from collections import defaultdict

def rank_resumes(vector_store, job_description: str, k: int = 20):
    # Fetch more results than needed to ensure all resumes have representation
    results = vector_store.similarity_search_with_score(
        job_description,
        k=k
    )

    # Group all page-level scores by resume name
    resume_map = defaultdict(list)

    for doc, score in results:
        name = doc.metadata.get(
            "resume_name",
            doc.metadata.get("source", "Unknown Resume")
        )
        resume_map[name].append({
            "score": float(score),
            "page": int(doc.metadata.get("page", 0)),
            "preview": str(doc.page_content[:250])
        })

    # For each resume, keep only the best scoring page
    ranked = []

    for resume_name, entries in resume_map.items():
        best_entry = max(entries, key=lambda x: x["score"])

        ranked.append({
            "resume": resume_name,
            "score": round(best_entry["score"] * 100, 2),
            "page": best_entry["page"],
            "preview": best_entry["preview"],
            "total_pages_matched": len(entries)  # useful debug info
        })

    # Sort by score descending
    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked