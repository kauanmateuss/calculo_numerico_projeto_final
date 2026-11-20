import sys
from typing import List, Tuple
from integracao_numerica import (
    regra_trapezio_repetida,
    regra_simpson_13_repetida,
    regra_simpson_adaptada
)
from grafico import plotar_perfil_rio


# Dados do problema
DADOS_ORIGINAIS_X = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0]
DADOS_ORIGINAIS_Y = [0.0, 1.8, 2.0, 4.0, 4.0, 6.0, 4.0, 3.6, 3.4, 2.8, 0.0]
H_ORIGINAL = 2.0





def exibir_tabela_pontos(x: List[float], y: List[float]):
    print("\n" + "-" * 55)
    print(f"{'Ponto (i)':^10} | {'Distância x_i (m)':^18} | {'Profundidade y_i (m)':^20}")
    print("-" * 55)
    for i, (xi, yi) in enumerate(zip(x, y)):
        print(f"{i:^10} | {xi:^18.2f} | {yi:^20.2f}")
    print("-" * 55)
    print(f"Total de pontos (N): {len(x)} | Total de subintervalos (n): {len(x) - 1}")
    h = x[1] - x[0] if len(x) > 1 else 0.0
    print(f"Espaçamento constante entre os pontos (h): {h:.2f} m\n")


def resolver_e_exibir(x: List[float], y: List[float], gerar_grafico: bool = True):
    h = x[1] - x[0]
    n = len(y) - 1
    
    exibir_tabela_pontos(x, y)
    
    print("=" * 75)
    print("  1. MÉTODO: REGRA DOS TRAPÉZIOS REPETIDA (COMPOSTA)")
    print("=" * 75)
    print("Fórmula Geral:")
    print("   I_Trap = (h / 2) * [ y_0 + 2 * (y_1 + y_2 + ... + y_{n-1}) + y_n ]\n")
    
    res_trap = regra_trapezio_repetida(y, h)
    
    y0 = res_trap["y0"]
    yn = res_trap["yn"]
    soma_internos = res_trap["soma_internos"]
    termo_soma = res_trap["termo_soma"]
    area_trap = res_trap["resultado"]
    
    print("Passo a passo do cálculo:")
    print(f"  • Extremos: y_0 = {y0:.2f} m,  y_{n} = {yn:.2f} m")
    print(f"  • Pontos intermediários: {', '.join(f'{val:.2f}' for val in res_trap['y_internos'])}")
    print(f"  • Soma dos pontos intermediários = {soma_internos:.2f}")
    print(f"  • Termo entre colchetes = {y0:.2f} + 2 * ({soma_internos:.2f}) + {yn:.2f} = {termo_soma:.2f}")
    print(f"  • I_Trap = ({h:.2f} / 2) * {termo_soma:.2f} = {area_trap:.4f} m²")
    print(f"\n>>> ÁREA CALCULADA (TRAPÉZIOS): {area_trap:.4f} m² <<<\n")
    
    print("=" * 75)
    print("  2. MÉTODO: REGRA DE SIMPSON REPETIDA (COMPOSTA)")
    print("=" * 75)
    
    area_simp = None
    if n % 2 == 0:
        print("Fórmula Geral (1/3 de Simpson Composta - n é PAR):")
        print("   I_Simp = (h / 3) * [ y_0 + 4 * Σ(y_ímpares) + 2 * Σ(y_pares) + y_n ]\n")
        
        res_simp = regra_simpson_13_repetida(y, h)
        area_simp = res_simp["resultado"]
        
        y0 = res_simp["y0"]
        yn = res_simp["yn"]
        s_impar = res_simp["soma_impares"]
        s_par = res_simp["soma_pares"]
        termo_soma = res_simp["termo_soma"]
        
        print("Passo a passo do cálculo:")
        print(f"  • Extremos: y_0 = {y0:.2f} m,  y_{n} = {yn:.2f} m")
        
        str_impares = " + ".join(f"y_{i}({y[i]:.2f})" for i in res_simp["indices_impares"])
        print(f"  • Termos ímpares (coeficiente 4): {str_impares}")
        print(f"    Σ(y_ímpares) = {s_impar:.2f}  ==>  4 * {s_impar:.2f} = {4.0 * s_impar:.2f}")
        
        str_pares = " + ".join(f"y_{i}({y[i]:.2f})" for i in res_simp["indices_pares"])
        print(f"  • Termos pares intermediários (coeficiente 2): {str_pares}")
        print(f"    Σ(y_pares) = {s_par:.2f}  ==>  2 * {s_par:.2f} = {2.0 * s_par:.2f}")
        
        print(f"  • Termo entre colchetes = {y0:.2f} + 4*({s_impar:.2f}) + 2*({s_par:.2f}) + {yn:.2f} = {termo_soma:.2f}")
        print(f"  • I_Simp = ({h:.2f} / 3) * {termo_soma:.2f} = {area_simp:.4f} m²")
        print(f"\n>>> ÁREA CALCULADA (SIMPSON 1/3): {area_simp:.4f} m² <<<\n")
    else:
        print(f"Atenção: O número de subintervalos n = {n} é ÍMPAR.")
        print("A Regra de 1/3 pura requer n PAR. Aplicando a Regra Mista (Simpson 1/3 + 3/8)...")
        res_misto = regra_simpson_adaptada(y, h)
        area_simp = res_misto["resultado"]
        print(f"Detalhes: {res_misto.get('detalhes', '')}")
        print(f"\n>>> ÁREA CALCULADA (SIMPSON MISTO): {area_simp:.4f} m² <<<\n")
    
    print("=" * 75)
    print("  3. QUADRO COMPARATIVO E DISCUSSÃO DE RESULTADOS")
    print("=" * 75)
    diff = abs(area_simp - area_trap)
    dif_pct = (diff / area_simp) * 100.0 if area_simp != 0 else 0.0
    
    print(f"  • Área obtida por Trapézios Repetidos : {area_trap:10.4f} m²")
    print(f"  • Área obtida por Simpson Repetido    : {area_simp:10.4f} m²")
    print(f"  • Diferença absoluta                  : {diff:10.4f} m²")
    print(f"  • Variação percentual relativa        : {dif_pct:10.2f} %")
    print("\nAnálise Técnica:")
    print("  - A Regra dos Trapézios aproxima o perfil do leito por segmentos de reta (polinômios de grau 1).")
    print("  - A Regra de 1/3 de Simpson aproxima o leito por arcos parabólicos (polinômios de grau 2),")
    print("    possuindo ordem de erro O(h⁴), o que captura com maior fidelidade a curvatura natural e")
    print("    suave do fundo de um rio ou canal.")
    print("=" * 75)
    
    if gerar_grafico:
        try:
            plotar_perfil_rio(x, y, area_trap, area_simp, salvar_caminho="perfil_secao_rio.png", mostrar=False)
        except Exception as e:
            print(f"(Aviso: Não foi possível gerar o gráfico automático: {e})")


def coletar_novos_dados() -> Tuple[List[float], List[float]]:
    print("\n" + "=" * 60)
    print("      ENTRADA DE NOVOS DADOS PARA OUTRO RIO / SEÇÃO")
    print("=" * 60)
    
    while True:
        try:
            h_input = input("Digite o espaçamento constante entre os pontos (h em metros): ").strip()
            h = float(h_input.replace(",", "."))
            if h <= 0:
                print("Erro: O espaçamento h deve ser estritamente positivo (> 0).")
                continue
            break
        except ValueError:
            print("Entrada inválida! Digite um número real (ex: 2.0 ou 1.5).")
            
    while True:
        try:
            print("\nDigite as profundidades (y_i) em metros:")
            print("Opção 1: Digite todos os valores na mesma linha separados por espaço ou vírgula.")
            print("Exemplo: 0 1.8 2 4 4 6 4 3.6 3.4 2.8 0")
            linha = input("Profundidades: ").strip()
            
            tokens = linha.replace(",", " ").split()
            y = [float(val) for val in tokens]
            
            if len(y) < 2:
                print("Erro: É necessário informar no mínimo 2 pontos de profundidade.")
                continue
            break
        except ValueError:
            print("Erro ao interpretar os valores. Certifique-se de digitar números válidos.")
            
    x = [i * h for i in range(len(y))]
    return x, y


def menu_principal():
    while True:
        print("\nEscolha uma opção:")
        print("  [1] Resolver o problema da Questão 1 (Perfil do Rio da Imagem)")
        print("  [2] Inserir novos dados (Novo problema com novos pontos/espaçamento)")
        print("  [3] Visualizar explicação teórica detalhada dos métodos")
        print("  [4] Sair do programa")
        print("-" * 75)
        
        opcao = input("Opção desejada (1/2/3/4): ").strip()
        
        if opcao == "1":
            print("\n>>> Executando cálculo com os dados oficiais da Questão 1...")
            resolver_e_exibir(DADOS_ORIGINAIS_X, DADOS_ORIGINAIS_Y, gerar_grafico=True)
            
        elif opcao == "2":
            x_custom, y_custom = coletar_novos_dados()
            print("\n>>> Executando cálculo com os dados informados...")
            resolver_e_exibir(x_custom, y_custom, gerar_grafico=True)
            
        elif opcao == "3":
            exibir_teoria()
            
        elif opcao == "4":
            print("\nEncerrando o programa.\n")
            sys.exit(0)
            
        else:
            print("\nOpção inválida! Escolha 1, 2, 3 ou 4.\n")
            
        print("\n" + "." * 75)
        continuar = input("Deseja realizar novos cálculos ou retornar ao menu? (S/n): ").strip().lower()
        if continuar in ["n", "nao", "não"]:
            print("\nEncerrando o programa. Até logo!\n")
            break
        print("\n" * 2)


def exibir_teoria():
    print("\n" + "=" * 75)
    print("                    FUNDAMENTAÇÃO TEÓRICA")
    print("=" * 75)
    print("""
1. CONTEXTUALIZAÇÃO FÍSICA E DE ENGENHARIA:
   - Em hidrologia e engenharia de recursos hídricos, a determinação da área 
     da seção transversal A(x) de um rio ou canal é indispensável para:
     a) Cálculo da Vazão (Q): Q = A * v (onde v é a velocidade média da água).
     b) Dimensionamento de diques e prevenção de transbordamentos e enchentes.
     c) Estimativa da capacidade volumétrica em bacias e reservatórios.
   - Como o perfil do leito não segue uma equação analítica conhecida f(x), 
     empregam-se métodos de quadratura numérica sobre pontos discretos (x_i, y_i) 
     obtidos por batimetria ou sondagens linimétricas.

2. REGRA DOS TRAPÉZIOS REPETIDA:
   - Aproxima o fundo do rio por uma linha poligonal formada por segmentos de reta
     (polinômios de interpolação linear de grau 1).
   - Em cada subintervalo [x_i, x_{i+1}], a área é calculada como um trapézio:
         A_i = (h / 2) * (y_i + y_{i+1})
   - Somando todos os n subintervalos:
         I_Trap = (h / 2) * [ y_0 + 2 * sum(y_1 até y_{n-1}) + y_n ]
   - Ordem de erro de truncamento: O(h²).

3. REGRA DE 1/3 DE SIMPSON REPETIDA:
   - Conecta pares de subintervalos adjacentes (grupos de 3 pontos consecutivos) 
     através de parábolas de 2º grau (interpolação quadrática).
   - Exige que o número total de subintervalos 'n' seja PAR (número ímpar de pontos).
   - Fórmula:
         I_Simp = (h / 3) * [ y_0 + 4 * sum(y_ímpares) + 2 * sum(y_pares) + y_n ]
   - Ordem de erro de truncamento: O(h⁴). É muito mais exata para superfícies 
     curvas naturais como os leitos de rios.
""")
    print("=" * 75)


if __name__ == "__main__":
    menu_principal()
