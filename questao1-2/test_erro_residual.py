import unittest
from contextlib import redirect_stdout
from io import StringIO

from eliminacao_gauss import resolver_gauss
from eliminacao_jordan import resolver_jordan
from erro_residual import calcular_erro_residual, exibir_erro_residual
from fatoracao_lu import resolver_lu


class TestErroResidual(unittest.TestCase):
    def setUp(self):
        self.matriz = [
            [15.0, 17.0, 19.0, 3890.0],
            [0.30, 0.40, 0.55, 95.0],
            [1.00, 1.20, 1.50, 282.0],
        ]
        self.solucao = [90.0, 60.0, 80.0]

    def test_solucao_exata_tem_residuo_nulo(self):
        resultado = calcular_erro_residual(self.matriz, self.solucao)

        self.assertEqual(resultado["norma_infinita"], 0.0)
        self.assertEqual(resultado["norma_2"], 0.0)
        self.assertEqual(resultado["erro_relativo"], 0.0)

    def test_solucao_errada_tem_residuo_grande(self):
        resultado = calcular_erro_residual(self.matriz, [0.0, 0.0, 0.0])

        self.assertEqual(resultado["residuos"], [3890.0, 95.0, 282.0])
        self.assertEqual(resultado["norma_infinita"], 3890.0)
        self.assertEqual(resultado["norma_b"], 3890.0)
        self.assertAlmostEqual(
            resultado["erro_relativo"],
            1.0,
            places=12,
        )

    def test_residuo_de_cada_equacao(self):
        solucao = [90.0, 60.0, 81.0]
        resultado = calcular_erro_residual(self.matriz, solucao)

        # A terceira componente usa 1.5 g de borracha por unidade
        self.assertAlmostEqual(resultado["residuos"][2], -1.5, places=12)

    def test_solucoes_dos_metodos_satisfazem_o_sistema(self):
        for metodo in (resolver_gauss, resolver_jordan, resolver_lu):
            solucao = metodo(self.matriz)
            resultado = calcular_erro_residual(self.matriz, solucao)

            self.assertLess(resultado["erro_relativo"], 1e-12)

    def test_exibicao_do_erro_residual(self):
        saida = StringIO()

        with redirect_stdout(saida):
            exibir_erro_residual(self.matriz, self.solucao)

        texto = saida.getvalue()

        self.assertIn("Erro residual", texto)
        self.assertIn("||r||_infinito", texto)
        self.assertIn("||r||_2", texto)
        self.assertIn("satisfaz o sistema", texto)


if __name__ == "__main__":
    unittest.main()
