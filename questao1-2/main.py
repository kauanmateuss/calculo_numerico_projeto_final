from eliminacao_gauss import resolver_gauss

def main():
    print("=== Sistema Linear - Metodo de Gauss ===")

    try:
        n = int(input("Numero de equacoes/incognitas: "))

        if n <= 0:
            print("Digite um numero maior que zero.")
            return

        matriz = []

        print(f"Digite {n + 1} numeros por linha:")
        print("Coeficientes e termo independente.")
        print("Exemplo: 15 17 19 3890")

        for i in range(n):
            entrada = input(
                f"Equacao {i + 1}: "
            ).replace(",", ".").split()

            if len(entrada) != n + 1:
                print(f"Erro: digite {n + 1} numeros.")
                return

            linha = []

            for valor in entrada:
                linha.append(float(valor))

            matriz.append(linha)

        solucao = resolver_gauss(matriz)

        print("\nSolucao encontrada:")

        for i in range(n):
            print(f"x{i + 1} = {solucao[i]:.6g}")

    except ValueError as erro:
        print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
