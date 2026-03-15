from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory storage
alumni_texts = []
alumni_vectors = None
index = None


def embed_text(text: str):
    """
    Convert text into vector embedding
    """
    return model.encode([text])[0]


def build_index(alumni_list):
    """
    Build FAISS index from alumni database
    """

    global alumni_vectors, index, alumni_texts

    alumni_texts = []

    vectors = []

    for alum in alumni_list:

        text = f"{alum['name']} works at {alum['company']} with skills {alum['skills']}"

        alumni_texts.append(text)

        vectors.append(embed_text(text))

    if len(vectors) == 0:
        return

    alumni_vectors = np.array(vectors).astype("float32")

    dimension = alumni_vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(alumni_vectors)


def search_alumni(query: str, top_k: int = 5):
    """
    Semantic search for alumni
    """

    if index is None:
        return []

    query_vector = embed_text(query).astype("float32").reshape(1, -1)

    distances, indices = index.search(query_vector, top_k)

    results = []

    for idx in indices[0]:
        if idx < len(alumni_texts):
            results.append(alumni_texts[idx])

    return results