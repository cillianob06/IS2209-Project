from flask import Flask, jsonify, render_template
import os
import time
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

START_TIME = time.time()

DOG_API_KEY = os.getenv("DOG_API_KEY")
DOG_API_URL = "https://api.thedogapi.com/v1"

DATABASE_URL = os.getenv("DATABASE_URL")


# ----------------------
# DB CONNECTION
# ----------------------
def get_conn():
    return psycopg2.connect(DATABASE_URL)


# ----------------------
# INDEX
# ----------------------
@app.route('/')
def index():
    return render_template("index.html")


# ----------------------
# DOG API
# ----------------------
@app.route('/random-dog')
def random_dog():
    headers = {"x-api-key": DOG_API_KEY}
    response = requests.get(f"{DOG_API_URL}/images/search", headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()[0])
    return jsonify({"error": "Dog API failed"}), 500


# ----------------------
# STATUS (DB + API)
# ----------------------
@app.route("/status")
def status():
    uptime = round(time.time() - START_TIME, 2)

    # ---- DB CHECK ----
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT NOW();")
                db_time = cur.fetchone()[0]

        db_status = f"connected (time: {db_time})"

    except Exception as e:
        db_status = "database unavailable"

    # ---- DOG API CHECK ----
    try:
        headers = {"x-api-key": DOG_API_KEY}
        r = requests.get(f"{DOG_API_URL}/breeds", headers=headers)

        if r.status_code == 200:
            api_status = "connected"
        else:
            api_status = "error"

    except Exception:
        api_status = "unavailable"

    return jsonify({
        "service": "Dog Dashboard Service",
        "uptime_seconds": uptime,
        "database": db_status,
        "dog_api": api_status,
        "dog_api_configured": DOG_API_KEY is not None,
        "environment": os.getenv("ENVIRONMENT", "development")
    })


# ----------------------
# RUN
# ----------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )