# Proposta — Sequências de Acordes Customizadas

## Abordagem escolhida

### Algoritmo de matching

Uma música combina com uma sequência quando duas condições valem ao mesmo
tempo: (1) a sequência aparece **em ordem e sem interrupção** na lista de
acordes da música , e (2) a música **não usa nenhum acorde
fora** da sequência. A comparação é exata, sensível a maiúsculas e sem
normalização; as repetições dentro da música são mantidas como estão. Em código: `set(cifra) == set(seq)` e seq é uma janela contígua de cifra.
Essa é a única das testadas que reproduziu a tag
`SEQ_FAMOSA` nas 6 sequências, sem sobrar nem faltar música (199, 296, 4, 5, 7
e 3 músicas), enquanto outras traziam milhares de resultados a mais.

### Banco de dados

SQLite, pelo módulo `sqlite3` da biblioteca padrão. Atende ao ADR 0001 (um
container, sem serviço externo), não adiciona dependência e suportou 4
processos gravando ao mesmo tempo no meu teste, com duplicatas rejeitadas
corretamente. O arquivo fica em /data/sequencias.db por padrão (fora da imagem, em um
volume Docker), com fallback para o diretório local caso /data não exista (desenvolvimento
sem Docker), e o caminho pode ser customizado via variável de ambiente DB_PATH. Só o
catálogo de sequências vai para o banco; músicas e gêneros continuam vindo do
CSV em memória.

### Esquema de dados (alto nível)

Uma tabela `sequencias`:
- `id`: inteiro, chave primária, gerado pelo banco.
- `acordes`: texto, obrigatório e único, com os acordes separados por
  vírgula (ex.: `Bm,G,D,A`). Nenhum acorde do CSV tem vírgula, então a
  separação é segura.
- `criada_em`: data e hora do cadastro.
Na primeira execução, a tabela é criada e as 6 sequências originais são
inseridas, sem duplicar nas execuções seguintes.


### API

- `GET /sequencias`: retorna o catálogo de sequências cadastradas. ex:
  `[{"id": 1, "acordes": ["Bm","G","D","A"]}, ...]`.
- `POST /sequencias`: cadastra uma sequência sem exigir login. Corpo:
  `{"acordes": ["Am","F","C","G"]}`. Sem login. Respostas:
  - `201`: cadastro realizado.
  - `400`: sequência inválida (de 2 a 8 acordes, cada um com até 20 caracteres e sem espaços, vírgulas, `;` ou valores vazios).
  - `409`: sequência já cadastrada, considerando a mesma ordem e grafia.
- `GET /similares?sequencia=Bm,G,D,A`: mantém o formato atual, mas usa a nova regra de matching em vez da tag `SEQ_FAMOSA`. Se a sequência não estiver cadastrada, retorna `[]`.

Todas as respostas continuam usando `json.dumps(...)`, sem `jsonify`. Acordes não existentes no CSV são aceitos, mas não encontrarão músicas.

### Frontend

Em `#/porsequencia`:
- A lista fixa de 4 sequências sai de `sequencia.js`. A tela carrega as
  sequências de `GET /sequencias` e mostra todas as 6 originais e as novas.
- Entra um campo de texto para digitar os acordes separados por vírgula e um
  botão "Cadastrar". Ao salvar, a lista é recarregada. Erros `400` e `409`
  aparecem como mensagem na tela.
- A cor dos acordes (`#2E1C74`) passa a ser aplicada pelo front, já que o
  backend não guarda cor.
- Clicar em qualquer sequência faz a busca de `/similares`, como já funciona.

## Alternativas consideradas e descartadas

- **Regra de matching mais solta** (sequência contígua sem restringir os
  acordes). Descartada: devolve milhares de falsos positivos e não reproduz a
  tag das sequências originais, que é o critério de regressão.
- **Guardar no banco, para cada sequência, a lista de músicas que combinam**
  (pré-calculada ao cadastrar). Descartada: ganha pouco, porque a busca em
  tempo real leva 123 ms, e exige recalcular tudo se o CSV mudar.
- **JSON ou TinyDB em vez de SQLite.** Descartada: sem trava de escrita, dois
  cadastros simultâneos podem se sobrescrever.

## Escopo explícito

**Dentro do escopo:**

- Cadastrar e listar sequências, persistidas em SQLite.
- Buscar músicas por qualquer sequência do catálogo, com a regra definida.
- Tela `#/porsequencia` ligada ao catálogo real, com formulário de cadastro.
- ADR 0002 e teste de regressão contra as 6 sequências originais.

**Fora do escopo (e por quê):**

- Sequências: o enunciado pede catálogo aberto e
  anônimo, e só cadastro.
- Limite de requisições ou proteção contra spam: sem login não há como
  identificar quem cadastra; fica como risco conhecido.
- Reconhecer `Em-G` e `G-Em` como a mesma sequência: dão as mesmas músicas, mas
  são cadastros distintos. Aceito como limitação.
