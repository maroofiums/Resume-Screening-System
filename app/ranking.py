def rank_resumes(vector_store, job_description: str, k: int = 10):

    results = vector_store.similarity_search_with_score(
        job_description,
        k=k
    )

    ranked = []

    for doc, distance in results:

        distance = float(distance)

        similarity = 1 / (1 + distance)

        ranked.append(
            {
                "resume": doc.metadata.get(
                    "resume_name",
                    doc.metadata.get("source", "Unknown Resume"),
                ),
                "score": round(float(similarity * 100), 2),
                "page": int(doc.metadata.get("page", 0)),
                "preview": str(doc.page_content[:250]),
            }
        )

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return ranked