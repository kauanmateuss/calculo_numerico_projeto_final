# Questão 2 — Componentes elétricos

Um engenheiro supervisiona a produção de três tipos de componentes elétricos.
Cada componente consome as seguintes quantidades de material:

| Componente | Metal (g) | Plástico (g) | Borracha (g) |
| ---------- | --------: | -----------: | -----------: |
| 1          |        15 |         0,30 |          1,0 |
| 2          |        17 |         0,40 |          1,2 |
| 3          |        19 |         0,55 |          1,5 |

A disponibilidade diária é de 3,89 kg de metal, 0,095 kg de plástico e
0,282 kg de borracha. Convertendo para gramas: 3890 g, 95 g e 282 g.

## a) Sistema de equações lineares

Sendo `x1`, `x2` e `x3` as quantidades diárias dos componentes 1, 2 e 3:

```
15*x1 + 17*x2 + 19*x3 = 3890   (metal)
0.30*x1 + 0.40*x2 + 0.55*x3 = 95   (plástico)
1.00*x1 + 1.20*x2 + 1.50*x3 = 282   (borracha)
```

Na forma matricial aumentada `[A|b]`:

```
[ 15    17    19 | 3890 ]
[ 0.30  0.40  0.55 |   95 ]
[ 1.00  1.20  1.50 |  282 ]
```

## b) Programa

O programa resolve sistemas lineares por métodos diretos, permitindo escolher
entre:

- **Eliminação de Gauss** — eliminação com pivoteamento parcial e
  retrossubstituição;
- **Eliminação de Gauss-Jordan** — a matriz é reduzida a `[I|x]`, sem
  retrossubstituição;
- **Fatoração LU** — decomposição `P*A = L*U`, seguida de substituição direta
  e retrossubstituição.

Todos os métodos usam pivoteamento parcial para reduzir erros de arredondamento
e detectar sistemas sem solução única. As etapas podem ser exibidas no terminal.

### Como executar

```bash
cd questao1-2
python3 main.py
```

O menu permite usar os dados do problema ou digitar qualquer sistema. Para o
problema dos componentes, basta escolher a opção `1`.

### Testes

```bash
cd questao1-2
python3 -m unittest discover -v
```

### Arquivos

| Arquivo               | Conteúdo                                            |
| --------------------- | --------------------------------------------------- |
| `main.py`             | Menu, leitura do sistema e exibição dos resultados   |
| `eliminacao_gauss.py` | Método de eliminação de Gauss                        |
| `eliminacao_jordan.py`| Método de eliminação de Gauss-Jordan                 |
| `fatoracao_lu.py`     | Fatoração LU com pivoteamento parcial                |
| `erro_residual.py`    | Cálculo e exibição do erro residual                  |
| `exibicao.py`         | Formatação de números e matrizes                     |
| `test_metodos.py`     | Testes dos três métodos diretos                      |
| `test_erro_residual.py`| Testes do erro residual                             |

## c) Solução

Resolvendo o sistema, obtém-se:

```
x1 = 90
x2 = 60
x3 = 80
```

Ou seja, podem ser produzidos por dia **90 componentes do tipo 1, 60 do tipo 2
e 80 do tipo 3**.

Verificação:

- metal: `15*90 + 17*60 + 19*80 = 1350 + 1020 + 1520 = 3890 g`;
- plástico: `0.30*90 + 0.40*60 + 0.55*80 = 27 + 24 + 44 = 95 g`;
- borracha: `1.0*90 + 1.2*60 + 1.5*80 = 90 + 72 + 120 = 282 g`.

## Erro residual

Para verificar numericamente a solução, o programa calcula o vetor residual

```
r = b - A*x
```

e exibe:

- o resíduo `r_i` de cada equação;
- a norma do infinito `||r||∞ = max |r_i|`;
- a norma euclidiana `||r||₂ = sqrt(Σ r_i²)`;
- o erro relativo `||r||∞ / ||b||∞`.

Quanto mais próximos de zero, melhor a solução satisfaz o sistema original.
Para o sistema do problema, o erro relativo fica na ordem de `1e-16`, próximo
do limite de precisão dos números de ponto flutuante.
