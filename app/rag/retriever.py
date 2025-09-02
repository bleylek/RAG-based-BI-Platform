# app/rag/retriever.py
import faiss


def build_faiss_index(embedding_matrix):
    dim = embedding_matrix.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embedding_matrix)
    return index


def search_similar(index, query_vector, k=3):
    _, I = index.search(query_vector.reshape(1, -1), k)
    return I[0].tolist()