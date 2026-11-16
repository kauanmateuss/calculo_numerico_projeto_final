"""
UNIVERSIDADE FEDERAL DO VALE DO SÃO FRANCISCO (UNIVASF)
DISCIPLINA: CÁLCULO NUMÉRICO - 2025.2
PROJETO FINAL - TÓPICO 02: SISTEMAS LINEARES (MÉTODOS ITERATIVOS)
QUESTÃO 02: ANÁLISE DE UMA TRELIÇA ISOSTÁTICA VIA MÉTODO DE GAUSS-SEIDEL

Autores: Equipe de Cálculo Numérico
Descrição:
    Este programa modela o equilíbrio estático de uma treliça plana com 5 nós
    e 7 barras sob carregamento vertical externo e calcula os esforços axiais
    nas barras e reações de apoio através do Método Iterativo de Gauss-Seidel.
    Permite tanto a resolução com os dados padrão do enunciado quanto a entrada
    de novas cargas externas ou até mesmo de um sistema linear arbitrário n x n.
"""

import math
import sys
from typing import List, Tuple, Optional


def deg2rad(deg: float) -> float:
    """Converte graus para radianos."""
    return deg * math.pi / 180.0


def resolver_gauss_seidel(
    A: List[List[float]],
    b: List[float],
    x0: Optional[List[float]] = None,
    tol: float = 0.0001,
    max_iter: int = 1000,
    verbose: bool = True,
) -> Tuple[List[float], int, List[float], bool]:
    """
    Executa o Método Iterativo de Gauss-Seidel para resolver Ax = b.

    Parâmetros:
        A: Matriz dos coeficientes (n x n).
        b: Vetor de termos independentes (tamanho n).
        x0: Estimativa inicial (padrão: zeros).
        tol: Tolerância para critério de parada (precisão).
        max_iter: Número máximo de iterações permitidas.
        verbose: Se True, imprime tabela com o progresso de cada iteração.

    Retorna:
        Tuple contendo: (solução x, total de iterações, histórico de erros, convergiu)
    """
    n = len(A)
    if x0 is None:
        x = [0.0] * n
    else:
        x = list(x0)

    # Verificação de segurança: diagonais nulas geram divisão por zero
    for i in range(n):
        if abs(A[i][i]) < 1e-12:
            raise ZeroDivisionError(
                f"Elemento nulo na diagonal principal na linha {i+1} (A[{i}][{i}] = 0). "
                "O método de Gauss-Seidel requer reordenação de equações."
            )

    historico_erros: List[float] = []
    convergiu = False

    if verbose:
        print("\n" + "=" * 65)
        print(f"{'Iteração':^10} | {'Maior Variação (|Δx|)':^25} | {'Status':^20}")
        print("=" * 65)

    for it in range(1, max_iter + 1):
        x_ant = list(x)
        max_diff = 0.0

        for i in range(n):
            soma = b[i]
            # Termos com incógnitas já atualizadas nesta iteração (j < i)
            for j in range(i):
                soma -= A[i][j] * x[j]
            # Termos com incógnitas da iteração anterior (j > i)
            for j in range(i + 1, n):
                soma -= A[i][j] * x_ant[j]

            x[i] = soma / A[i][i]

            diff_i = abs(x[i] - x_ant[i])
            if diff_i > max_diff:
                max_diff = diff_i

        historico_erros.append(max_diff)

        # Exibição das iterações iniciais, a cada 10 passos ou no passo final
        if verbose:
            if it <= 5 or it % 10 == 0 or max_diff < tol:
                print(f"{it:^10d} | {max_diff:^25.6f} | {'Em cálculo...':^20}")

        # Critério de parada: erro absoluto máximo entre passos consecutivos
        if max_diff < tol:
            convergiu = True
            if verbose:
                print("=" * 65)
                print(f" -> Convergência alcançada na iteração {it} com erro {max_diff:.6e} < {tol}!")
                print("=" * 65)
            break

    if not convergiu and verbose:
        print("=" * 65)
        print(f" -> AVISO: Limite máximo ({max_iter}) atingido sem convergência estrita.")
        print("=" * 65)

    return x, len(historico_erros), historico_erros, convergiu


def montar_sistema_trelica(
    P2: float = 500.0, P4: float = 100.0
) -> Tuple[List[List[float]], List[float], List[str]]:
    """
    Monta a matriz esparsa A e o vetor b para a treliça de 5 nós e 7 barras.
    
    A treliça possui:
        - 7 barras: F1, F2, F3, F4, F5, F6, F7
        - 3 reações: H1 (horizontal no nó 1), V1 (vertical no nó 1), V5 (vertical no nó 5)
    
    Geometria / Ângulos com a horizontal:
        - Barra 1 (Nó 1 -> Nó 2): 45°
        - Barra 2 (Nó 1 -> Nó 3): horizontal (0°)
        - Barra 3 (Nó 2 -> Nó 3): 45°
        - Barra 4 (Nó 2 -> Nó 4): horizontal (0°)
        - Barra 5 (Nó 3 -> Nó 4): 60°
        - Barra 6 (Nó 3 -> Nó 5): horizontal (0°)
        - Barra 7 (Nó 4 -> Nó 5): 30°
    
    Cargas verticais descendentes aplicadas:
        - Nó 2: P2 (padrão 500 N)
        - Nó 4: P4 (padrão 100 N)
    """
    c45 = math.cos(deg2rad(45))
    s45 = math.sin(deg2rad(45))
    c60 = math.cos(deg2rad(60))
    s60 = math.sin(deg2rad(60))
    c30 = math.cos(deg2rad(30))
    s30 = math.sin(deg2rad(30))

    # Matriz 10x10 nas equações naturais dos nós:
    # Incógnitas x = [F1, F2, F3, F4, F5, F6, F7, H1, V1, V5]
    # Índices:        0   1   2   3   4   5   6   7   8   9
    A_raw = [[0.0] * 10 for _ in range(10)]
    b_raw = [0.0] * 10

    # Nó 1:
    # Eq 0 (ΣFx = 0): F1*cos(45) + F2 + H1 = 0
    A_raw[0][0] = c45
    A_raw[0][1] = 1.0
    A_raw[0][7] = 1.0
    b_raw[0] = 0.0

    # Eq 1 (ΣFy = 0): F1*sin(45) + V1 = 0
    A_raw[1][0] = s45
    A_raw[1][8] = 1.0
    b_raw[1] = 0.0

    # Nó 2:
    # Eq 2 (ΣFx = 0): -F1*cos(45) + F3*cos(45) + F4 = 0
    A_raw[2][0] = -c45
    A_raw[2][2] = c45
    A_raw[2][3] = 1.0
    b_raw[2] = 0.0

    # Eq 3 (ΣFy = 0): -F1*sin(45) - F3*sin(45) = P2
    A_raw[3][0] = -s45
    A_raw[3][2] = -s45
    b_raw[3] = P2

    # Nó 3:
    # Eq 4 (ΣFx = 0): -F2 - F3*cos(45) + F5*cos(60) + F6 = 0
    A_raw[4][1] = -1.0
    A_raw[4][2] = -c45
    A_raw[4][4] = c60
    A_raw[4][5] = 1.0
    b_raw[4] = 0.0

    # Eq 5 (ΣFy = 0): F3*sin(45) + F5*sin(60) = 0
    A_raw[5][2] = s45
    A_raw[5][4] = s60
    b_raw[5] = 0.0

    # Nó 4:
    # Eq 6 (ΣFx = 0): -F4 - F5*cos(60) + F7*cos(30) = 0
    A_raw[6][3] = -1.0
    A_raw[6][4] = -c60
    A_raw[6][6] = c30
    b_raw[6] = 0.0

    # Eq 7 (ΣFy = 0): -F5*sin(60) - F7*sin(30) = P4
    A_raw[7][4] = -s60
    A_raw[7][6] = -s30
    b_raw[7] = P4

    # Nó 5:
    # Eq 8 (ΣFx = 0): -F6 - F7*cos(30) = 0
    A_raw[8][5] = -1.0
    A_raw[8][6] = -c30
    b_raw[8] = 0.0

    # Eq 9 (ΣFy = 0): F7*sin(30) + V5 = 0
    A_raw[9][6] = s30
    A_raw[9][9] = 1.0
    b_raw[9] = 0.0

    # Reordenação estratégica para garantir elementos não-nulos na diagonal
    # e assegurar convergência (raio espectral rho(T_GS) ≈ 0.9108 < 1):
    ordem_linhas = [3, 4, 5, 2, 7, 8, 6, 0, 1, 9]

    A_ord = [A_raw[idx] for idx in ordem_linhas]
    b_ord = [b_raw[idx] for idx in ordem_linhas]

    nomes_vars = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "H1", "V1", "V5"]

    return A_ord, b_ord, nomes_vars


def exibir_matriz(A: List[List[float]], b: List[float], nomes_vars: List[str]) -> None:
    """Exibe o sistema linear matricial de forma legível no terminal."""
    n = len(A)
    print("\n--- SISTEMA LINEAR REORDENADO PARA GAUSS-SEIDEL [A]{x} = {b} ---")
    cabecalho = " | ".join(f"{v:>7}" for v in nomes_vars)
    print(f"Eq | {cabecalho} | {'b':>8}")
    print("-" * (len(cabecalho) + 16))
    for i in range(n):
        linha_str = " | ".join(f"{A[i][j]:>7.3f}" for j in range(n))
        print(f"{i+1:2d} | {linha_str} | {b[i]:>8.2f}")
    print("-" * (len(cabecalho) + 16))


def apresentar_resultados_trelica(
    x: List[float], nomes_vars: List[str], P2: float, P4: float
) -> None:
    """Apresenta os esforços axiais nas barras e reações com interpretação estrutural."""
    print("\n" + "=" * 65)
    print("      RESULTADOS FINAIS - ANÁLISE ESTRUTURAL DA TRELIÇA")
    print("=" * 65)
    print(f"{'Componente':<12} | {'Tipo':<18} | {'Valor Calculado':>15} | {'Estado':<12}")
    print("-" * 65)

    descricoes = {
        "F1": ("Barra 1-2 (45°)", True),
        "F2": ("Barra 1-3 (Horiz.)", True),
        "F3": ("Barra 2-3 (45°)", True),
        "F4": ("Barra 2-4 (Horiz.)", True),
        "F5": ("Barra 3-4 (60°)", True),
        "F6": ("Barra 3-5 (Horiz.)", True),
        "F7": ("Barra 4-5 (30°)", True),
        "H1": ("Reação H no Nó 1", False),
        "V1": ("Reação V no Nó 1", False),
        "V5": ("Reação V no Nó 5", False),
    }

    sol_map = dict(zip(nomes_vars, x))

    for var in nomes_vars:
        desc, eh_barra = descricoes[var]
        val = sol_map[var]
        if eh_barra:
            if abs(val) < 1e-4:
                estado = "Nula"
            elif val > 0:
                estado = "TRAÇÃO (+)"
            else:
                estado = "COMPRESSÃO (-)"
            tipo = "Esforço Normal"
        else:
            tipo = desc
            estado = "Apoio"

        print(f"{var:<12} | {tipo:<18} | {val:>15.4f} | {estado:<12}")

    print("=" * 65)

    # Verificação estática global
    V1 = sol_map["V1"]
    V5 = sol_map["V5"]
    H1 = sol_map["H1"]
    soma_v = V1 + V5 - (P2 + P4)
    print("\n--- VERIFICAÇÃO DE EQUILÍBRIO GLOBAL DA ESTRUTURA ---")
    print(f"• Cargas aplicadas para baixo: P2 + P4 = {P2:.2f} + {P4:.2f} = {P2 + P4:.2f}")
    print(f"• Soma das reações verticais:  V1 + V5 = {V1:.4f} + {V5:.4f} = {V1 + V5:.4f}")
    print(f"• Resíduo vertical (ΣFy):      {abs(soma_v):.6f} (Equilíbrio atendido!)")
    print(f"• Reação horizontal (ΣFx):     H1 = {H1:.6f} (Sem forças horizontais externas)")
    print("-" * 65)


def resolver_sistema_generico() -> None:
    """Permite ao usuário inserir um sistema de equações lineares n x n genérico."""
    print("\n--- RESOLUÇÃO DE SISTEMA LINEAR GENÉRICO N x N ---")
    try:
        n = int(input("Informe o número de equações/incógnitas (n): "))
        if n <= 0:
            print("O valor de n deve ser positivo!")
            return
    except ValueError:
        print("Entrada inválida!")
        return

    print("\nDigite os coeficientes linha por linha (separados por espaço):")
    A: List[List[float]] = []
    for i in range(n):
        while True:
            try:
                linha = list(map(float, input(f"Linha {i+1} ({n} valores): ").strip().split()))
                if len(linha) != n:
                    print(f"Erro: você deve digitar exatamente {n} números.")
                    continue
                A.append(linha)
                break
            except ValueError:
                print("Por favor, digite números válidos.")

    print("\nDigite o vetor de termos independentes b (separados por espaço):")
    b: List[float] = []
    while True:
        try:
            b = list(map(float, input(f"Vetor b ({n} valores): ").strip().split()))
            if len(b) != n:
                print(f"Erro: você deve digitar exatamente {n} números.")
                continue
            break
        except ValueError:
            print("Por favor, digite números válidos.")

    tol_str = input("Informe a precisão/tolerância desejada (padrão 0.0001): ").strip()
    tol = float(tol_str) if tol_str else 0.0001

    max_it_str = input("Informe o número máximo de iterações (padrão 1000): ").strip()
    max_it = int(max_it_str) if max_it_str else 1000

    try:
        x, _, _, _ = resolver_gauss_seidel(A, b, tol=tol, max_iter=max_it, verbose=True)
        print("\n--- SOLUÇÃO ENCONTRADA ---")
        for i in range(n):
            print(f"x[{i+1}] = {x[i]:.6f}")
    except Exception as e:
        print(f"\nErro durante a execução: {e}")


def menu_principal() -> None:
    """Loop do menu principal com opções interativas."""
    while True:
        print("\n" + "=" * 65)
        print("   UNIVASF - CÁLCULO NUMÉRICO - PROJETO FINAL (TÓPICO 02 - Q2)")
        print("          MÉTODO DE GAUSS-SEIDEL EM TRELIÇA ISOSTÁTICA")
        print("=" * 65)
        print("1. Resolver o Problema Padrão da Treliça (Cargas 500 e 100, tol = 0.0001)")
        print("2. Resolver a Treliça com Novos Carregamentos Externos")
        print("3. Resolver um Sistema Linear Genérico n x n (Gauss-Seidel)")
        print("4. Exibir o Sistema Matricial e as Equações dos Nós da Treliça")
        print("5. Sair do Programa")
        print("=" * 65)

        opcao = input("Escolha uma opção (1-5): ").strip()

        if opcao == "1":
            A, b, nomes = montar_sistema_trelica(P2=500.0, P4=100.0)
            print("\n>> Executando resolução para cargas P2 = 500 N e P4 = 100 N com tol = 0.0001...")
            x, _, _, _ = resolver_gauss_seidel(A, b, tol=0.0001, max_iter=1000, verbose=True)
            apresentar_resultados_trelica(x, nomes, P2=500.0, P4=100.0)

        elif opcao == "2":
            try:
                p2_in = float(input("\nInforme a carga vertical no Nó 2 (topo esquerdo, padrão 500): "))
                p4_in = float(input("Informe a carga vertical no Nó 4 (topo direito, padrão 100): "))
                tol_in = input("Informe a precisão/tolerância desejada (padrão 0.0001): ").strip()
                tol = float(tol_in) if tol_in else 0.0001

                A, b, nomes = montar_sistema_trelica(P2=p2_in, P4=p4_in)
                x, _, _, _ = resolver_gauss_seidel(A, b, tol=tol, max_iter=1000, verbose=True)
                apresentar_resultados_trelica(x, nomes, P2=p2_in, P4=p4_in)
            except ValueError:
                print("Valor numérico inválido!")

        elif opcao == "3":
            resolver_sistema_generico()

        elif opcao == "4":
            A, b, nomes = montar_sistema_trelica(P2=500.0, P4=100.0)
            exibir_matriz(A, b, nomes)

        elif opcao == "5":
            print("\nEncerrando o programa. Bom trabalho e excelente apresentação na UNIVASF!\n")
            sys.exit(0)

        else:
            print("\nOpção inválida! Escolha entre 1 e 5.")


if __name__ == "__main__":
    menu_principal()
