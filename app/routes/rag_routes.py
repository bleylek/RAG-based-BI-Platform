# app/routes/rag_routes.py
from flask import Blueprint, request, render_template
from app.services.file_processor import extract_text  # eski: extract_text_from_pdf
from app.rag.embedder import get_embeddings
from app.rag.retriever import build_faiss_index, search_similar
from app.rag.llm_answerer import generate_answer
from app.auth.decorators import login_required
import os, json


rag_bp = Blueprint("rag", __name__)


@rag_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        files = request.files.getlist("files")
        job_description = request.form.get("job_description")


        texts = []
        for file in files:
            text = extract_text(file)
            texts.append(text)


        embeddings = get_embeddings(texts) # CV’lerden çıkarılan metinlerin embedding vektörleri oluşturuluyor.
        index = build_faiss_index(embeddings) # embeddings vektörlerini kullanarak FAISS veritabanı kurulur. Bu, benzerlik sorgularında kullanılacak.
        query_emb = get_embeddings([job_description])[0]
        top_indices = search_similar(index, query_emb, k=len(texts)) # top_indices: En benzerden en az benzer olana sıralı index listesi döner (örn. [2, 0, 1] gibi).


        top_cvs = [texts[i] for i in top_indices] # 🔢 top_indices Bu, FAISS ile yapılan benzerlik aramasının sonucudur. Yani iş ilanına en uygun CV’lerin index sıralamasıdır. Örnek (sıralı): top_indices = [2, 0, 1] Bu ne demek? "İş ilanına en uygun CV = texts[2], sonra texts[0], sonra texts[1]" 🧩 1. top_cvs = [texts[i] for i in top_indices] Bu satır, top_indices listesindeki sıralamaya göre texts listesinden en uygun CV’leri alır. Örnek: top_cvs = [ texts[2],  # "CV3 içeriği" texts[0],  # "CV1 içeriği" texts[1]   # "CV2 içeriği" ] Yani artık top_cvs listemiz, önce en uygun, sonra daha az uygun olan CV metinlerini içeriyor.
        context = "\n\n".join(top_cvs) # top_cvs listesindeki tüm metinleri, aralarına 2 satır boşluk (\n\n) koyarak tek bir metin haline getiriyor. Bu da LLM'e "işte sana context olarak bu CV'ler!" demek. Örnek: context = ( "CV3 içeriği: C++, Linux...\n\n" "CV1 içeriği: Python, SQL...\n\n" "CV2 içeriği: Java, AWS...")
        answer = generate_answer(context, job_description, "Bu ilana en uygun aday kim?")


        return render_template("results.html", answer=answer)
    return render_template("upload.html")