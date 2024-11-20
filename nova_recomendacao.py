from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Página inicial para testar o envio (se necessário)
@app.route('/')
def index():
    return "Back-end funcionando! Acesse /nova-recomendacao para enviar dados."

# Rota para processar o formulário de recomendação
@app.route('/nova-recomendacao', methods=['POST'])
def nova_recomendacao():
    # Coleta os dados enviados pelo formulário
    sentimento = request.form.getlist('sentimento')  # Retorna uma lista de sentimentos selecionados
    tarefa = request.form.get('tarefa')             # Tarefa selecionada
    foco = request.form.get('foco')                 # Porcentagem de foco

    # Exibe ou salva os dados recebidos
    print(f"Sentimentos: {sentimento}")
    print(f"Tarefa: {tarefa}")
    print(f"Foco: {foco}%")

    # Pode-se implementar lógica adicional aqui, como salvar em um banco de dados ou gerar uma recomendação
    

    # Retorna uma resposta de sucesso
    return jsonify({
        "message": "Dados recebidos com sucesso!",
        "dados": {
            "sentimento": sentimento,
            "tarefa": tarefa,
            "foco": foco
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)