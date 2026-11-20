from exibicao import TOLERANCIA, exibir_matriz, formatar_valor


def resolver_jordan(matriz, mostrar_passos=False):
    n = len(matriz)
    A = [linha[:] for linha in matriz]

    if mostrar_passos:
        print("\n--- Eliminacao de Gauss-Jordan ---")
        exibir_matriz(A, "Matriz aumentada inicial [A|b]:")

    for k in range(n):
        # Pivoteamento parcial
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

        pivo = A[k][k]

        for j in range(k, n + 1):
            A[k][j] /= pivo

        if mostrar_passos:
            print(f"  L{k + 1} = L{k + 1} / ({formatar_valor(pivo)})")

        for i in range(n):
            if i == k:
                continue

            multiplicador = A[i][k]

            if abs(multiplicador) < TOLERANCIA:
                A[i][k] = 0.0
                continue

            for j in range(k, n + 1):
                A[i][j] -= multiplicador * A[k][j]

            A[i][k] = 0.0

            if mostrar_passos:
                print(
                    f"  L{i + 1} = L{i + 1} - "
                    f"({formatar_valor(multiplicador)}) * L{k + 1}"
                )

        if mostrar_passos:
            exibir_matriz(A)

    solucao = [A[i][n] for i in range(n)]

    if mostrar_passos:
        print("A matriz final e [I|x], portanto a solucao ja esta isolada.")

    return solucao
