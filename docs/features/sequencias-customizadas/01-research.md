# Pesquisa — Sequências de Acordes Customizadas

## Perguntas que você precisa responder

1. **Algoritmo de matching**: hoje, as 6 sequências hardcoded em `main.py` (linhas
   40-45) são comparadas contra músicas via uma tag pré-computada
   (`SEQ_FAMOSA`/`seqs_famosas`, vinda do CSV). Sequências cadastradas pelo usuário
   não têm essa tag — o matching precisa ser calculado em tempo real a partir da
   lista de acordes de cada música (`musica.acordes`/`musica.cifra`). O que vai
   definir "a sequência X aparece na música Y"? A ordem dos acordes importa?
   Repetições de acorde dentro da música importam? É preciso normalizar (ex.:
   maiúsculas/minúsculas, variações de escrita do mesmo acorde)? 
2. **Validação da hipótese**: rode o algoritmo que você está considerando contra os
   dados reais em `data/top/dataset_final.csv`, para as 6 sequências hoje
   hardcoded, e confirme (ou refute) que ele reproduz os mesmos matches que o
   código atual produz via `seqs_famosas`. Esse é o bar mínimo de correção que
   você vai usar na fase de testes. 
3. **Banco de dados**: quais bancos embarcados (sem serviço externo adicional) são
   viáveis dentro do container Docker único e local-only já documentado em
   `docs/adr/0001-local-only-docker-deploy.md`? O que cada opção implica para o
   `Dockerfile` atual e para a persistência dos dados entre reinícios do
   container?
4. **Frontend existente**: o que a página `#/porsequencia`
   (`static/templates/sequencia.html` +
   `static/assets/js/controllers/sequencia.js`) já faz? Repare que ela tem hoje uma
   lista *hardcoded no JavaScript* de 4 sequências (`sequencia1`..`sequencia4`),
   diferente das 6 que existem no backend — um detalhe real e pré-existente do
   código, não um erro seu, que vale entender antes de decidir o que precisa
   mudar.

## Registro das descobertas

1. 1- Sim, a ordem importa e a sequência aparece como uma janela contígua em musica.cifra. 2- A música usa apenas os acordes da sequência e nenhum acorde extra. 3- A comparação é exata e sensível a maiúsculas, sem normalização. Repetições não precisam de tratamento, pois a janela contígua já as cobre. Normalizar (tirar baixo e extensões) piora o resultado e quebra a seq 5.

2. Testei diferentes critérios de correspondência e identifiquei que as músicas marcadas usam somente os acordes da sequência, que deve aparecer em ordem e continuamente na cifra, sem acordes extras. A comparação preserva as repetições dos acordes.
A regra reproduziu exatamente as tags das seis sequências existentes:
| Sequência | Marcadas pela tag | Achadas pela regra | Diferença |
   |---|---|---|---|
   | BmGDA | 199 | 199 | 0 |
   | CGAmF | 296 | 296 | 0 |
   | EmG | 4 | 4 | 0 |
   | CA7DmG7 | 5 | 5 | 0 |
   | GmF | 7 | 7 | 0 |
   | CC7FFm | 3 | 3 | 0 |
Conclusão: a regra será utilizada como teste de regressão. Ela foi inferida a partir dos dados do CSV; portanto, embora reproduza todas as tags testadas, não há confirmação de que corresponda ao algoritmo original.

3.O ADR 0001 exige um único container, sem serviços externos, o que descarta bancos como PostgreSQL e MySQL. Entre as alternativas embarcadas, escolhi o SQLite, disponível na biblioteca padrão do Python (sqlite3), sem dependências adicionais.
O teste de concorrência com quatro processos resultou em 200 inserções válidas e 200 duplicatas rejeitadas pela restrição UNIQUE, totalizando 201 linhas. Um novo processo conseguiu ler os mesmos dados.
Para garantir a persistência, o banco deve ficar em um diretório como /data, fora da imagem Docker, utilizando um volume. Também será necessário inicializar a tabela e cadastrar as seis sequências originais sem duplicá-las nas execuções seguintes.

4. A página #/porsequencia lista quatro sequências definidas manualmente em sequencia.js, enquanto o backend possui seis em main.py. Assim, Em-G e C-A7-Dm-G7 estão disponíveis na busca, mas não aparecem na interface.
Ao selecionar uma sequência, o frontend chama /similares?sequencia=, e o backend remove as vírgulas para localizar a sequência. O filtro por gênero repete essa busca. Atualmente, não há formulário de cadastro nem endpoint para listar as sequências existentes.
Conclusão: Vai ser necessário criar uma rota para fornecer o catálogo ao frontend e substituir a lista fixa por uma chamada HTTP.

## Trade-offs identificados

### Algoritimo de Matching 
- Opção: Trecho contínuo, sem restrição de acordes.
    - Prós: Simples de implementar.
    - Contras: Muitos falsos positivos, 3.110 achados para Em-G (4 marcadas).
- Opção: Sequência não contígua ou conjunto sem ordem.
  - Prós: Aceita variações na ordem e na posição dos acordes.
  - Contras: Muitos falsos positivos: 13.643 e 14.160 músicas para Em-G.
- Opção: Trecho contínuo usando somente os acordes da sequência.
  - Prós: Reproduziu exatamente as tags das seis sequências existentes.
  - Contras: Exclui músicas com acordes extras; a regra foi deduzida dos dados, não confirmada pelo algoritmo original.

### Banco de dados
- Opção: SQLite.
  - Prós: Disponível na biblioteca padrão do Python, sem serviço externo, com transações e restrição `UNIQUE`.
  - Contras: O arquivo precisa de um volume Docker montado para persistir após a recriação do container; a persistência de volume será validada no container durante os testes.
- Opção: JSON ou TinyDB.
  - Prós: Mais simples de implementar.
  - Contras: Sem o controle de concorrência adequado, cadastros simultâneos podem sobrescrever dados.

### Frontend

- Opção: Manter a lista fixa no JavaScript e adicionar apenas o formulário.
  - Prós: Exige menos alterações.
  - Contras: A lista continua divergindo do backend, com quatro sequências na tela e seis disponíveis na busca.
- Opção: Criar uma rota no backend para listar as sequências e consumi-la no frontend.
  - Prós: Mantém o catálogo sincronizado com os dados reais e atende ao requisito de exibição das sequências cadastradas.
  - Contras: Exige alterações no frontend AngularJS e no backend.


