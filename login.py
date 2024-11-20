from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"  # Substitua por uma chave secreta segura

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",       # Substitua pelo seu usuário do banco de dados
    "password": "",  # Substitua pela sua senha
    "database": "lyra"
}

# Rota para exibir o formulário de login (se necessário)
@app.route('/')
def login_form():
    return render_template("login.html")  # Certifique-se de que "login.html" está no diretório "templates"

# Rota para processar o login
@app.route('/login', methods=['POST'])
def login():
    matricula = request.form.get("matricula")
    email = request.form.get("email")
    senha = request.form.get("senha")
    
    try:
        # Conectando ao banco de dados
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # Consulta para validar as credenciais
            query = """
                SELECT * FROM usuarios 
                WHERE matricula = %s AND email = %s AND senha = %s
            """
            cursor.execute(query, (matricula, email, senha))
            user = cursor.fetchone()
            
            if user:
                session['user'] = user['matricula']
                return jsonify({"message": "Login bem-sucedido", "user": user})
            else:
                return jsonify({"error": "Credenciais inválidas"}), 401
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Rota para logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login_form'))

if __name__ == '__main__':
    app.run(debug=True)