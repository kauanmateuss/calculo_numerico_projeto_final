"""
Módulo de Métodos de Integração Numérica
Disciplina: Cálculo Numérico - UNIVASF
Tópico 04: Integração Numérica (Regras do Trapézio e Simpson Repetidas)
"""

from typing import List, Tuple, Dict, Any


def regra_trapezio_repetida(y: List[float], h: float) -> Dict[str, Any]:
    """
    Aplica a Regra dos Trapézios Repetida (Composta).
    
    Fórmula:
        I = (h / 2) * [y_0 + 2 * sum(y_1 ... y_{n-1}) + y_n]
        
    Parâmetros:
        y: Lista das ordenadas f(x_i)
        h: Espaçamento constante entre os pontos (h = x_{i+1} - x_i)
        
    Retorna:
        Dicionário com o resultado e detalhes dos passos intermediários.
    """
    n = len(y) - 1
    if n < 1:
        raise ValueError("São necessários pelo menos 2 pontos (1 subintervalo) para a Regra do Trapézio.")
    
    y0 = y[0]
    yn = y[-1]
    y_internos = y[1:-1]
    soma_internos = sum(y_internos)
    
    termo_parenteses = y0 + 2.0 * soma_internos + yn
    integral = (h / 2.0) * termo_parenteses
    
    return {
        "metodo": "Regra dos Trapézios Repetida",
        "n_subintervalos": n,
        "n_pontos": len(y),
        "h": h,
        "y0": y0,
        "yn": yn,
        "y_internos": y_internos,
        "soma_internos": soma_internos,
        "termo_soma": termo_parenteses,
        "resultado": integral
    }


def regra_simpson_13_repetida(y: List[float], h: float) -> Dict[str, Any]:
    """
    Aplica a Regra de 1/3 de Simpson Repetida (Composta).
    Requer que o número de subintervalos (n = len(y) - 1) seja PAR.
    
    Fórmula:
        I = (h / 3) * [y_0 + 4 * sum(y_impares) + 2 * sum(y_pares) + y_n]
        
    Parâmetros:
        y: Lista das ordenadas f(x_i)
        h: Espaçamento constante entre os pontos
        
    Retorna:
        Dicionário com o resultado e detalhes dos passos intermediários.
    """
    n = len(y) - 1
    if n < 2:
        raise ValueError("São necessários pelo menos 3 pontos (2 subintervalos) para a Regra de Simpson 1/3.")
    if n % 2 != 0:
        raise ValueError(
            f"O número de subintervalos (n = {n}) deve ser PAR para aplicar a Regra de 1/3 de Simpson Composta pura."
        )
        
    y0 = y[0]
    yn = y[-1]
    
    # Índices ímpares (multiplicados por 4)
    indices_impares = list(range(1, n, 2))
    valores_impares = [y[i] for i in indices_impares]
    soma_impares = sum(valores_impares)
    
    # Índices pares intermediários (multiplicados por 2)
    indices_pares = list(range(2, n, 2))
    valores_pares = [y[i] for i in indices_pares]
    soma_pares = sum(valores_pares)
    
    termo_parenteses = y0 + 4.0 * soma_impares + 2.0 * soma_pares + yn
    integral = (h / 3.0) * termo_parenteses
    
    return {
        "metodo": "Regra de 1/3 de Simpson Repetida",
        "n_subintervalos": n,
        "n_pontos": len(y),
        "h": h,
        "y0": y0,
        "yn": yn,
        "indices_impares": indices_impares,
        "valores_impares": valores_impares,
        "soma_impares": soma_impares,
        "indices_pares": indices_pares,
        "valores_pares": valores_pares,
        "soma_pares": soma_pares,
        "termo_soma": termo_parenteses,
        "resultado": integral
    }


def regra_simpson_adaptada(y: List[float], h: float) -> Dict[str, Any]:
    """
    Caso geral para Simpson:
    - Se n for par: aplica Simpson 1/3 diretamente.
    - Se n for ímpar: aplica Simpson 1/3 nos primeiros n-1 intervalos e Trapézio no último intervalo,
      ou Simpson 3/8 nos últimos 3 intervalos (se n >= 3 e n for ímpar).
    """
    n = len(y) - 1
    if n % 2 == 0:
        return regra_simpson_13_repetida(y, h)
    
    # Caso n seja ímpar e >= 3: combinar Simpson 1/3 (n-3 intervalos) + Simpson 3/8 (últimos 3 intervalos)
    if n >= 3:
        n_13 = n - 3
        res_13 = 0.0
        if n_13 > 0:
            res_13 = regra_simpson_13_repetida(y[:n_13 + 1], h)["resultado"]
        
        # Simpson 3/8 nos últimos 3 intervalos (4 pontos)
        # I_38 = (3*h / 8) * [y_{n-3} + 3*y_{n-2} + 3*y_{n-1} + y_n]
        y_38 = y[n_13:]
        res_38 = (3.0 * h / 8.0) * (y_38[0] + 3.0 * y_38[1] + 3.0 * y_38[2] + y_38[3])
        
        return {
            "metodo": "Regra Mista (Simpson 1/3 + Simpson 3/8)",
            "n_subintervalos": n,
            "n_pontos": len(y),
            "h": h,
            "resultado": res_13 + res_38,
            "detalhes": f"Aplicado Simpson 1/3 em {n_13} intervalos e Simpson 3/8 nos últimos 3 intervalos."
        }
    else:
        # n = 1: só pode trapézio
        res_trap = regra_trapezio_repetida(y, h)
        return {
            "metodo": "Trapézio (devido a n=1)",
            "n_subintervalos": n,
            "n_pontos": len(y),
            "h": h,
            "resultado": res_trap["resultado"],
            "detalhes": "Com apenas 1 subintervalo, aplica-se a Regra do Trapézio."
        }
