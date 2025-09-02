# app/rag/llm_answerer.py
import openai
from app.config import OPENAI_API_KEY


openai.api_key = OPENAI_API_KEY


LLM_MODEL = "gpt-4"

# cv için
def generate_answer(context, job_description, query):
    prompt = f"""
    Aşağıda bir iş ilanı ve adaylara ait CV metinleri bulunmaktadır.

    Lütfen bu CV'leri dikkatlice değerlendirerek iş tanımına göre:

    1. En uygun adaydan en az uygun adaya kadar **sırala**
    2. Her aday için **neden uygun / neden daha az uygun** olduğunu **kısa açıklamalarla belirt**
    3. Değerlendirmeni sadece içerikteki bilgilere dayanarak yap
    4. Türkçe ve kısa, net ifadeler kullan
    
    İş Tanımı:
    {job_description}
    
    
    CV Metinleri:
    {context}
    
    
    Soru:
    {query}
    
    
    Yanıt (Türkçe, kısa, açıklayıcı):
    """


    response = openai.ChatCompletion.create(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

#teklif için
def generate_offer_summary_dynamic(offer_texts: list[str], metrics: str) -> str:
    prompt = f"Kullanıcı, aşağıdaki metriklere göre teklifler arasında karşılaştırma istiyor:\n→ {metrics.strip()}\n\n"

    for i, text in enumerate(offer_texts, 1):
        prompt += f"\n📄 Teklif {i}:\n{text.strip()}\n"

    prompt += "\n\n📊 Bu teklifleri yukarıdaki metrikler ışığında maddeler halinde karşılaştır ve genel bir yorum yap. Cevap Türkçe olsun."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Sen bir teklif değerlendirme uzmanısın."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

# sözleşmeler için
def compare_contracts_llm(contracts: list[dict]):
    contract_block = "\n\n".join(
        [f"<Sözleşme {i+1} – {c['name']}>\n{c['text']}" for i, c in enumerate(contracts)]
    )

    prompt = f"""
Aşağıda bazı sözleşmeler yer almaktadır. Lütfen bu sözleşmeleri aşağıdaki başlıklara göre karşılaştır:

- Süre
- Fesih Koşulları
- Cezai Şartlar
- Gizlilik Maddesi (NDA)
- Teslimat / Performans
- Ödeme Koşulları
- Yükümlülükler
- Uyuşmazlık Çözümü
- Yürürlük ve Geçerlilik
- Ek Notlar / Özel Şartlar

### 🔶 İSTENEN ÇIKTI (lütfen bu yapıya sadık kal):

1. 📊 HTML formatında bir karşılaştırma tablosu oluştur:
    - `<table>` etiketi kullan
    - Her satırda bir başlık olsun
    - Her sütun bir sözleşmeyi temsil etsin (Sözleşme 1, Sözleşme 2, ...)

2. 🔍 Belirgin eksik/riskli maddeleri listele (madde madde)

3. 🧠 Genel bir değerlendirme yap (hangi sözleşme daha avantajlı, neden)

⛔️ **Kesinlikle Markdown veya düz metin değil, sadece HTML tablo etiketi kullan.**

Sözleşme içerikleri:

{contract_block}
"""

    messages = [
        {"role": "system", "content": "Sen bir sözleşme analizi yapan hukuk danışmanı AI agentsin."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message["content"]


# mesaj/mail hazırlama için
def generate_auto_message(topic, recipient, tone, min_words, max_words, extra=""):
    import openai
    from app.config import OPENAI_API_KEY

    openai.api_key = OPENAI_API_KEY
    model = "gpt-4"

    # Tonu kelimeyle eşleştir
    if tone < 33:
        tone = "samimi ve sıcak"
    elif tone < 66:
        tone = "yarı-resmi ve dengeli"
    else:
        tone = "resmi ve profesyonel"

    # Prompt oluştur
    prompt = f"""
Sen bir mesaj yazma uzmanı AI'sın. Aşağıdaki bilgileri kullanarak istenilen kişiye uygun bir mesaj yazmalısın.

🎯 Konu: {topic}
👤 Alıcı: {recipient}
🎭 Ton: {tone}
📏 Uzunluk: Minimum {min_words} kelime, maksimum {max_words} kelime
📝 Ek Bilgi: {extra if extra.strip() else "Yok"}

Kurallar:
- Mesajı doğrudan yaz, açıklama yapma.
- Kibar, anlaşılır ve hedefe yönelik olsun.
- Format: Normal bir e-posta ya da mesaj gibi yaz.

Şimdi bu bilgilere göre mesajı üret:
"""

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Sen bir mesaj yazma uzmanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message["content"].strip()

    except Exception as e:
        return f"GPT hatası: {e}"
