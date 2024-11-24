import random
from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

# Configurações do banco de dados MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lyra'

mysql = MySQL(app)

#rota para fazer post do formulario de nova recomendaçao (em nova-recomendacao.html)

@app.route('/get-track', methods=['POST'])
def get_track():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    matricula = data.get('matricula')
    if not matricula:
        return jsonify({'error': 'No matricula provided'}), 400
    
    print(f"Matrícula recebida: {matricula}")

    sentimento = data.get('sentimento')  
    tarefa = data.get('tarefa')             
    foco = data.get('foco')

    if not sentimento:
        return jsonify({"error": "O campo 'sentimento' é obrigatório!"}), 400
    if not tarefa:
        return jsonify({"error": "O campo 'tarefa' é obrigatório!"}), 400
    if foco is None:
        return jsonify({"error": "O campo 'foco' é obrigatório!"}), 400

    try:
        foco = int(foco)
    except ValueError:
        return jsonify({"error": "O campo 'foco' deve ser um número válido!"}), 400

    print(f"Sentimento: {sentimento}, Tarefa: {tarefa}, Foco: {foco}")

    # Lógica de seleção de acordo com foco aqui"""
    if (foco>=0 and foco<=25):
        track_ids = [
            "0sZy1HE2aGBQABHfVRQ4jB",
            "3OnCnEWgy79xR5pr2kv4TX",
            "4fQMGlCawbTkH9yPPZ49kP",
            "3Wwy5wlxd8CpKMZGc4Mgjf",
            "5gJKsGij5oGt5H5RSFYXPa",
            "4zoQ3EqopTIGmK2c2rPV5t"
        ]
        track_id = random.choice(track_ids)

    elif(foco>=26 and foco<=50):
        track_ids = [
            "6hewgaPPeGRR4P92bEQZqg",
            "3gFQOMoUwlR6aUZj81gCzu",
            "2utLeUqNj7G7oSGpyhmVIa",
            "2ZJ28Rm7OXMYJshLtp5uff",
            "4RsL2ZlU4P0CIKDrOwQkzz"
        ]
        track_id = random.choice(track_ids)

    elif(foco>=51 and foco<=75):
        track_ids = [
            "1bW9h3vWoJVXyZK7em3noV",
            "2jTXrav9Voj0FpdT2yUIuH",
            "2vBuaUzWANdghLfM1nF0Yw",
            "6MfCnTGFIsqnR6yBAggaH4",
            "2XFnVjuPCnx4dkWwJkz4H9",
        ]
        track_id = random.choice(track_ids)

    elif(foco>=76 and foco<=100):
        track_ids = [
            "3d2oTExzu9dEhfCPXlpVXd",
            "6jdH1T167abmhAvIz0M3CR",
            "789WJxwUk6Pxb4AnqqnJlx",
            "6gj55yZkNA0UA9XDO4PXof",
            "1A9Zpwjpjz91R7lIACq5EG"
        ]

        track_id = random.choice(track_ids)
    else:
        return jsonify({"error": "Foco deve estar entre 0 e 100!"}), 400
    
    embed_url = f"https://open.spotify.com/embed/track/{track_id}"

    #Salvar id user e id musica recomendada no banco de dados 
    '''idUser = 1  # Substitua pela lógica real para obter o idUser
    idMusica = 1  # Substitua pela lógica real para obter o idMusica
    print(f"Inserindo no banco: idUser={idUser}, idMusica={idMusica}, data={datetime.now()}")'''

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE matricula = %s", (matricula,))
    idUser = cursor.fetchone()
    if not idUser:
        cursor.close()
        return jsonify({"error": "Usuário não encontrado!"}), 404
    idUser = idUser[0]

    cursor.execute("SELECT id FROM musicas WHERE link = %s", (f'https://open.spotify.com/embed/track/{track_id}',))
    idMusica = cursor.fetchone()

    cursor.execute("""
        INSERT INTO ouvidas (idUser, idMusica, data)
        VALUES (%s, %s, %s)
    """, (idUser, idMusica, datetime.now()))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"embed_url": embed_url}), 200
     

if __name__ == '__main__':
    app.run(debug=True)
    