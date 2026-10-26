# coding: utf-8
import json
import os
import tempfile
import unittest
import uuid

os.environ.setdefault(
    'DB_PATH',
    os.path.join(tempfile.gettempdir(), 'ciframe_api_%s.db' % uuid.uuid4().hex))

import main


class SequenciasApiTests(unittest.TestCase):

    def setUp(self):
        self.client = main.app.test_client()

    def get_json(self, response):
        return json.loads(response.data.decode('utf-8'))

    def test_get_sequencias_traz_as_seis_originais(self):
        response = self.client.get('/sequencias')

        self.assertEqual(200, response.status_code)
        sequencias = self.get_json(response)
        self.assertEqual(
            [
                ['Bm', 'G', 'D', 'A'],
                ['C', 'G', 'Am', 'F'],
                ['Em', 'G'],
                ['C', 'A7', 'Dm', 'G7'],
                ['Gm', 'F'],
                ['C', 'C7', 'F', 'Fm'],
            ],
            [sequencia['acordes'] for sequencia in sequencias[:6]])

    def test_post_sequencia_valida_retorna_201_e_aparece_no_catalogo(self):
        nova = ['Am', 'F', 'C', 'G']
        response = self.client.post('/sequencias', json={'acordes': nova})

        self.assertEqual(201, response.status_code)
        criada = self.get_json(response)
        self.assertEqual(nova, criada['acordes'])
        self.assertIsInstance(criada['id'], int)

        catalogo = self.get_json(self.client.get('/sequencias'))
        self.assertIn(nova, [sequencia['acordes'] for sequencia in catalogo])

    def test_post_sequencia_duplicada_retorna_409(self):
        nova = ['Dm', 'G', 'C']
        self.assertEqual(
            201,
            self.client.post('/sequencias', json={'acordes': nova}).status_code)

        response = self.client.post('/sequencias', json={'acordes': nova})

        self.assertEqual(409, response.status_code)
        self.assertIn('erro', self.get_json(response))

    def test_post_sequencia_original_duplicada_retorna_409(self):
        response = self.client.post(
            '/sequencias', json={'acordes': ['Bm', 'G', 'D', 'A']})

        self.assertEqual(409, response.status_code)

    def test_post_sequencias_invalidas_retornam_400(self):
        casos = [
            None,
            {},
            {'acordes': 'Am,F,C,G'},
            {'acordes': ['Am']},
            {'acordes': ['Am', 'F', 'C', 'G', 'D', 'Em', 'A', 'B', 'E']},
            {'acordes': ['Am', '']},
            {'acordes': ['Am', 'F C']},
            {'acordes': ['Am', 'F,C']},
            {'acordes': ['Am', 'F;C']},
            {'acordes': ['Am', 'F' * 21]},
            {'acordes': ['Am', 7]},
        ]

        for caso in casos:
            with self.subTest(caso=caso):
                response = self.client.post('/sequencias', json=caso)
                self.assertEqual(400, response.status_code)

    def test_similares_de_sequencia_nao_cadastrada_retorna_vazio(self):
        response = self.client.get('/similares?sequencia=X,Y,Z')

        self.assertEqual(200, response.status_code)
        self.assertEqual([], self.get_json(response))

    def test_similares_com_sequencia_cadastrada_funciona(self):
        response = self.client.get('/similares?sequencia=Bm,G,D,A')

        self.assertEqual(200, response.status_code)
        self.assertEqual(100, len(self.get_json(response)))


if __name__ == '__main__':
    unittest.main()
