import ast
import re
import json

def analisar_codigo(codigo, arquivo):
    vulnerabilidades = []
    
    try:
        tree = ast.parse(codigo)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ['eval', 'exec']: 
                    vulnerabilidades.append({"arquivo": arquivo, "tipo": "Uso de eval/exec (Execução de Código Arbitrário)"})
    except Exception as e:
        print(f"Erro ao analisar código: {e}")
    
    padrao_sql_injection = re.compile(r"SELECT\s+.*\s+FROM\s+.*\s+WHERE\s+.*=[^?%\s]+", re.IGNORECASE)
    if padrao_sql_injection.search(codigo):
        vulnerabilidades.append({"arquivo": arquivo, "tipo": "SQL Injection"})
    
    padrao_xss = re.compile(r"<script>.*</script>")
    if padrao_xss.search(codigo):
        vulnerabilidades.append({"arquivo": arquivo, "tipo": "Cross-Site Scripting (XSS)"})
    
    return vulnerabilidades

def salvar_resultados(vulnerabilidades):
    with open("resultados.json", "w") as f:
        json.dump(vulnerabilidades, f, indent=4)