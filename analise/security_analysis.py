import re
def detectar_sql_injection(codigo):
    padrao = re.compile(r"SELECT .* FROM .* WHERE .*=['\"]\w+['\"]")
    return "Possível SQL Injection detectado!" if padrao.search(codigo) else "SQL Injection: OK."

def detectar_xss(codigo):
    padrao = re.compile(r"<script>.*</script>")
    return "Possível Cross-Site Scripting detectado!" if padrao.search(codigo) else "Cross-Site Scripting: OK."

def detectar_injecao_comando(codigo):
    padrao = re.compile(r"system\(.*\)|exec\(.*\)|subprocess\.run\(.*\)")
    return "Possível Injeção de Comando detectada!" if padrao.search(codigo) else "Injeção de Comando: OK."