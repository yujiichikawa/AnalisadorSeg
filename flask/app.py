from flask import Flask, render_template
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from collections import Counter
from security_analysis2 import analisar_codigo
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time
import os

app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, routes_pathname_prefix='/dash/')

vulnerabilidades_detectadas = []

class MonitoramentoArquivos(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(('.py', '.java', '.c', '.cpp', '.js')):
            with open(event.src_path, 'r', encoding='utf-8', errors='ignore') as f:
                codigo = f.read()
                vulnerabilidades_detectadas.extend(analisar_codigo(codigo))

repositorio_projeto = "./repository_exemplo"
monitor = MonitoramentoArquivos()
observador = Observer()
observador.schedule(monitor, path=repositorio_projeto, recursive=True)
observador.start()

def atualizar_dash():
    while True:
        contagem = Counter(vulnerabilidades_detectadas)
        df = pd.DataFrame(list(contagem.items()), columns=['Tipo de Vulnerabilidade', 'Ocorrências'])
        fig = px.bar(df, x='Tipo de Vulnerabilidade', y='Ocorrências', title='Análise de Código')
        dash_app.layout = html.Div(children=[
            html.H1(""),
            dcc.Graph(figure=fig)
        ])
        time.sleep(5)

threading.Thread(target=atualizar_dash, daemon=True).start()

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)