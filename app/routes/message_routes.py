# app/routes/message_routes.py
from flask import Blueprint, render_template, request
from app.rag.llm_answerer import generate_auto_message
from app.auth.decorators import login_required

message_bp = Blueprint("message_bp", __name__, url_prefix="/message")

@message_bp.route("/", methods=["GET", "POST"])
@login_required
def create_message():
    if request.method == "POST":
        topic = request.form.get("topic", "")
        recipient = request.form.get("recipient", "")
        tone = request.form.get("tone", "normal")
        word_min = int(request.form.get("min_words", 30))
        word_max = int(request.form.get("max_words", 150))
        extra = request.form.get("extra", "")

        try:
            message = generate_auto_message(
                topic=topic,
                recipient=recipient,
                tone=int(tone),
                min_words=word_min,
                max_words=word_max,
                extra=extra
            )
        except Exception as e:
            message = f"GPT mesajı oluşturulamadı: {e}"

        return render_template("message_result.html", message=message)

    return render_template("message_form.html")
