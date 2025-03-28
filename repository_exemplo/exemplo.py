import sqlite3
from flask import Flask, request

app = Flask(__name__)

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

@app.route('/login', methods=['GET'])
def login():
    usuario = request.args.get("usuario")
    senha = request.args.get("senha")
    query = "SELECT * FROM usuarios WHERE usuario = '" + usuario + "' AND senha = '" + senha + "'"
    query = "SELECT * FROM usuarios WHERE usuario = '" + usuario + "' AND senha = '" + senha + "'"
    cursor.execute(query)
    resultado = cursor.fetchall()

    if resultado:
        return "Login bem-sucedido!"
    else:
        return "Credenciais inválidas."

if __name__ == '__main__':
    app.run(debug=True)