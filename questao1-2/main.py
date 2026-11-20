from eliminacao_gauss import resolver_gauss
from eliminacao_jordan import resolver_jordan
from erro_residual import exibir_erro_residual
from fatoracao_lu import resolver_lu

METODOS = {
    "1": ("Eliminacao de Gauss", resolver_gauss),
    "2": ("Eliminacao de Gauss-Jordan", resolver_jordan),
    "3": ("Fatoracao LU", resolver_lu),
}


def dados_problema():
    return [
        [15.0, 17.0, 19.0, 3890.0],  # metal
        [0.30, 0.40, 0.55, 95.0],    # plastico
        [1.00, 1.20, 1.50, 282.0],   # borracha
    ]


def exibir_solucao(solucao):
    print("\nSolucao encontrada:")

    for i, valor in enumerate(solucao):
        print(f"  x{i + 1} = {valor:.6g}")


def perguntar_sim_nao(mensagem):
    resposta = input(mensagem).strip().lower()
    return resposta in ("s", "sim", "y", "yes")


def ler_sistema():
    try:
        n = int(input("Numero de equacoes/incognitas: "))
    except ValueError:
        print("Erro: digite um numero inteiro.")
        return None

    if n <= 0:
        print("Erro: digite um numero maior que zero.")
        return None

    matriz = []

    print(f"\nDigite {n + 1} numeros por linha: os coeficientes e o termo independente.")
    print("Exemplo: 15 17 19 3890")

    for i in range(n):
        while True:
            entrada = input(f"Equacao {i + 1}: ").replace(",", ".").split()

            if len(entrada) != n + 1:
                print(f"Erro: digite exatamente {n + 1} numeros.")
                continue

            try:
                linha = [float(valor) for valor in entrada]
            except ValueError:
                print("Erro: use apenas numeros.")
                continue

            matriz.append(linha)
            break

    return matriz


def escolher_metodo():
    print("\nMetodos disponiveis:")
    print("  1 - Eliminacao de Gauss")
    print("  2 - Eliminacao de Gauss-Jordan")
    print("  3 - Fatoracao LU")
    print("  4 - Comparar os tres metodos")
    print("  0 - Sair")

    opcao = input("Opcao: ").strip()

    if opcao == "0":
        return []
    if opcao == "4":
        return list(METODOS.keys())
    if opcao in METODOS:
        return [opcao]

    print("Opcao invalida.")
    return None


def executar_metodo(nome, funcao, matriz, mostrar_passos):
    print(f"\n=== {nome} ===")

    try:
        solucao = funcao(matriz, mostrar_passos=mostrar_passos)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return None

    exibir_solucao(solucao)
    exibir_erro_residual(matriz, solucao)
    return solucao


def main():
    print("=== Sistema Linear - Metodos Diretos ===")

    while True:
        print("\nDados de entrada:")
        print("  1 - Usar o problema dos componentes eletricos")
        print("  2 - Digitar um sistema")
        print("  0 - Sair")

        opcao = input("Opcao: ").strip()

        if opcao == "0":
            print("Encerrando.")
            return

        if opcao == "1":
            matriz = dados_problema()
            print("\nSistema montado (materiais em gramas):")
            print("  15*x1 + 17*x2 + 19*x3 = 3890")
            print("  0.30*x1 + 0.40*x2 + 0.55*x3 = 95")
            print("  1.00*x1 + 1.20*x2 + 1.50*x3 = 282")
            break

        if opcao == "2":
            matriz = ler_sistema()

            if matriz is not None:
                break

            continue

        print("Opcao invalida.")

    metodos_escolhidos = escolher_metodo()

    if metodos_escolhidos is None:
        return

    if not metodos_escolhidos:
        print("Encerrando.")
        return

    mostrar_passos = perguntar_sim_nao(
        "\nMostrar as etapas da resolucao? [s/N]: "
    )

    for chave in metodos_escolhidos:
        nome, funcao = METODOS[chave]
        executar_metodo(nome, funcao, matriz, mostrar_passos)


if __name__ == "__main__":
    main()
