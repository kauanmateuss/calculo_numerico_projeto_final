import unittest
from contextlib import redirect_stdout
from io import StringIO

from eliminacao_gauss import resolver_gauss
from eliminacao_jordan import resolver_jordan
from fatoracao_lu import fatorar_lu, resolver_lu


class TestMetodosDiretos(unittest.TestCase):
    def setUp(self):
        # Sistema dos componentes eletricos (materiais em gramas)
        self.matriz = [
            [15.0, 17.0, 19.0, 3890.0],
            [0.30, 0.40, 0.55, 95.0],
            [1.00, 1.20, 1.50, 282.0],
        ]
        self.esperado = [90.0, 60.0, 80.0]

    def verificar_solucao(self, solucao):
        for obtido, esperado in zip(solucao, self.esperado):
            self.assertAlmostEqual(obtido, esperado, places=6)

    def test_gauss(self):
        self.verificar_solucao(resolver_gauss(self.matriz))

    def test_gauss_jordan(self):
        self.verificar_solucao(resolver_jordan(self.matriz))

    def test_lu(self):
        self.verificar_solucao(resolver_lu(self.matriz))

    def test_gauss_com_troca_de_linhas(self):
        matriz = [
            [0.0, 2.0, 4.0],
            [1.0, 1.0, 3.0],
        ]

        self.assertEqual(resolver_gauss(matriz), [1.0, 2.0])

    def test_jordan_com_troca_de_linhas(self):
        matriz = [
            [0.0, 2.0, 4.0],
            [1.0, 1.0, 3.0],
        ]

        self.assertEqual(resolver_jordan(matriz), [1.0, 2.0])

    def test_lu_com_troca_de_linhas(self):
        matriz = [
            [0.0, 2.0, 4.0],
            [1.0, 1.0, 3.0],
        ]

        self.assertEqual(resolver_lu(matriz), [1.0, 2.0])

    def test_sistema_generico_com_solucao_negativa(self):
        # Sistema diferente do problema base, com solucao (2, -1, 3)
        matriz = [
            [1.0, 1.0, 1.0, 4.0],
            [2.0, -1.0, 1.0, 8.0],
            [1.0, 2.0, 3.0, 9.0],
        ]

        for metodo in (resolver_gauss, resolver_jordan, resolver_lu):
            solucao = metodo(matriz)

            self.assertAlmostEqual(solucao[0], 2.0, places=6)
            self.assertAlmostEqual(solucao[1], -1.0, places=6)
            self.assertAlmostEqual(solucao[2], 3.0, places=6)

    def test_sistema_generico_4x4(self):
        # Sistema 4x4 com solucao (1, 2, 3, 4)
        matriz = [
            [1.0, 1.0, 1.0, 1.0, 10.0],
            [0.0, 1.0, 1.0, 1.0, 9.0],
            [0.0, 0.0, 1.0, 1.0, 7.0],
            [0.0, 0.0, 0.0, 1.0, 4.0],
        ]
        esperado = [1.0, 2.0, 3.0, 4.0]

        for metodo in (resolver_gauss, resolver_jordan, resolver_lu):
            solucao = metodo(matriz)

            for obtido, valor_esperado in zip(solucao, esperado):
                self.assertAlmostEqual(obtido, valor_esperado, places=6)

    def test_sistema_singular(self):
        matriz = [
            [1.0, 2.0, 3.0],
            [2.0, 4.0, 6.0],
        ]

        with self.assertRaises(ValueError):
            resolver_gauss([linha[:] for linha in matriz])

        with self.assertRaises(ValueError):
            resolver_jordan([linha[:] for linha in matriz])

        with self.assertRaises(ValueError):
            resolver_lu([linha[:] for linha in matriz])

    def test_fatoracao_lu_reconstroi_matriz_permutada(self):
        fatoracao = fatorar_lu(self.matriz)

        L = fatoracao["L"]
        U = fatoracao["U"]
        permutacao = fatoracao["permutacao"]
        n = fatoracao["n"]

        for i in range(n):
            for j in range(n):
                produto = sum(L[i][k] * U[k][j] for k in range(n))
                self.assertAlmostEqual(produto, self.matriz[permutacao[i]][j], places=9)

    def test_metodos_nao_alteram_matriz_original(self):
        copia = [linha[:] for linha in self.matriz]

        resolver_gauss(self.matriz)
        resolver_jordan(self.matriz)
        resolver_lu(self.matriz)

        self.assertEqual(self.matriz, copia)

    def test_exibicao_de_etapas(self):
        for metodo in (resolver_gauss, resolver_jordan, resolver_lu):
            saida = StringIO()

            with redirect_stdout(saida):
                metodo(self.matriz, mostrar_passos=True)

            texto = saida.getvalue()

            self.assertIn("Matriz aumentada inicial", texto)

            if metodo is resolver_lu:
                self.assertIn("Substituicao direta", texto)
                self.assertIn("Retrossubstituicao", texto)
            elif metodo is resolver_gauss:
                self.assertIn("Retrossubstituicao", texto)
            else:
                self.assertIn("Etapa 1", texto)


if __name__ == "__main__":
    unittest.main()
