# Relatório de testes — Sequências de Acordes Customizadas

## Cobertura

- **Matching (TDD):** `tests/test_matching.py` (11 testes)
  - Ordem e contiguidade obrigatórias.
  - Rejeição de acordes extras na música.
  - Repetições preservadas na janela contígua.
  - Comparação exata, sensível a maiúsculas.
  - Sequência ou cifra vazia não combina.
- **API (`POST /sequencias` e `GET /sequencias`):** `tests/test_api.py`
  - Listagem traz as 6 originais na ordem.
  - Criação válida (201) e presença no catálogo.
  - Duplicidade da sequência original e de sequência nova (409).
  - Validações de limites, vazios e caracteres inválidos (400).
  - `/similares?sequencia=` retorna `[]` para sequência não cadastrada e
    resultados para sequência cadastrada.
- **Regressão:** `tests/test_regression.py`
  - Compara o conjunto de ids encontrados pela regra com o conjunto marcado
    pela tag `SEQ_FAMOSA`, além das contagens.
- **Persistência em Container (Docker):**
  - Teste de restart: dados permanecem após `docker restart`.
  - Teste de recriação: dados permanecem após `docker rm -f` e novo
    `docker run` com volume `-v ciframe-data-test:/data`.

## Evidência TDD (vermelho e verde)

Antes de existir `matching.py`, os testes falharam na importação:

```
ERROR: test_matching (unittest.loader._FailedTest.test_matching)
ImportError: Failed to import test module: test_matching
ModuleNotFoundError: No module named 'matching'
Ran 1 test in 0.000s
FAILED (errors=1)
```

Depois da implementação de `matching.py`:

```
Ran 11 tests in 0.001s
OK
```

Suíte completa:

```
python -m unittest discover -s tests -v
Ran 19 tests in 1.237s
OK
```

## Teste de regressão obrigatório

As 6 sequências originais (`SEQUENCIAS_ORIGINAIS` em `main.py`) continuam
retornando os mesmos resultados de antes da migração para o banco de dados.

| Sequência | Marcadas pela tag | Achadas pela regra | Conjunto de ids |
|---|---|---|---|
| BmGDA | 199 | 199 | igual |
| CGAmF | 296 | 296 | igual |
| EmG | 4 | 4 | igual |
| CA7DmG7 | 5 | 5 | igual |
| GmF | 7 | 7 | igual |
| CC7FFm | 3 | 3 | igual |

A comparação é feita pelo conjunto de ids das músicas e não só pela contagem
(`tests/test_regression.py`).

## Persistência no Docker

Com o volume nomeado, cadastrei `Am,F,C,G` e verifiquei o catálogo:

```
POST status: 201 body: {"id": 7, "acordes": ["Am", "F", "C", "G"]}
Antes do restart: 7 sequencias; custom presente: True
Apos docker restart: 7 sequencias; custom presente: True
Apos docker rm -f + docker run: 7 sequencias; custom presente: True
```

## Como rodar

```
python -m unittest discover -s tests
```

## O que ficou de fora

- Proteção contra spam ou muitas requisições: fora do escopo.
- Validação de caracteres ilegais no CSV: fora do escopo.
- Teste automatizado do frontend (AngularJS): verificado manualmente no
  navegador.
