import math

TOLERANCIA_RELATIVA = 1e-9


def calcular_erro_residual(matriz, solucao):
    n = len(matriz)
    residuos = []

    for i in range(n):
        soma = 0.0

        for j in range(n):
            soma += matriz[i][j] * solucao[j]

        residuos.append(matriz[i][n] - soma)

    norma_infinita = max(abs(residuo) for residuo in residuos)
    norma_2 = math.sqrt(sum(residuo ** 2 for residuo in residuos))
    norma_b = max(abs(matriz[i][n]) for i in range(n))

    if norma_b > 0:
        erro_relativo = norma_infinita / norma_b
    else:
        erro_relativo = norma_infinita

    return {
        "residuos": residuos,
        "norma_infinita": norma_infinita,
        "norma_2": norma_2,
        "norma_b": norma_b,
        "erro_relativo": erro_relativo,
    }


def exibir_erro_residual(matriz, solucao):
    resultado = calcular_erro_residual(matriz, solucao)

    print("\nErro residual (r = b - A*x):")

    for i, residuo in enumerate(resultado["residuos"]):
        print(f"  r{i + 1} = {residuo:+.6e}")

    print(f"  ||r||_infinito = {resultado['norma_infinita']:.6e}")
    print(f"  ||r||_2        = {resultado['norma_2']:.6e}")
    print(f"  erro relativo  = {resultado['erro_relativo']:.6e}")

    if resultado["erro_relativo"] <= TOLERANCIA_RELATIVA:
        print("  A solucao satisfaz o sistema original.")
    else:
        print("  Atencao: a solucao pode estar imprecisa.")

    return resultado


if __name__ == "__main__":
    matriz = [
        [15.0, 17.0, 19.0, 3890.0],
        [0.30, 0.40, 0.55, 95.0],
        [1.00, 1.20, 1.50, 282.0],
    ]
    solucao = [90.0, 60.0, 80.0]

    exibir_erro_residual(matriz, solucao)
