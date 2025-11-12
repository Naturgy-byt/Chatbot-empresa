from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Chatbot está funcionando!"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"].strip().lower()

    if user_input in ["oi", "olá", "bom dia", "boa tarde", "boa noite"]:
        saudacao = (
            "Olá! Seja bem-vindo. Deseja agendar:\n"
            "1 - Entrega\n"
            "2 - Retirada"
        )
        return jsonify({"response": saudacao})

    return jsonify({"response": "Desculpe, não entendi. Por favor, diga 'oi' para começar."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, request, jsonify
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Chatbot está funcionando!"

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
