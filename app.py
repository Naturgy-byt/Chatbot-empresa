from flask import Flask, request, jsonify
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
    return jsonify({"response": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
