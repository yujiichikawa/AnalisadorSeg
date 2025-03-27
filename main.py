from lexer import lexer
from analise.security_analysis import detectar_sql_injection, detectar_xss,detectar_injecao_comando
from relatorio import gerar_relatorio

#codigo = "SELECT * FROM users WHERE username='admin'"
#codigo = "<script>alert("")</script>"
codigo = "System.exec()"

print("--- Analisando Código ---")
lexer.input(codigo)
for token in lexer:
    print(token)

print("\n--- Verificação de Segurança ---")
print(detectar_sql_injection(codigo))
print(detectar_xss(codigo))
print(detectar_injecao_comando(codigo))
gerar_relatorio(codigo)

