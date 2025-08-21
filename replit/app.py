from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

# Load Gemini API key from Replit Secrets
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"reply": "Please send a valid message."})

    try:
        response = requests.post(
            "https://api.gemini.ai/v1/chat",
            headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
            json={"prompt": user_message, "model": "gemini-1.5"}
        )
        result = response.json()
        reply = result.get("reply", "Sorry, I couldn't respond.")
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
