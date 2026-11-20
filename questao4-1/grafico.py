from typing import List, Optional
import matplotlib.pyplot as plt
import numpy as np


def plotar_perfil_rio(
    x: List[float],
    y: List[float],
    area_trap: float,
    area_simp: float,
    salvar_caminho: Optional[str] = "perfil_secao_rio.png",
    mostrar: bool = False
) -> None:
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(11, 6), dpi=120)
    
    x_arr = np.array(x)
    y_arr = np.array(y)
    
    ax.axhline(0, color='#1f77b4', linestyle='--', linewidth=1.5, label="Superfície da Água (y = 0)")
    
    # Profundidade desenhada para baixo (valores negativos)
    ax.plot(x_arr, -y_arr, color='#8c564b', marker='o', linewidth=2.5, markersize=6, label="Leito do Rio (Perfil Batimétrico)")
    
    ax.fill_between(x_arr, 0, -y_arr, color='#4ba3e3', alpha=0.35, label="Área da Seção Reta (Água)")
    
    for xi, yi in zip(x_arr, y_arr):
        if yi > 0:
            ax.plot([xi, xi], [0, -yi], color='#7f7f7f', linestyle=':', linewidth=1.2)
            ax.annotate(
                f"{yi:.1f} m",
                xy=(xi, -yi / 2.0),
                xytext=(0, 0),
                textcoords="offset points",
                ha='center',
                va='center',
                fontsize=9,
                color='#111111',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#cccccc", alpha=0.85)
            )
            ax.annotate(
                f"({xi:.0f}, {yi:.1f})",
                xy=(xi, -yi),
                xytext=(0, -12),
                textcoords="offset points",
                ha='center',
                va='top',
                fontsize=8,
                color='#333333'
            )
    
    titulo = "Seção Reta do Rio - Integração Numérica\n"
    titulo += f"Área (Trapézios Repetidos): {area_trap:.2f} m² | Área (Simpson 1/3 Repetido): {area_simp:.2f} m²"
    ax.set_title(titulo, fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Distância a partir da margem esquerda (m)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Profundidade (m)", fontsize=11, fontweight='bold')
    
    # Profundidade positiva no eixo vertical
    max_prof = max(y) if len(y) > 0 else 6.0
    ax.set_ylim(-max_prof - 1.5, 1.0)
    ticks_y = np.arange(0, int(max_prof) + 2, 1)
    ax.set_yticks(-ticks_y)
    ax.set_yticklabels([f"{t:.1f}" for t in ticks_y])
    
    ax.set_xticks(x_arr)
    ax.set_xlim(min(x_arr) - 1, max(x_arr) + 1)
    
    ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    
    if salvar_caminho:
        plt.savefig(salvar_caminho, dpi=150)
        print(f"Gráfico salvo com sucesso em: {salvar_caminho}")
        
    if mostrar:
        plt.show()
    plt.close(fig)
