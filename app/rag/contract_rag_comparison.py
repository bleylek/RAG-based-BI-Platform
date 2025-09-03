# app/rag/contract_rag_comparison.py

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

def generate_contract_comparison(contracts: List[Dict[str, Any]]) -> str:
    """
    Sözleşmeleri RAG tekniği ile karşılaştırır.
    
    Args:
        contracts: Her biri {"name": dosya_adı, "text": içerik} olan sözleşme listesi
    
    Returns:
        str: Karşılaştırma sonucu HTML tablosu ve analiz
    """
    # Sözleşme metinlerini ayır
    contract_texts = [c["text"] for c in contracts]
    contract_names = [c["name"] for c in contracts]
    
    # Öncelikle her sözleşmeyi bölümlere ayır (semantik chunking)
    all_sections = []
    section_sources = []  # Her bölümün hangi sözleşmeden geldiği
    
    for i, text in enumerate(contract_texts):
        # Yaklaşık 1000 karakterlik bölümlere ayırma
        words = text.split()
        chunks = []
        current_chunk = []
        
        for word in words:
            current_chunk.append(word)
            if len(' '.join(current_chunk)) >= 800:  # Yaklaşık 800 karakter
                chunks.append(' '.join(current_chunk))
                current_chunk = []
        
        if current_chunk:  # Son kısım da eklenmeli
            chunks.append(' '.join(current_chunk))
        
        # Bölümleri kaydet
        for chunk in chunks:
            all_sections.append(chunk)
            section_sources.append(i)
    
    # Tüm bölümleri embed et
    section_embeddings = get_embeddings(all_sections)
    
    # FAISS index oluştur
    dim = section_embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(section_embeddings)
    
    # Önemli sözleşme konuları
    important_topics = [
        "süre ve sözleşme süresi",
        "fesih koşulları",
        "cezai şart ve ceza maddeleri",
        "gizlilik ve gizlilik şartları",
        "teslimat ve performans şartları",
        "ödeme koşulları ve ödeme şekli",
        "tarafların yükümlülükleri",
        "uyuşmazlık çözümü",
        "yürürlük ve geçerlilik",
        "özel şartlar ve ek notlar"
    ]
    
    # Her konu için en alakalı bölümleri bul
    topic_results = []
    
    for topic in important_topics:
        # Konuyu embed et
        topic_embedding = get_embeddings([topic])[0]
        
        # Bu konu için en alakalı 5 bölümü bul
        _, I = index.search(topic_embedding.reshape(1, -1), k=min(10, len(all_sections)))
        top_indices = I[0].tolist()
        
        # Her sözleşmenin bu konu ile ilgili bölümlerini topla
        contract_sections = {}
        for idx in top_indices:
            contract_idx = section_sources[idx]
            contract_name = contract_names[contract_idx]
            
            if contract_name not in contract_sections:
                contract_sections[contract_name] = []
                
            contract_sections[contract_name].append(all_sections[idx])
        
        # Her sözleşmenin bu konu ile ilgili bölümlerini birleştir
        for name in contract_sections:
            contract_sections[name] = "\n".join(contract_sections[name])
            
        # Bu konu için karşılaştırma yap
        comparison = compare_topic_across_contracts(topic, contract_sections)
        topic_results.append({"topic": topic, "comparison": comparison})
    
    # Tüm sonuçları birleştir
    final_html = generate_final_html_report(topic_results, contract_names)
    return final_html

def compare_topic_across_contracts(topic, contract_sections):
    """Belirli bir konu için sözleşmeler arasında karşılaştırma yapar."""
    
    prompt = f"""
Aşağıda farklı sözleşmelerden çıkarılan "{topic}" konusu ile ilgili bölümler bulunmaktadır.
Bu bölümleri karşılaştırarak:

1. Her sözleşme için bu konunun nasıl ele alındığını kısaca özetle
2. Sözleşmeler arasındaki önemli farkları belirt
3. Avantaj/dezavantaj açısından değerlendir

"""
    
    # Sözleşme bölümlerini prompta ekle
    for contract_name, sections in contract_sections.items():
        prompt += f"\n--- {contract_name} ---\n{sections}\n"
    
    response = openai.ChatCompletion.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "Sen bir hukuk uzmanı AI asistansın."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message["content"].strip()

def generate_final_html_report(topic_results, contract_names):
    """Konuların karşılaştırmalarını HTML formatında birleştirir."""
    
    # Tüm sonuçları LLM'e gönderip düzenli bir HTML raporu oluşturmasını iste
    sections_text = ""
    for result in topic_results:
        sections_text += f"\n\n### {result['topic'].upper()}\n{result['comparison']}"
    
    prompt = f"""
Aşağıda farklı sözleşme bölümlerinin karşılaştırmaları bulunmaktadır.
Lütfen bu bilgileri kullanarak aşağıdaki yapıda bir HTML raporu oluştur:

1. Başlık
2. Karşılaştırma tablosu (aşağıdaki konuları satır, sözleşmeleri sütun yaparak)
3. Riskli/Eksik maddeler listesi
4. Genel değerlendirme ve öneriler

Sözleşmeler: {', '.join(contract_names)}

Karşılaştırma sonuçları:
{sections_text}

Çıktı olarak HTML formatında bir rapor oluştur. Tablonun anlaşılır ve iyi formatlanmış olmasına özen göster.
Riskli/eksik maddeleri belirgin şekilde işaretle.
"""

    response = openai.ChatCompletion.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "Sen bir sözleşme analizi uzmanı AI asistansın."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    
    return response.choices[0].message["content"].strip()
