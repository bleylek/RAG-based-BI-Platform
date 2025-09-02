# run.py
from dotenv import load_dotenv
import os

# Önce .env dosyasını yükle
load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)