import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory store (later DB)
jd_store = []
embeddings = []

# Initialize FAISS index
dimension = 384
index = faiss.IndexFlatL2(dimension)


# ✅ Add JD to DB
def add_jd(jd_text):
    vector = model.encode([jd_text])[0]

    jd_store.append(jd_text)
    embeddings.append(vector)

    index.add(np.array([vector]))


# ✅ Search similar JDs
def search_jd(query, top_k=2):
    if len(jd_store) == 0:
        return []

    query_vector = model.encode([query])[0]
    D, I = index.search(np.array([query_vector]), top_k)

    results = [jd_store[i] for i in I[0] if i < len(jd_store)]
    return results

def get_skill_gaps(jd_text):
    try:
        results = search_jd(jd_text)  # already built

        market_skills = set()
        for r in results:
            metadata = r.get("metadata", {})
            skills = metadata.get("skills", [])
            market_skills.update(skills)

        jd_skills = set(jd_text.lower().split())

        missing_skills = list(market_skills - jd_skills)

        return {
            "missing_skills": missing_skills[:10],
            "market_skills": list(market_skills)[:10]
        }

    except Exception as e:
        return {"error": str(e)}    