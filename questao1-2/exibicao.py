TOLERANCIA = 1e-12


def formatar_valor(valor):
    if abs(valor) < 1e-10:
        valor = 0.0

    texto = f"{valor:.4f}".rstrip("0").rstrip(".")

    if texto in ("", "-0"):
        texto = "0"

    return texto


def exibir_matriz(matriz, titulo=None):
    if titulo:
        print(titulo)

    linhas = [[formatar_valor(valor) for valor in linha] for linha in matriz]

    if not linhas:
        print()
        return

    largura = max(len(valor) for linha in linhas for valor in linha)

    for linha in linhas:
        conteudo = "  ".join(valor.rjust(largura) for valor in linha)
        print(f"  [ {conteudo} ]")

    print()
