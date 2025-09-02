# app/rag/embedder.py
import openai
from app.config import OPENAI_API_KEY
import numpy as np


openai.api_key = OPENAI_API_KEY


MODEL = "text-embedding-3-small"


def get_embeddings(texts):
    response = openai.Embedding.create(
    model=MODEL,
    input=texts
    )
    return np.array([r.embedding for r in response.data], dtype="float32") # OpenAI'den gelen embedding sonuçlarından sadece embedding kısımlarını al, bir NumPy dizisine dönüştür ve geri döndür.