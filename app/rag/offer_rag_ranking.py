# app/rag/offer_rag_ranking.py

from app.config import OPENAI_API_KEY
import openai
import numpy as np
import faiss
from typing import List, Dict, Any

openai.api_key = OPENAI_API_KEY

EMBED_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4"

def get_embeddings(texts):
    response = openai.Embedding.create(
        model=EMBED_MODEL,
        input=texts
    )
    return np.array([r.embedding for r in response.data], dtype="float32")

def generate_offer_ranking(offer_texts: List[str], metrics: str) -> str:
    # Embed teklif metinleri
    embeddings = get_embeddings(offer_texts)

    # FAISS index oluştur
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Her teklif için en benzer 3 teklifi bul
    groups = []
    for i in range(len(offer_texts)):
        _, I = index.search(embeddings[i].reshape(1, -1), k=3)
        indices = I[0].tolist()
        unique_indices = list(dict.fromkeys([i] + indices))  # tekrarları sil, sırayı koru
        group_texts = [f"Teklif {j+1}:{offer_texts[j].strip()}" for j in unique_indices]
        joined = "\n\n".join(group_texts)
        groups.append(joined)

    # Her grup için GPT'ten analiz al
    results = []
    for i, group in enumerate(groups):
        prompt = f"""
Aşağıda bazı teklifler yer almakta. Lütfen şu metriklere göre karşılaştır:
📌 {metrics.strip()}

{group}

🎯 Çıktı:
- En iyi tekliften en kötüye sırala (örn: 1 > 3 > 2)
- Her teklif için kısa açıklama yap (neden daha iyi / kötü)
- Genel değerlendirme ver
- Türkçe ve açıklayıcı yaz
"""
        response = openai.ChatCompletion.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": "Sen bir teklif analisti AI'sın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        output = response.choices[0].message.content.strip()
        results.append(f"--- Teklif {i+1} için değerlendirme ---\n" + output + "\n")

    return "\n\n".join(results)
