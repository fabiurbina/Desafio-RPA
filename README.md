# RPA Desafio Full Stack Developer - Python (RPA)

Este RPA tem o objetivo de realizar a coleta de dados no Portal da Transparência, utilizando como referência o **nome**, **CPF** ou **número do NIS**.

## Visão Geral

Este RPA foi criado para automatizar o processo de consultas no Portal da Transparência, disponível em [https://portaldatransparencia.gov.br/pessoa/visao-geral](https://portaldatransparencia.gov.br/pessoa/visao-geral). Ele busca informações sobre benefícios de programas sociais, como **Auxílio Brasil**, **Auxílio Emergencial** e **Bolsa Família**, a partir dos seguintes parâmetros: **Nome**, **CPF** ou **NIS**.

### Funcionalidades principais:
- Realiza a busca de dados de pessoas no Portal da Transparência.
- Permite consulta múltipla via campo único.
- Retorna até **10 resultados** quando a busca é feita pelo nome. Quando consultado por **CPF** ou **NIS**, retorna apenas 1 resultado.
- A resposta de saída, para resultados positivos, é fornecida em formato **JSON** com os seguintes dados:
  - **NIS**
  - **Nome**
  - **Benefício Social**
  - **Valor do Benefício**
  - **Imagem** (captura de tela em base64)

### Exemplo de saída (JSON):
```json
[
  {
    "nome": "Nome da Pessoa",
    "link": "link da página onde os dados foram coletados",
    "beneficio": "Auxílio Brasil",
    "nis": "2222222",
    "valor": "500,00",
    "imagem": "Imagem64"
  }
]




























## Considerações Finais

Este código automatiza a coleta de dados do Portal da Transparência, realizando a busca e extração de informações sobre benefícios sociais como Auxílio Brasil, Auxílio Emergencial e Bolsa Família. Durante o processo, algumas considerações são importantes:

- **Captura de Evidências (Print Screens)**: Ao longo da execução, o código captura evidências visuais das telas, gerando imagens base64. Estas imagens representam o resultado da consulta e são retornadas ao final do processo para análise visual.
  
- **Navegação em Telas Ocultas**: Utilizamos a função `find_elements` do Selenium para navegar nas páginas, inclusive nas telas que podem estar ocultas ou requerer interação adicional (como rolar a página). Isso garante que a automação seja capaz de capturar todos os dados necessários, mesmo que estejam em áreas que não são imediatamente visíveis.

- **Evidência Final**: Após o término de cada consulta, o código sempre retorna a **evidência visual** do **primeiro dado consultado**, exibindo-o de forma clara e precisa. Isso é feito gerando uma imagem da tela com as informações relevantes e exibindo-a ao usuário para que possa verificar os dados processados.

Essa abordagem permite que a automação não apenas colete dados de maneira eficiente, mas também forneça uma forma tangível e visual de validação do processo, garantindo que o usuário possa confirmar os resultados de forma simples e rápida.

### Fluxo do Processo
1. O código realiza a busca com os parâmetros fornecidos (CPF, NIS ou nome).
2. Ele navega pelas telas, extraindo os dados necessários.
3. Ao final, gera uma imagem da tela e a converte para base64, exibindo-a como evidência.
4. O primeiro dado consultado é sempre exibido de forma clara, garantindo que o processo seja transparente e fácil de verificar.

Isso facilita a verificação e garante a transparência no processo de automação, tornando-o mais confiável e acessível.
