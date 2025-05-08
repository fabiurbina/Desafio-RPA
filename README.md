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

## Exemplo de saída 1 (consulta por CPF ou NIS):
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
```

## Exemplo de saída 2 (consulta por Nome - múltiplos resultados):
```json
[
  {
    "nome": "Pessoa 1",
    "link": "link da página onde os dados foram coletados",
    "beneficio": "Bolsa Família",
    "nis": "1111111",
    "valor": "400,00",
    "imagem": "Imagem64Pessoa1"
  },
  {
    "nome": "Pessoa 2",
    "link": "link da página onde os dados foram coletados",
    "beneficio": "Auxílio Emergencial",
    "nis": "3333333",
    "valor": "600,00",
    "imagem": "Imagem64Pessoa2"
  }
]
```
## Exemplo de saída 3 (consulta não localizada):
```json
[
  {
    "validos": [],
    "invalidos": [
        {
            "item": 1,
            "status": "Item não existe na página"
        },
        {
            "status": "CPF/NIS não encontrado"
        }
    ]
}
]
```

## Bibliotecas Necessárias

```python
from selenium import webdriver  # Automação de navegador web
from selenium.webdriver.chrome.service import Service  # Gerenciamento do serviço do ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager  # Gerencia automaticamente o download do ChromeDriver
from selenium.webdriver.common.by import By  # Localizadores de elementos (ID, XPATH, etc.)
from selenium.webdriver.support.ui import WebDriverWait  # Espera por condições específicas
from selenium.webdriver.support import expected_conditions as EC  # Condições esperadas para o WebDriverWait
from selenium.webdriver.common.keys import Keys  # Simula pressionamento de teclas
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException  # Exceções do Selenium
import time  # Manipulação de tempo (ex.: time.sleep())
import sys  # Acesso a funções do sistema (ex.: sys.exit())
import base64  # Codificação e decodificação de dados em base64
from PIL import Image  # Manipulação de imagens (ex.: abrir e exibir imagens)
import pandas as pd  # Manipulação de dados estruturados (DataFrames)
import json  # Trabalha com dados no formato JSON
from io import BytesIO  # Manipula dados binários na memória
import re  # Expressões regulares (para buscar padrões em strings)

