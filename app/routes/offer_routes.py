# app/routes/offer_routes.py
from flask import Blueprint, render_template, request, flash
from app.services.file_processor import extract_text
from app.rag.llm_answerer import generate_offer_summary_dynamic
from app.rag.offer_rag_ranking import generate_offer_ranking
from app.auth.decorators import login_required

offer_bp = Blueprint("offer", __name__, url_prefix="/offers")

@offer_bp.route("/", methods=["GET", "POST"])
@login_required
def compare_offers():
    if request.method == "POST":
        uploaded_files = request.files.getlist("offer_files")
        metrics = request.form.get("metrics", "")

        if not uploaded_files or not metrics:
            flash("Lütfen dosya ve karşılaştırma metrikleri girin.", "error")
            return render_template("offer_upload.html")

        offer_texts = []
        for file in uploaded_files:
            try:
                text = extract_text(file)
                offer_texts.append(text.strip())
            except Exception as e:
                error_msg = f"HATA ({file.filename}): {str(e)}"
                offer_texts.append(error_msg)
                flash(error_msg, "error")
                
        # Her iki analiz türünü de dene
        rag_result = None
        classic_result = None
        
        # 1. RAG ile analizi dene
        try:
            rag_result = generate_offer_ranking(offer_texts, metrics)
            flash("Teklifler RAG teknolojisi ile başarıyla analiz edildi.", "success")
        except Exception as e:
            print(f"RAG sıralamada hata: {e}")
            flash("RAG ile analiz sırasında hata oluştu, klasik analiz deneniyor.", "warning")
            
        # 2. Klasik GPT-4 analizini dene (yedekleme olarak veya karşılaştırma için)
        try:
            classic_result = generate_offer_summary_dynamic(offer_texts, metrics)
        except Exception as e:
            print(f"Klasik analiz hatası: {e}")
        
        # Sonuçları birleştir
        if rag_result:
            if classic_result:
                # Her iki yöntem de başarılı - birleştir
                evaluation = f"<h2>🧠 RAG Tabanlı Analiz</h2><div class='rag-analysis'>{rag_result}</div><hr>"
                evaluation += f"<h2>🔍 Klasik LLM Analizi</h2><div class='classic-analysis'>{classic_result}</div>"
            else:
                # Sadece RAG sonucu var
                evaluation = f"<h2>🧠 RAG Tabanlı Analiz</h2><div class='rag-analysis'>{rag_result}</div>"
        elif classic_result:
            # Sadece klasik sonuç var
            evaluation = f"<h2>🔍 Klasik LLM Analizi</h2><div class='classic-analysis'>{classic_result}</div>"
            flash("RAG analizi başarısız oldu, klasik analiz görüntüleniyor.", "warning")
        else:
            # Hiçbir analiz başarılı değil
            evaluation = "Tekliflerin analizi sırasında her iki yöntem de başarısız oldu."
            flash("Tekliflerin analizi yapılamadı.", "error")

        return render_template("offer_results.html", evaluation=evaluation)

    return render_template("offer_upload.html")
