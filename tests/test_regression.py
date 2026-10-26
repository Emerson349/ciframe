# coding: utf-8
import os
import tempfile
import unittest
import uuid

os.environ.setdefault(
    'DB_PATH',
    os.path.join(tempfile.gettempdir(), 'ciframe_regression_%s.db' % uuid.uuid4().hex))

import main


class RegressaoSequenciasOriginaisTests(unittest.TestCase):

    CASOS = [
        (['Bm', 'G', 'D', 'A'], '0', 199),
        (['C', 'G', 'Am', 'F'], '1', 296),
        (['Em', 'G'], '2', 4),
        (['C', 'A7', 'Dm', 'G7'], '3', 5),
        (['Gm', 'F'], '4', 7),
        (['C', 'C7', 'F', 'Fm'], '5', 3),
    ]

    def test_as_seis_sequencias_originais_reproduzem_a_tag(self):
        for acordes, id_tag, quantidade in self.CASOS:
            with self.subTest(sequencia=acordes):
                encontradas = {
                    musica['id_unico_musica']
                    for musica in main.get_similares_por_sequencia(
                        acordes, main.generos)
                }
                marcadas = {
                    musica.id_unico_musica
                    for musica in main.musicas.values()
                    if id_tag in musica.seqs_famosas
                }

                self.assertEqual(quantidade, len(encontradas))
                self.assertEqual(marcadas, encontradas)


if __name__ == '__main__':
    unittest.main()
