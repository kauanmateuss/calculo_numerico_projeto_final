from typing import List, Tuple, Dict, Any


def regra_trapezio_repetida(y: List[float], h: float) -> Dict[str, Any]:
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
    n = len(y) - 1
    if n % 2 == 0:
        return regra_simpson_13_repetida(y, h)
    
    # n ímpar: combina Simpson 1/3 com Simpson 3/8
    if n >= 3:
        n_13 = n - 3
        res_13 = 0.0
        if n_13 > 0:
            res_13 = regra_simpson_13_repetida(y[:n_13 + 1], h)["resultado"]
        
        # Simpson 3/8 nos últimos 3 intervalos
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
