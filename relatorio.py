from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from analise.security_analysis import detectar_sql_injection, detectar_xss, detectar_injecao_comando


def gerar_relatorio(codigo, nome_arquivo="relatorio.pdf"):
    c = canvas.Canvas(nome_arquivo, pagesize=letter)
    c.drawString(100, 750, "Relatório de Análise de Código Seguro")

    resultados = {
        "SQL Injection": detectar_sql_injection(codigo),
        "Cross-Site Scripting (XSS)": detectar_xss(codigo),
        "Injeção de Comando": detectar_injecao_comando(codigo)
    }

    y = 700
    for vulnerabilidade, resultado in resultados.items():
        c.drawString(100, y, f"{vulnerabilidade}: {resultado}")
        y -= 30

    c.save()
    print(f"Relatório salvo como {nome_arquivo}")

