from flask import Flask, request, jsonify

app = Flask(__name__)

# Armazena o estado da conversa por usuário (simples, baseado no IP)
conversas = {}

@app.route("/", methods=["GET"])
def home():
    return "Chatbot está funcionando!"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"].strip().lower()
    user_id = request.remote_addr

    # Inicia conversa se ainda não existe
    if user_id not in conversas:
        conversas[user_id] = {"etapa": "inicio"}
        saudacao = (
            "Olá! Seja bem-vindo. Deseja agendar:\n"
            "1 - Entrega\n"
            "2 - Retirada"
        )
        return jsonify({"response": saudacao})

    etapa = conversas[user_id]["etapa"]

    # Escolha entre entrega ou retirada
    if etapa == "inicio":
        if user_input == "1":
            conversas[user_id]["etapa"] = "pedido"
            return jsonify({"response": "Você escolheu entrega. Por favor, informe o número do pedido."})
        elif user_input == "2":
            conversas[user_id]["etapa"] = "retirada"
            return jsonify({"response": "Você escolheu retirada. Por favor, informe o local e a data da retirada."})
        else:
            return jsonify({"response": "Desculpe, não entendi. Digite 1 para entrega ou 2 para retirada."})

    # Coleta número do pedido
    elif etapa == "pedido":
        conversas[user_id]["numero_pedido"] = user_input
        conversas[user_id]["etapa"] = "peticao"
        return jsonify({"response": "Pedido registrado. Agora, por favor, informe o número da petição."})

    # Coleta número da petição
    elif etapa == "peticao":
        conversas[user_id]["numero_peticao"] = user_input
        conversas[user_id]["etapa"] = "fim"
        return jsonify({
            "response": f"Entrega agendada com sucesso!\nNúmero do pedido: {conversas[user_id]['numero_pedido']}\nNúmero da petição: {user_input}"
        })

    # Coleta dados de retirada
    elif etapa == "retirada":
        conversas[user_id]["etapa"] = "fim"
        return jsonify({"response": f"Retirada agendada com os dados: {user_input}. Em breve entraremos em contato para confirmar."})

    # Conversa encerrada
    else:
        return jsonify({"response": "Obrigado! Se precisar de algo mais, envie uma nova mensagem."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

