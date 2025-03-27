import matplotlib.pyplot as plt
from collections import Counter
from lexer import lexer
from analise.security_analysis import detectar_sql_injection, detectar_xss, detectar_injecao_comando


def gerar_grafico(codigo):
    lexer.input(codigo)
    tipos_tokens = [token.type for token in lexer]
    contagem = Counter(tipos_tokens)

    plt.figure(figsize=(8, 5))
    plt.bar(contagem.keys(), contagem.values(), color=['blue', 'red', 'green', 'orange'])
    plt.xlabel("Tipos de Tokens")
    plt.ylabel("Quantidade")
    plt.title("Distribuição de Tokens no Código")
    plt.show()

    print("\n--- Verificação de Segurança ---")
    print(detectar_sql_injection(codigo))
    print(detectar_xss(codigo))
    print(detectar_injecao_comando(codigo))


if __name__ == "__main__":
    codigo_teste = "<script>alert('Hacked!');</script>"
    gerar_grafico(codigo_teste)