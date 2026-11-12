def resolver_gauss(matriz):
    n = len(matriz)

    # 1. Eliminacao de Gauss
    for k in range(n):

        # Escolhe o maior pivo na coluna atual
        linha_pivo = k

        for i in range(k + 1, n):
            if abs(matriz[i][k]) > abs(matriz[linha_pivo][k]):
                linha_pivo = i

        if abs(matriz[linha_pivo][k]) < 1e-12:
            raise ValueError("O sistema nao possui solucao unica.")

        # Troca as linhas, se necessario
        matriz[k], matriz[linha_pivo] = matriz[linha_pivo], matriz[k]

        # Zera os elementos abaixo do pivo
        for i in range(k + 1, n):
            multiplicador = matriz[i][k] / matriz[k][k]

            for j in range(k, n + 1):
                matriz[i][j] -= multiplicador * matriz[k][j]

    # 2. Retrossubstituicao
    x = [0.0] * n

    for i in range(n - 1, -1, -1):
        soma = 0.0

        for j in range(i + 1, n):
            soma += matriz[i][j] * x[j]

        x[i] = (matriz[i][n] - soma) / matriz[i][i]

    return x
