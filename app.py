from flask import Flask, jsonify, render_template, request
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


def get_conn():
    return psycopg2.connect(DATABASE_URL)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/random-dog')
def random_dog():
    headers = {"x-api-key": DOG_API_KEY}
    response = requests.get(f"{DOG_API_URL}/images/search?include_breeds=1", headers=headers)

    if response.status_code == 200:
        dog_data = response.json()[0]
        breeds = dog_data.get("breeds", [])
        breed_name = breeds[0]["name"] if breeds else "Unknown"

        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO dog_requests (breed) VALUES (%s);", (breed_name,))
                conn.commit()
        except Exception as e:
            print(f"DB log failed: {e}")

        return jsonify(dog_data)
    return jsonify({"error": "Dog API failed"}), 500


@app.route('/stats')
def stats():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM dog_requests;")
                count = cur.fetchone()[0]
        return jsonify({"total_dog_requests": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/stats-page')
def stats_page():
    return render_template("stats.html")


@app.route("/status")
def status():
    uptime = round(time.time() - START_TIME, 2)

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT NOW();")
                db_time = cur.fetchone()[0]
        db_status = f"connected (time: {db_time})"
    except Exception:
        db_status = "database unavailable"

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


@app.route("/health")
def health():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        db_status = "ok"
    except Exception:
        db_status = "unavailable"

    status = "ok" if db_status == "ok" else "degraded"

    return jsonify({
        "status": status,
        "database": db_status,
    }), 200


@app.route('/breeds')
def get_breeds():
    headers = {"x-api-key": DOG_API_KEY}
    response = requests.get(f"{DOG_API_URL}/breeds", headers=headers)
    if response.status_code == 200:
        breeds = [{"id": b["id"], "name": b["name"]} for b in response.json()]
        return jsonify(breeds)
    return jsonify({"error": "Could not fetch breeds"}), 500


@app.route('/random-dog-by-breed/<int:breed_id>')
def random_dog_by_breed(breed_id):
    headers = {"x-api-key": DOG_API_KEY}
    response = requests.get(f"{DOG_API_URL}/images/search?breed_ids={breed_id}&include_breeds=1", headers=headers)
    if response.status_code == 200:
        dog_data = response.json()[0]
        breeds = dog_data.get("breeds", [])
        breed_name = breeds[0]["name"] if breeds else "Unknown"

        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO dog_requests (breed) VALUES (%s);", (breed_name,))
                conn.commit()
        except Exception as e:
            print(f"DB log failed: {e}")

        return jsonify(dog_data)
    return jsonify({"error": "Dog API failed"}), 500


@app.route('/favourite', methods=['POST'])
def add_favourite():
    data = request.get_json()
    image_url = data.get('url')

    if not image_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO favourites (image_url) VALUES (%s);", (image_url,))
            conn.commit()
        return jsonify({"message": "Saved!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/favourites')
def get_favourites():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT image_url, created_at FROM favourites ORDER BY created_at DESC;")
                rows = cur.fetchall()
        return jsonify([{"url": row[0], "saved_at": str(row[1])} for row in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/favourites-page')
def favourites_page():
    return render_template("favourites.html")


@app.route('/leaderboard')
def leaderboard():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT breed, COUNT(*) as count
                    FROM dog_requests
                    WHERE breed IS NOT NULL AND breed != 'Unknown'
                    GROUP BY breed
                    ORDER BY count DESC
                    LIMIT 5;
                """)
                rows = cur.fetchall()
        return jsonify([{"breed": row[0], "count": row[1]} for row in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )