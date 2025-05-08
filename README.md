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
