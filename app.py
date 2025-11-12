from flask import Flask, request, jsonify

app = Flask(__name__)

# Armazena o estado da conversa por usuário (simples, baseado no IP)
conversas = {}

@app.route("/", methods=["GET"])
def home():
    return "Chatbot está funcionando!"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"].strip()
    user_id = request.remote_addr

    if user_id not in conversas:
        conversas[user_id] = {"etapa": "inicio"}
        saudacao = (
            "Olá! Seja bem-vindo. Deseja agendar:\n"
            "1 - Entrega\n"
            "2 - Retirada"
        )
        return jsonify({"response": saudacao})

    etapa = conversas[user_id]["etapa"]

    if etapa == "inicio":
        if user_input == "1":
            conversas[user_id]["etapa"] = "pedido"
            return jsonify({"response": "Você escolheu entrega. Por favor, informe o número do pedido."})
        elif user_input == "2":
            conversas[user_id]["etapa"] = "retirada_local"
            return jsonify({"response": "Você escolheu retirada. Por favor, informe o local da retirada."})
        else:
            return jsonify({"response": "Desculpe, não entendi. Digite 1 para entrega ou 2 para retirada."})

    elif etapa == "pedido":
        conversas[user_id]["numero_pedido"] = user_input
        conversas[user_id]["etapa"] = "peticao"
        return jsonify({"response": "Pedido registrado. Agora, informe o número da petição."})

    elif etapa == "peticao":
        conversas[user_id]["numero_peticao"] = user_input
        conversas[user_id]["etapa"] = "responsavel"
        return jsonify({"response": "Petição registrada. Por favor, informe o nome do responsável."})

    elif etapa == "retirada_local":
        conversas[user_id]["local_retirada"] = user_input
        conversas[user_id]["etapa"] = "responsavel"
        return jsonify({"response": "Local registrado. Por favor, informe o nome do responsável."})

    elif etapa == "responsavel":
        conversas[user_id]["responsavel"] = user_input
        conversas[user_id]["etapa"] = "data"
        return jsonify({"response": "Responsável registrado. Informe a data desejada (ex: 25/11/2025)."})

    elif etapa == "data":
        conversas[user_id]["data"] = user_input
        conversas[user_id]["etapa"] = "hora"
        return jsonify({"response": "Data registrada. Agora, informe o horário desejado (ex: 14:30)."})

    elif etapa == "hora":
        conversas[user_id]["hora"] = user_input
        conversas[user_id]["etapa"] = "material"
        return jsonify({"response": "Horário registrado. Por fim, informe o tipo de material."})

    elif etapa == "material":
        conversas[user_id]["material"] = user_input
        conversas[user_id]["etapa"] = "fim"

        dados = conversas[user_id]
        if "numero_pedido" in dados:
            resumo = (
                f"Entrega agendada com sucesso!\n"
                f"Pedido: {dados['numero_pedido']}\n"
                f"Petição: {dados['numero_peticao']}\n"
            )
        else:
            resumo = (
                f"Retirada agendada com sucesso!\n"
                f"Local: {dados['local_retirada']}\n"
            )

        resumo += (
            f"Responsável: {dados['responsavel']}\n"
            f"Data: {dados['data']}\n"
            f"Horário: {dados['hora']}\n"
            f"Material: {dados['material']}"
        )

        return jsonify({"response": resumo})

    else:
        return jsonify({"response": "Obrigado! Se precisar de algo mais, envie uma nova mensagem."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
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

