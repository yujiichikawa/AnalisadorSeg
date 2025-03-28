import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from analise.security_analysis import analisar_codigo, salvar_resultados

REPOSITORIO = "./repository_exemplo" 
JSON_PATH = "resultados.json"

class MonitoramentoArquivos(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(('.py', '.java', '.c', '.cpp', '.js')):
            print(f"Arquivo modificado: {event.src_path}")
            atualizar_json(REPOSITORIO)  

def analisar_todos_os_arquivos(diretorio):
    print("Analisando todos os arquivos no início...")
    atualizar_json(diretorio) 

def atualizar_json(diretorio):
    """Reanalisa todos os arquivos e remove vulnerabilidades corrigidas do JSON"""
    vulnerabilidades_atualizadas = []

    for root, _, files in os.walk(diretorio):
        for file in files:
            if file.endswith(('.py', '.java', '.c', '.cpp', '.js')):
                caminho_arquivo = os.path.join(root, file)
                print(f"Analisando: {caminho_arquivo}")
                with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                    codigo = f.read()
                    vulnerabilidades_atualizadas.extend(analisar_codigo(codigo, caminho_arquivo))

    salvar_resultados(vulnerabilidades_atualizadas, sobrescrever=True) 

def salvar_resultados(vulnerabilidades, sobrescrever=False):
    
    if sobrescrever or not os.path.exists(JSON_PATH):
        dados_finais = vulnerabilidades
    else:
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                dados_antigos = json.load(f)
        except json.JSONDecodeError:
            print("Erro ao carregar JSON antigo, criando um novo.")
            dados_antigos = []

        dados_finais = [vuln for vuln in dados_antigos if vuln in vulnerabilidades]

    try:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(dados_finais, f, indent=4, ensure_ascii=False)
        print(f"Resultados atualizados em {JSON_PATH}!")
    except Exception as e:
        print(f"Erro ao salvar resultados: {e}")


analisar_todos_os_arquivos(REPOSITORIO)


monitor = MonitoramentoArquivos()
observador = Observer()
observador.schedule(monitor, path=REPOSITORIO, recursive=True)
observador.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observador.stop()
observador.join()
