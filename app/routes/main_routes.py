from flask import Blueprint, render_template, redirect, url_for, session
from app.auth.decorators import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def root():
    # Eğer kullanıcı zaten giriş yapmışsa, doğrudan ana sayfaya yönlendir
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    # Aksi takdirde login sayfasına yönlendir
    return redirect(url_for("auth.login"))


@main_bp.route("/home")
@login_required
def index():
    return render_template("index.html")


@main_bp.route("/about-platform")
@login_required
def about_platform():
    return render_template("about_platform.html")