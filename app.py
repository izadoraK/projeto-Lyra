from binascii import Error
import os
import random
from flask import Flask, redirect, request, jsonify, send_from_directory, session, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS
import hashlib

app = Flask(__name__)
app.secret_key = "chave_secreta123"  
CORS(app)

# Configurações do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lyra'

mysql = MySQL(app)

@app.route('/')
def login_form():
    return redirect("login.html")  # Direciona para a página de login diretamente

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

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

        hashed_password = hash_password(senha)

        # Consulta para verificar credenciais
        cur = mysql.connection.cursor()
        query = """
            SELECT * FROM usuarios 
            WHERE matricula = %s AND email = %s AND senha = %s
        """
        cur.execute(query, (matricula, email, hashed_password))
        user = cur.fetchone()

        if user:
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
    #if 'user' in session:
        return redirect("index.html")  # Certifique-se de que index.html está acessível
   # else:
    #    return redirect(url_for('login_form'))

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

        # Verificar se a matrícula já existe no banco
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE matricula = %s", (matricula,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            return jsonify(message="Matrícula já cadastrada. Por favor, use uma matrícula diferente."), 409

        hashed_password = hash_password(senha)
        
        # Inserir no banco de dados
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (matricula, senha, email) VALUES (%s, %s, %s)", (matricula, hashed_password, email))
        mysql.connection.commit()
        cur.close()

        return jsonify(message="Usuário criado com sucesso!"), 201

    except Exception as e:
        return jsonify(message=f"Erro ao cadastrar usuário: {str(e)}"), 500
    
@app.route('/historico', methods=['POST'])
def get_historico():
    data = request.json
    matricula = data.get('matricula')
    print(f'Recebido matrícula: {matricula}')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE matricula = %s", (matricula,))
    idUser = cursor.fetchone()
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT ouvidas.data, musicas.nome, musicas.link FROM musicas JOIN ouvidas ON musicas.ID = ouvidas.idMusica WHERE ouvidas.idUser = %s", (idUser,))
        historico = cur.fetchall()
        cur.close()

        historico_list = []
        for row in historico:
            historico_list.append({
                'data': row[0],
                'nome': row[1],
                'link': row[2]
            })

        return jsonify(historico), 200

    except Exception as e:
        return jsonify(message=f"Erro ao buscar histórico: {str(e)}"), 500

@app.route('/suporte', methods=['POST'])
def create_suporte():
    try:
        data = request.json
        email = data.get('email')
        mensagem = data.get('message')

        if not email or not mensagem:
            return jsonify(message="Todos os campos são obrigatórios!"), 400

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO suporte (email, mensagem) VALUES (%s, %s)", (email, mensagem,))
        mysql.connection.commit()
        cur.close()

        return jsonify(message="Mensagem enviada com sucesso!"), 201

    except Exception as e:
        return jsonify(message=f"Erro ao enviar mensagem: {str(e)}"), 500

if __name__ == '__main__':
    app.run(debug=True)
