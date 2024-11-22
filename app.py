import base64
from binascii import Error
import os
import random
from flask import Flask, redirect, request, jsonify, send_from_directory, session, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS
import bcrypt


app = Flask(__name__)
app.secret_key = "chave_secreta123"  
CORS(app)

# Configurações do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lyra'

mysql = MySQL(app)

# Faixa quando abre o site
track_ids = [
    "6wT447V5gCK7mXjuUGpouU"
]

@app.route("/get-initial-track", methods=["GET"])
def get_initial_track():
    track_id = random.choice(track_ids)
    embed_url = f"https://open.spotify.com/embed/track/{track_id}"
    return jsonify({"embed_url": embed_url})

@app.route('/')
def login_form():
    return redirect("login.html")  # Direciona para a página de login diretamente

# Rota para processar o login
@app.route('/login', methods=['POST'])
def login():
    try:
        # Recebe os dados enviados no corpo da requisição
        data = request.json
        matricula = data.get("matricula")
        email = data.get("email")
        senha = data.get("senha")

        # Verifica se os campos foram preenchidos
        if not matricula or not email or not senha:
            return jsonify({"message": "Preencha todos os campos"}), 400

        # Consulta para verificar credenciais
        cur = mysql.connection.cursor()
        query = """
            SELECT * FROM usuarios 
            WHERE matricula = %s AND email = %s AND senha = %s
        """
        cur.execute(query, (matricula, email, senha))
        user = cur.fetchone()

        if user and bcrypt.checkpw(senha.encode('utf-8'), user[0].encode('utf-8')):
            # Armazena informações do usuário na sessão
            session['user'] = matricula
            return jsonify({"message": "Login bem-sucedido"}), 200
        else:
            return jsonify({"message": "Credenciais inválidas, digite corretamente"}), 401

    except Exception as e:
        return jsonify({"message": f"Erro no banco de dados: {str(e)}"}), 500

    finally:
        cur.close()

# Rota para página inicial (opcional, se renderizar diretamente)
@app.route('/index')
def index():
    if 'user' in session:
        return redirect("index.html")  # Certifique-se de que index.html está acessível
    else:
        return redirect(url_for('login_form'))

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

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), salt)
        
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