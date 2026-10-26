# Plano — Sequências de Acordes Customizadas

## Passos

1. [x] **Banco:** em `main.py`, criar a tabela `sequencias` no SQLite
   (`DB_PATH`, padrão `/data/sequencias.db`) e inserir as 6 originais só se
   a tabela estiver vazia. 
2. [x] **Matching (TDD):**
   - Escrever testes unitários em `tests/test_matching.py` para as regras de matching (janela contígua na ordem, sem acordes extras, repetições preservadas).
   - Executar os testes e capturar a saída de falha (**vermelho**).
   - Implementar a função de matching isolada em `matching.py` (ou `main.py`) até os testes passarem (**verde**).
3. [x] **Busca:** trocar `get_similares_por_sequencia` para usar essa função
   e o catálogo do banco, em vez da tag `SEQ_FAMOSA`.
4. [x] **API:** criar `GET /sequencias` e `POST /sequencias` com as validações
   e os códigos 201, 400 e 409 da proposta.
5. [x] **Teste de regressão:** rodar a regra nas 6 sequências e conferir que
   dá 199, 296, 4, 5, 7 e 3 músicas, iguais à tag.
6. [x] **Frontend:** em `sequencia.js` e `sequencia.html`, trocar a lista fixa
   por `GET /sequencias` e adicionar o formulário de cadastro com as
   mensagens de erro.
7. [x] **Docker & Persistência:**
   - Adicionar diretório `/data` e declaração de `VOLUME ["/data"]` no `Dockerfile`.
   - Testar ciclo no Docker: build, run com volume (`-v ciframe-data:/data`), cadastrar sequência customizada, dar `docker restart` e `docker rm -f` + `docker run` para provar persistência.
8. [x] **ADR 0002 & Documentação:** redigir `docs/adr/0002-persist-custom-sequences.md` justificando a adoção do SQLite e preencher o relatório final em `04-test-report.md`.

## Arquivos afetados

| Arquivo | Mudança |
|---|---|
| `main.py` | Banco, função de matching, `GET`/`POST /sequencias` e nova busca em `/similares` |
| `musica.py` | Sem mudança prevista |
| `static/assets/js/controllers/sequencia.js` | Carregar sequências da API e cadastrar nova |
| `static/templates/sequencia.html` | Formulário de cadastro e mensagens de erro |
| `Dockerfile` | Volume `/data` |
| `docs/adr/0002-persist-custom-sequences.md` | Novo: decisão de persistir em SQLite |
O banco é criado pelo próprio `main.py` na primeira execução, então não há
arquivo de migração separado.

## Riscos e mitigação

- **Atraso na busca em tempo real:** Testes preliminares registraram ~123 ms para varredura completa. Se necessário, aplicar filtro prévio pelo conjunto de acordes.
- **Perda de dados no container:** Mitigado montando volume nomeado (`-v ciframe-data:/data`) e definindo fallback local caso a pasta `/data` não exista no host de dev.


## Definição de pronto

- Cadastrar uma sequência funciona e rejeita inválida (400) e duplicada (409).
- A busca por uma sequência cadastrada devolve músicas.
- As 6 originais dão 199, 296, 4, 5, 7 e 3 músicas, como antes.
- A tela `#/porsequencia` mostra o catálogo do backend e permite cadastrar.
- As sequências cadastradas continuam lá depois de reiniciar o container.
- TDD do matching executado com evidência de vermelho e verde.
