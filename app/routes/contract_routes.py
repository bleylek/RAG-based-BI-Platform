# app/routes/contract_routes.py
from app.services.file_processor import extract_text  # senin mevcut fonksiyonun
from app.rag.llm_answerer import compare_contracts_llm  # Klasik LLM analizi için
from app.rag.contract_rag_comparison import generate_contract_comparison  # RAG tabanlı karşılaştırma
from flask import Blueprint, request, render_template, flash
from app.auth.decorators import login_required

contract_bp = Blueprint("contract_bp", __name__, url_prefix="/contracts")

@contract_bp.route("/", methods=["GET", "POST"])
@login_required
def compare_contracts():
    if request.method == "POST":
        files = request.files.getlist("contract_files")
        if not files:
            return "Lütfen sözleşme dosyası yükleyin."

        # Tüm sözleşmeleri okuyup liste haline getir
        contracts = []
        for f in files:
            try:
                text = extract_text(f)
                contracts.append({"name": f.filename, "text": text})
            except Exception as e:
                print(f"{f.filename} okunamadı: {e}")
                flash(f"{f.filename} dosyası okunamadı: {e}", "error")

        # RAG ile analiz ettir (öncelikli yöntem)
        try:
            ai_output = generate_contract_comparison(contracts)
            flash("Sözleşmeler RAG teknolojisi ile başarıyla analiz edildi.", "success")
        except Exception as e:
            print(f"RAG karşılaştırması hatası: {e}")
            flash("RAG analizi başarısız oldu, klasik karşılaştırma yöntemine geçildi.", "warning")
            
            # Fallback olarak klasik LLM karşılaştırması kullan
            try:
                ai_output = compare_contracts_llm(contracts)
            except Exception as fallback_error:
                ai_output = f"GPT yanıtı alınamadı: {str(fallback_error)}"
                flash(f"Karşılaştırma yapılamadı: {str(fallback_error)}", "error")

        return render_template("contract_results.html", ai_output=ai_output)

    return render_template("contract_upload.html")
