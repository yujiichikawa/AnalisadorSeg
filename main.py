from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

from analise.security_analysis import analisar_codigo, salvar_resultados

vulnerabilidades_detectadas = []

class MonitoramentoArquivos(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(('.py', '.java', '.c', '.cpp', '.js')):
            with open(event.src_path, 'r', encoding='utf-8', errors='ignore') as f:
                codigo = f.read()
                vulnerabilidades_detectadas.extend(analisar_codigo(codigo, event.src_path))
                
                # Exibir resultados no terminal
                for vuln in vulnerabilidades_detectadas:
                    print(f"[!] {vuln['tipo']} encontrado no arquivo {vuln['arquivo']}")
                
                # Salvar em JSON
                salvar_resultados(vulnerabilidades_detectadas)

monitor = MonitoramentoArquivos()
observador = Observer()
observador.schedule(monitor, path="./repository_exemplo", recursive=True)
observador.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observador.stop()
observador.join()