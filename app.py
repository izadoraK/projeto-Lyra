import base64
import os
import random
from flask import Flask, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configurações do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lyra'

mysql = MySQL(app)

# Lista de faixas
track_ids = [
    "6wT447V5gCK7mXjuUGpouU"
]

@app.route("/get-track", methods=["GET"])
def get_track():
    track_id = random.choice(track_ids)
    embed_url = f"https://open.spotify.com/embed/track/{track_id}"
    return jsonify({"embed_url": embed_url})

# Rota para cadastrar os usuários
@app.route('/usuarios', methods=['POST'])
def create_user():
    try:
        # Capturar os dados do JSON enviado
        data = request.json
        matricula = data.get('matricula')
        email = data.get('email')
        senha = data.get('senha')

        # Verificar se todos os campos foram enviados
        if not matricula or not email or not senha:
            return jsonify(message="Todos os campos são obrigatórios!"), 400

        # Inserir no banco de dados
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (matricula, senha, email) VALUES (%s, %s, %s)", (matricula, senha, email))
        mysql.connection.commit()
        cur.close()

        return jsonify(message="Usuário criado com sucesso!"), 201

    except Exception as e:
        return jsonify(message=f"Erro ao cadastrar usuário: {str(e)}"), 500



if __name__ == '__main__':
    app.run(debug=True)