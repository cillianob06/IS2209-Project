from flask import Flask, render_template, jsonify
import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

DOG_API_KEY = os.getenv("DOG_API_KEY")
DOG_API_URL = os.getenv("DOG_API_URL")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/random-dog')
def random_dog():
    headers = {"x-api-key": DOG_API_KEY}
    response = requests.get(f"{DOG_API_URL}/images/search", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data[0])  # Return the first dog image info
    else:
        return jsonify({"error": "Failed to fetch dog image"}), response.status_code


if __name__ == '__main__':
    app.run(debug=True)