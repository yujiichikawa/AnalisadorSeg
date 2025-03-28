import ast
import re
import json
import os

def analisar_codigo(codigo, arquivo):
    vulnerabilidades = []
    
    try:
        tree = ast.parse(codigo)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ['eval', 'exec']: 
                    vulnerabilidades.append({"arquivo": arquivo, "tipo": "Uso de eval/exec"})
    except Exception as e:
        print(f"Erro ao analisar código: {e}")
    
    padrao_sql_injection = re.compile(r"SELECT\s+.+?\s+FROM\s+.+?\s+WHERE\s+.+?=.*?['\"].*?(AND|OR)?.*?['\"]?", re.IGNORECASE)
    if padrao_sql_injection.search(codigo):
        vulnerabilidades.append({"arquivo": arquivo, "tipo": "Possível SQL Injection"})
    
    padrao_xss = re.compile(r"<script[^>]*>.*?</script>", re.IGNORECASE)
    if padrao_xss.search(codigo):
        vulnerabilidades.append({"arquivo": arquivo, "tipo": "Possível Cross-Site Scripting"})
    
    return vulnerabilidades

def salvar_resultados(vulnerabilidades):
    if not vulnerabilidades:
        return
    
    caminho_json = "resultados.json"

    if os.path.exists(caminho_json):
        try:
            with open(caminho_json, "r", encoding="utf-8") as f:
                dados_antigos = json.load(f)
        except json.JSONDecodeError:
            print("Erro ao carregar JSON antigo, criando um novo.")
            dados_antigos = []
    else:
        dados_antigos = []

    # Convertendo para um conjunto para evitar duplicatas
    set_vulnerabilidades = {json.dumps(vuln, sort_keys=True) for vuln in dados_antigos}  
    for vuln in vulnerabilidades:
        set_vulnerabilidades.add(json.dumps(vuln, sort_keys=True))

    # Convertendo de volta para lista
    dados_finais = [json.loads(vuln) for vuln in set_vulnerabilidades]

    try:
        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(dados_finais, f, indent=4, ensure_ascii=False)
        print(f"Resultados salvos em {caminho_json} sem duplicatas!")
    except Exception as e:
        print(f"Erro ao salvar resultados: {e}")