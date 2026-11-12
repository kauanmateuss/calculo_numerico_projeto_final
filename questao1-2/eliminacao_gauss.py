from exibicao import TOLERANCIA, exibir_matriz, formatar_valor


def resolver_gauss(matriz, mostrar_passos=False):
    """Resolve um sistema linear pelo metodo da eliminacao de Gauss.

    A matriz deve estar na forma aumentada [A | b].
    O parametro mostrar_passos imprime as operacoes realizadas.
    """
    n = len(matriz)
    A = [linha[:] for linha in matriz]

    if mostrar_passos:
        print("\n--- Eliminacao de Gauss ---")
        exibir_matriz(A, "Matriz aumentada inicial [A|b]:")

    # 1. Eliminacao (com pivoteamento parcial)
    for k in range(n):
        linha_pivo = k

        for i in range(k + 1, n):
            if abs(A[i][k]) > abs(A[linha_pivo][k]):
                linha_pivo = i

        if abs(A[linha_pivo][k]) < TOLERANCIA:
            raise ValueError("O sistema nao possui solucao unica (pivo nulo).")

        if mostrar_passos:
            print(
                f"Etapa {k + 1}: pivo na coluna {k + 1} = "
                f"{formatar_valor(A[linha_pivo][k])}"
            )

        if linha_pivo != k:
            A[k], A[linha_pivo] = A[linha_pivo], A[k]

            if mostrar_passos:
                print(f"  Troca de linhas: L{k + 1} <-> L{linha_pivo + 1}")

        for i in range(k + 1, n):
            multiplicador = A[i][k] / A[k][k]

            if mostrar_passos:
                print(
                    f"  L{i + 1} = L{i + 1} - "
                    f"({formatar_valor(multiplicador)}) * L{k + 1}"
                )

            for j in range(k, n + 1):
                A[i][j] -= multiplicador * A[k][j]

            A[i][k] = 0.0

        if mostrar_passos:
            exibir_matriz(A)

    # 2. Retrossubstituicao
    x = [0.0] * n

    if mostrar_passos:
        print("Retrossubstituicao:")

    for i in range(n - 1, -1, -1):
        soma = 0.0

        for j in range(i + 1, n):
            soma += A[i][j] * x[j]

        x[i] = (A[i][n] - soma) / A[i][i]

        if mostrar_passos:
            print(f"  x{i + 1} = {formatar_valor(x[i])}")

    return x
