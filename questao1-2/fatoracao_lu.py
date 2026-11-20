from exibicao import TOLERANCIA, exibir_matriz, formatar_valor


def fatorar_lu(matriz, mostrar_passos=False):
    n = len(matriz)
    U = [linha[:n] for linha in matriz]
    b = [linha[n] for linha in matriz]
    L = [[0.0] * n for _ in range(n)]
    permutacao = list(range(n))

    for i in range(n):
        L[i][i] = 1.0

    if mostrar_passos:
        print("\n--- Fatoracao LU ---")
        exibir_matriz([linha[:] for linha in matriz], "Matriz aumentada inicial [A|b]:")

    # Fatoracao
    for k in range(n):
        linha_pivo = k

        for i in range(k + 1, n):
            if abs(U[i][k]) > abs(U[linha_pivo][k]):
                linha_pivo = i

        if abs(U[linha_pivo][k]) < TOLERANCIA:
            raise ValueError("O sistema nao possui solucao unica (pivo nulo).")

        if linha_pivo != k:
            U[k], U[linha_pivo] = U[linha_pivo], U[k]
            b[k], b[linha_pivo] = b[linha_pivo], b[k]
            permutacao[k], permutacao[linha_pivo] = (
                permutacao[linha_pivo],
                permutacao[k],
            )

            # A troca de linhas tambem troca os multiplicadores ja calculados
            for j in range(k):
                L[k][j], L[linha_pivo][j] = L[linha_pivo][j], L[k][j]

            if mostrar_passos:
                print(f"Troca de linhas: L{k + 1} <-> L{linha_pivo + 1}")

        for i in range(k + 1, n):
            L[i][k] = U[i][k] / U[k][k]

            if mostrar_passos:
                print(
                    f"Multiplicador L{i + 1}{k + 1} = "
                    f"{formatar_valor(L[i][k])}"
                )

            for j in range(k, n):
                U[i][j] -= L[i][k] * U[k][j]

            U[i][k] = 0.0

        if mostrar_passos:
            exibir_matriz(U, "Matriz U parcial:")

    if mostrar_passos:
        exibir_matriz(L, "Matriz L:")
        exibir_matriz(U, "Matriz U:")

    return {
        "L": L,
        "U": U,
        "b": b,
        "permutacao": permutacao,
        "n": n,
    }


def resolver_lu(matriz, mostrar_passos=False):
    fatoracao = fatorar_lu(matriz, mostrar_passos)

    L = fatoracao["L"]
    U = fatoracao["U"]
    b = fatoracao["b"]
    n = fatoracao["n"]

    y = [0.0] * n

    if mostrar_passos:
        print("Substituicao direta (L*y = P*b):")

    for i in range(n):
        soma = 0.0

        for j in range(i):
            soma += L[i][j] * y[j]

        y[i] = b[i] - soma

        if mostrar_passos:
            print(f"  y{i + 1} = {formatar_valor(y[i])}")

    x = [0.0] * n

    if mostrar_passos:
        print("Retrossubstituicao (U*x = y):")

    for i in range(n - 1, -1, -1):
        soma = 0.0

        for j in range(i + 1, n):
            soma += U[i][j] * x[j]

        x[i] = (y[i] - soma) / U[i][i]

        if mostrar_passos:
            print(f"  x{i + 1} = {formatar_valor(x[i])}")

    return x
