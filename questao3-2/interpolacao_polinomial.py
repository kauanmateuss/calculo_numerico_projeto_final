import os


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def selecionar_pontos_mais_proximos(x_dados, y_dados, x_alvo, grau):
    pontos = list(zip(x_dados, y_dados))

    # Ordena pela distância até o alvo para escolher os pontos mais próximos
    pontos_ordenados = sorted(pontos, key=lambda ponto: abs(ponto[0] - x_alvo))

    quantidade_pontos = grau + 1
    pontos_selecionados = pontos_ordenados[:quantidade_pontos]

    x_sel = [p[0] for p in pontos_selecionados]
    y_sel = [p[1] for p in pontos_selecionados]

    return x_sel, y_sel


def interpolacao_lagrange(x, y, x_alvo):
    n = len(x)
    resultado = 0.0

    for k in range(n):
        termo_L = 1.0

        for j in range(n):
            # Pula o próprio ponto para não dividir por zero
            if k != j:
                termo_L *= (x_alvo - x[j]) / (x[k] - x[j])

        resultado += y[k] * termo_L

    return resultado


def interpolacao_newton(x, y, x_alvo):
    n = len(x)

    # Tabela de diferenças divididas
    tabela = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        tabela[i][0] = y[i]

    for j in range(1, n):
        for i in range(n - j):
            numerador = tabela[i + 1][j - 1] - tabela[i][j - 1]
            denominador = x[i + j] - x[i]
            tabela[i][j] = numerador / denominador

    resultado = tabela[0][0]
    produto_termos = 1.0

    for j in range(1, n):
        produto_termos *= x_alvo - x[j - 1]
        resultado += tabela[0][j] * produto_termos

    return resultado


def exibir_resultados(x_dados, y_dados, x_alvo):
    max_grau_possivel = len(x_dados) - 1

    print("\n" + "=" * 65)
    print(f"resultados da interpolação para x = {x_alvo}")
    print("=" * 65)
    print(
        f"{'grau':<6} | {'lagrange (v)':<15} | {'newton (v)':<15} | {'pontos base utilizados (i)'}"
    )
    print("-" * 65)

    # Testa do grau 2 ao 4
    grau_final = min(4, max_grau_possivel)

    if grau_final < 2:
        print(
            "erro: são necessários pelo menos 3 pontos para calcular a partir do 2º grau."
        )
        return

    for grau in range(2, grau_final + 1):
        x_sel, y_sel = selecionar_pontos_mais_proximos(
            x_dados, y_dados, x_alvo, grau
        )

        res_lagrange = interpolacao_lagrange(x_sel, y_sel, x_alvo)
        res_newton = interpolacao_newton(x_sel, y_sel, x_alvo)

        pontos_str = ", ".join(str(val) for val in sorted(x_sel))

        print(
            f"{grau}º     | {res_lagrange:<15.6f} | {res_newton:<15.6f} | [{pontos_str}]"
        )

    print("=" * 65 + "\n")


def inserir_novos_dados():
    print("\n--- entrada de novos dados ---")
    while True:
        try:
            qtd = int(input("quantos pontos a tabela possui?: "))
            if qtd < 3:
                print(
                    "por favor, insira pelo menos 3 pontos para permitir polinômios de 2º grau."
                )
                continue
            break
        except ValueError:
            print("entrada inválida! digite um número inteiro.")

    x_novos = []
    y_novos = []

    print("\ndigite os valores usando ponto para casas decimais:")
    for i in range(qtd):
        while True:
            try:
                x_val = float(input(f"  ponto {i+1} - valor de x: "))
                if x_val in x_novos:
                    print(
                        "  erro: esse valor de x já foi inserido. os valores de x devem ser distintos."
                    )
                    continue
                y_val = float(input(f"  ponto {i+1} - valor de y: "))
                x_novos.append(x_val)
                y_novos.append(y_val)
                break
            except ValueError:
                print("  entrada inválida! digite apenas números.")

    while True:
        try:
            alvo = float(input("\nqual valor de x deseja estimar?: "))
            break
        except ValueError:
            print("entrada inválida! digite um número.")

    return x_novos, y_novos, alvo


def main():
    # Dados do problema
    x_padrao = [0.25, 0.75, 1.25, 1.5, 2.0]
    y_padrao = [-0.45, -0.60, 0.70, 1.88, 6.0]
    alvo_padrao = 1.15

    while True:
        print("\n=======================================================")
        print("  cálculo numérico - interpolação  ")
        print("=======================================================")
        print("1 - resolver o problema proposto na lista")
        print("2 - inserir novos dados")
        print("3 - sair do programa")

        opcao = input("\nescolha uma opção: ").strip()

        if opcao == "1":
            print("\ncarregando dados da tabela do ensaio de laboratório...")
            exibir_resultados(x_padrao, y_padrao, alvo_padrao)
            input("pressione enter para voltar ao menu...")
            limpar_tela()

        elif opcao == "2":
            x_custom, y_custom, alvo_custom = inserir_novos_dados()
            exibir_resultados(x_custom, y_custom, alvo_custom)
            input("pressione enter para voltar ao menu...")
            limpar_tela()

        elif opcao == "3":
            print("\nencerrando o programa. bom trabalho na apresentação!")
            break

        else:
            print("\nopção inválida! tente novamente.")


if __name__ == "__main__":
    main()
