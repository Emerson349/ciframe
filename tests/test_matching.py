# coding: utf-8
import unittest

from matching import musica_contem_sequencia


class MatchingTests(unittest.TestCase):

    def test_sequencia_contigua_no_inicio(self):
        self.assertTrue(
            musica_contem_sequencia(['C', 'G', 'C', 'G'], ['C', 'G']))

    def test_sequencia_contigua_no_meio(self):
        self.assertTrue(
            musica_contem_sequencia(['G', 'C', 'G'], ['C', 'G']))

    def test_sequencia_contigua_no_fim(self):
        self.assertTrue(
            musica_contem_sequencia(['C', 'G', 'G', 'C'], ['G', 'C']))

    def test_rejeita_ordem_diferente(self):
        self.assertFalse(
            musica_contem_sequencia(['G', 'Am', 'C', 'F'], ['C', 'G', 'Am', 'F']))

    def test_rejeita_sequencia_nao_contigua(self):
        self.assertFalse(
            musica_contem_sequencia(['A', 'A', 'B', 'B'], ['A', 'B', 'A']))

    def test_rejeita_acordes_extras_na_musica(self):
        self.assertFalse(
            musica_contem_sequencia(
                ['C', 'G', 'Am', 'F', 'D'], ['C', 'G', 'Am', 'F']))

    def test_preserva_repeticoes_da_sequencia(self):
        self.assertTrue(
            musica_contem_sequencia(['C', 'G', 'C', 'G'], ['C', 'G', 'C']))

    def test_rejeita_repeticoes_em_ordem_nao_contigua(self):
        self.assertFalse(
            musica_contem_sequencia(['C', 'G', 'G', 'C'], ['C', 'G', 'C']))

    def test_comparacao_sensivel_a_maiusculas(self):
        self.assertFalse(
            musica_contem_sequencia(['Am', 'F', 'C', 'G'], ['AM', 'F', 'C', 'G']))

    def test_sequencia_vazia_nao_combina(self):
        self.assertFalse(musica_contem_sequencia(['C', 'G'], []))

    def test_cifra_vazia_nao_combina(self):
        self.assertFalse(musica_contem_sequencia([], ['C', 'G']))


if __name__ == '__main__':
    unittest.main()
