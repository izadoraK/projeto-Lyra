from flask import Flask, request, jsonify, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"  # Substitua por uma chave secreta segura
CORS(app)  # Permitir acesso de origem cruzada (necessário para uso com fetch)

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",  # Substitua pelo seu usuário do banco de dados
    "password": "",  # Substitua pela sua senha
    "database": "lyra"
}

# Rota para exibir o formulário de login (opcional para renderização direta)
@app.route('/')
def login_form():
    return redirect("login.html")  # Direciona para a página de login diretamente

# Rota para processar o login
@app.route('/login', methods=['POST'])
def login():
    # Recebe os dados enviados no corpo da requisição
    data = request.json
    matricula = data.get("matricula")
    email = data.get("email")
    senha = data.get("senha")

    # Verifica se os campos foram preenchidos
    if not matricula or not email or not senha:
        return jsonify({"message": "Preencha todos os campos"}), 400

    try:
        # Conecta ao banco de dados
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            # Consulta para verificar credenciais
            query = """
                SELECT * FROM usuarios 
                WHERE matricula = %s AND email = %s AND senha = %s
            """
            cursor.execute(query, (matricula, email, senha))
            user = cursor.fetchone()  # Retorna a primeira linha, ou None se não houver

            if user:
                # Armazena informações do usuário na sessão
                session['user'] = user['matricula']
                return jsonify({"message": "Login bem-sucedido"}), 200
            else:
                return jsonify({"message": "Credenciais inválidas, digite corretamente"}), 401

    except Error as e:
        # Retorna erro caso ocorra no banco de dados
        return jsonify({"message": f"Erro no banco de dados: {str(e)}"}), 500

    finally:
        # Fecha a conexão com o banco de dados
        if connection.is_connected():
            cursor.close()
            connection.close()

# Rota para página inicial (opcional, se renderizar diretamente)
@app.route('/index')
def index():
    if 'user' in session:
        return redirect("index.html")  # Certifique-se de que index.html está acessível
    else:
        return redirect(url_for('login_form'))

# Rota para logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login_form'))

if __name__ == '__main__':
    app.run(debug=True)