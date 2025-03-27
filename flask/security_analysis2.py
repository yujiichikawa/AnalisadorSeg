import re

def analisar_codigo(codigo):
    vulnerabilidades = []

    padrao_sql_injection = re.compile(r"SELECT\s+.*\s+FROM\s+.*\s+WHERE\s+.*=.*['\"].*['\"]", re.IGNORECASE)

    if padrao_sql_injection.search(codigo):
        vulnerabilidades.append("SQL Injection")
    padrao_xss = re.compile(r"<script>.*</script>")
    if padrao_xss.search(codigo):
        vulnerabilidades.append("Cross-Site Scripting (XSS)")

    return vulnerabilidades