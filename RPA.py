
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

#--------------------------------------------------------------------------------------------------------------------------------------

#Função para informar os dados para pesquisar 
def parametro_pessoal():
    cpf_nome_nis = input("Digite o CPF, NIS OU NOME (Obs: CPF e NIS informe apenas os números sem pontos ou traços): ") 
    return cpf_nome_nis  # retorna os valores para uso

#---------------------------------------------------------------------------------------------------------------------------------------

#Função para escolher o Beneficio soscial
def parametro_busca(): #FIXME: Essa para acrescentar mais opções no imput de busca é necessário adcionar manualmente outra opção após 
                        # palavra "Beneficiário de Programa Social" da lista "opções".
    opcoes = [
        "Beneficiário de Programa Social",
    ]

    print("Escolha uma das opções de busca:")
    for i, opcao in enumerate(opcoes, start=1):
        print(f"{i}. {opcao}")

    escolha = int(input("Digite o número da opção desejada: "))

    if 1 <= escolha <= len(opcoes):
        return [opcoes[escolha - 1]]  # retorna como lista para manter a lógica
    else:
        print("Opção inválida. Tente novamente.")
        return parametro_busca()
    

    
#----------------------------------------------------------------------------------------------------------------------------------------
#FIXME: Função principal do projeto, a partir dessa função o RPA vai fazer as buscas no portal da transparência
def abrir_site():
    
    #URL contem o site onde vammos realizar as buscas
    url = "https://portaldatransparencia.gov.br/pessoa/visao-geral"

    options = webdriver.ChromeOptions()  # Cria uma instância para configurar o navegador

    # Configurações para rodar o navegador sem interface gráfica (modo headless)
    options.add_argument("--headless=new")  # Modo headless (sem interface gráfica)
    options.add_argument("--disable-gpu")  # Desabilita o uso de GPU (necessário para rodar headless em alguns casos)
    options.add_argument("--no-sandbox")  # Desabilita o sandboxing, necessário em ambientes sem interface gráfica
    options.add_argument("--disable-dev-shm-usage")  # Evita o uso excessivo de memória compartilhada no ambiente Docker
    options.add_argument("--window-size=1920,1080")  # Define o tamanho da janela do navegador

    # Disfarces contra deteção de bots
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")  # Simula um user-agent comum
    options.add_argument("--disable-blink-features=AutomationControlled")  # Desabilita a detecção de automação
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Remove o aviso de automação no navegador
    options.add_experimental_option("useAutomationExtension", False)  # Desativa a extensão de automação do Chrome

    # Inicia o Chrome com as opções configuradas
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Abre a URL desejada
    driver.get(url)

    tempo = 10 # Essa variavel tempo vai controlar todos os webdrivers, fazendo com que seja aguardado até 10 segundos 
                #para que o elemento esteja presente na tela
    #---------------------------------------------------------------------------------------------------------------------------------
    # Aqui aceitamoms os termos exigido ao abrir a pagina 
    try:
        aceitar = WebDriverWait(driver, tempo).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='accept-all-btn']"))
            )
        aceitar.click()
    except TimeoutError:
        print("Elemento não encontrado encerrando o codigo!")
        sys.exit()
    #---------------------------------------------------------------------------------------------------------------------------------
    #selecionar buscas
    try:
        buscas = WebDriverWait(driver, tempo).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='button-consulta-pessoa-fisica']"))
        )
        buscas.click()
    except TimeoutError:
        print("Elemento não encontrado encerrando o codigo!")
        sys.exit()
    #---------------------------------------------------------------------------------------------------------------------------------
    # Aqui aceitamoms os termos exigido ao abrir a pagina 
    try:
        aceitar = WebDriverWait(driver, tempo).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='accept-all-btn']"))
                )
        aceitar.click()
    except TimeoutError:
        print("Elemento não encontrado encerrando o codigo!")
        sys.exit()
    #---------------------------------------------------------------------------------------------------------------------------------
    # Neste elemento informamos o parametro NOME, CPF OU NIS conforme a função "cpf_nome_nis"
    
    try:
        campo_cpf_nome_nis = WebDriverWait(driver, tempo).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='termo']"))
                )
        campo_cpf_nome_nis.click()
        campo_cpf_nome_nis.send_keys(cpf_nome_nis) 
    except TimeoutError:
        print("Elemento não encontrado encerrando o codigo!")
        sys.exit()
    #---------------------------------------------------------------------------------------------------------------------------------
    # Abre o campo para identificar o elemento de busca para o prósmo passo
    try:
        refinebusca = WebDriverWait(driver, tempo).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='accordion1']/div[1]/button"))
                )
        refinebusca.click()
    except TimeoutError:
        print("Elemento não encontrado encerrando o codigo!")
        sys.exit()
    #---------------------------------------------------------------------------------------------------------------------------------
    #flega a opção de beneficiario programa social para dar outros caminho podemos incluir um elif para seguir para outro tipo de opção
    if parametro_busca == 1:
        try:
            programasocial = WebDriverWait(driver, tempo).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='box-busca-refinada']/div[1]/div[2]/div/label"))
                    )
            programasocial.click()
        except TimeoutError:
            print("Elemento não encontrado encerrando o codigo!")
            sys.exit()
    #---------------------------------------------------------------------------------------------------------------------------------
    #Essa parte será feito a primeira consulta real e carregará os dados na tela, sendo apenas 1 para CPF ou NIS e até 10 itens por nome
    try:
        consultar_cpf = WebDriverWait(driver, tempo).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='btnConsultarPF']"))
                )
        consultar_cpf.click()
        time.sleep(5) # tempo de seguntança para os casos ficarem presentes na tela
    except TimeoutError:
            print("Elemento não encontrado encerrando o codigo!")
            sys.exit() 
    #---------------------------------------------------------------------------------------------------------------------------------
   
    #FIXME: Primeira parte em que vamos coletar dados, aqui ele pode pegar apenas o primeiro

    nomes_links = []  # Armazena os resultados válidos encontrados (nome e link)
    nomes_links_invalidos = []  # Armazena informações sobre falhas ou itens inválidos

    
    # Verifica se a entrada é um CPF ou NIS (somente números)
    if cpf_nome_nis.isdigit():
        limite = 2  # CPF/NIS: tenta apenas o primeiro item (índice 1)
    else:
        limite = 11  # Nome: tenta até 10 itens (índices de 1 a 10)

    # Itera sobre os possíveis resultados da pesquisa
    for i in range(1, limite):
        xpath = f'//*[@id="resultados"]/div[{i}]/div/div[1]/a'
        elementos = driver.find_elements(By.XPATH, xpath)  # Verifica se o item existe no DOM

        if elementos:
            try:
                # Aguarda até que o elemento esteja visível na tela
                elemento = WebDriverWait(driver, tempo).until(
                    EC.visibility_of_element_located((By.XPATH, xpath))
                )
                nome = elemento.text.strip()  # Extrai o texto do nome
                link = elemento.get_attribute('href')  # Extrai o link do resultado
                if nome and link:
                    nomes_links.append({'nome': nome, 'link': link})  # Adiciona à lista de válidos
                    if cpf_nome_nis.isdigit():  # Para CPF/NIS, encontrou 1 resultado, já pode encerrar
                        break
                else:
                    # Nome ou link ausentes ou vazios
                    nomes_links_invalidos.append({'item': i, 'status': 'Nome ou link vazio'})
            except Exception as e:
                # Erro ao tentar acessar o elemento visível
                nomes_links_invalidos.append({'item': i, 'status': f'Erro ao acessar: {e}'})
        else:
            # Elemento não encontrado no DOM (índice inválido)
            nomes_links_invalidos.append({'item': i, 'status': 'Item não existe na página'})

    # Se nenhum resultado válido for encontrado
    if not nomes_links:
        status = 'CPF/NIS não encontrado' if cpf_nome_nis.isdigit() else 'Nenhum item encontrado com o nome fornecido'
        nomes_links_invalidos.append({'status': status})

    # Saída em JSON com os resultados válidos e os erros/ausências
    saida = {
        'validos': nomes_links,
        'invalidos': nomes_links_invalidos
    }
    print(json.dumps(saida, indent=4, ensure_ascii=False))

    # Tenta clicar no primeiro resultado encontrado
    try:
        resultado = WebDriverWait(driver, tempo).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='resultados']/div/div/div[1]/a"))
        )
        resultado.click()
    except TimeoutException:
        # Se nenhum resultado for clicável (0 resultados), encerra o script
        print("Nenhum resultado encontrado – 0 resultados obtidos.")
        sys.exit()


    #---------------------------------------------------------------------------------------------------------------------------------
    
     #solicita novamente a confirmação
    try:
        aceitar = WebDriverWait(driver, tempo).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='accept-all-btn']"))
                )
        aceitar.click()
    except TimeoutError:
         print("Elemento não encontrado encerrando o codigo!")
         sys.exit() 
    #---------------------------------------------------------------------------------------------------------------------------------
    try:
        #acessar o panorama
        panorama = WebDriverWait(driver, tempo).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='accordion1']/div[1]/button"))
                )
        panorama.click()
    except TimeoutError:
        print("Elemento não encontrado encerrando o codigo!")
        sys.exit() 
    #---------------------------------------------------------------------------------------------------------------------------------
    #FIXME: Esse caso foi necessário usar javascript para centralizar corretamente a posição para melhor saída do print na tela
    
    time.sleep(5) 
    try:
        rec = WebDriverWait(driver, tempo).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='accordion1']/div[1]/button/span[2]"))
        )

        # Faz a página rolar até o botão
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", rec)

        # Aguarda um segundo para o scroll acontecer (opcional)
        time.sleep(1)

        # Clica no botão
        rec.click()
    except TimeoutError:
        print("Elemento não encontrado encerrando o codigo!")
        sys.exit() 
    #---------------------------------------------------------------------------------------------------------------------------------
    
    #FIXME: Gera captura da evidencia para o primeiro caso coletado
    driver.save_screenshot("screenshot.png")

    # Abre o arquivo e converte para base64 (isso será feito apenas para o primeiro item)
    with open("screenshot.png", "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

     #---------------------------------------------------------------------------------------------------------------------------------

    dados_coletados = [] # lista para coletar os dados

    # Loop pelos links coletados
    for idx, item in enumerate(nomes_links):
        #print(f"\n🔗 Acessando: {item['nome']} - {item['link']}")

        try:
            driver.get(item['link'])
            time.sleep(2)

            # Clica no botão para expandir o recebimento
            rec = WebDriverWait(driver, tempo).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='accordion1']/div[1]/button/span[2]"))
            )
            rec.click()

            # Aguarda o conteúdo expandido carregar
            WebDriverWait(driver, tempo).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='accordion-recebimentos-recursos']"))
            )
            
            # Coleta os dados desejados
            try:
                dado1 = driver.find_element(By.XPATH, "//*[@id='accordion-recebimentos-recursos']/div/div/div/div/Strong").text.strip()
            except:
                dado1 = None

            try:
                dado2 = driver.find_element(By.XPATH, "//*[@id='tabela-visao-geral-sancoes']/tbody/tr/td[2]").text.strip()
            except:
                dado2 = None

            try:
                dado3 = driver.find_element(By.XPATH, "//*[@id='tabela-visao-geral-sancoes']/tbody/tr/td[3]").text.strip()
            except:
                dado3 = None

            try:
                dado4 = driver.find_element(By.XPATH, "//*[@id='tabela-visao-geral-sancoes']/tbody/tr/td[4]").text.strip()
            except:
                dado4 = None

            #cria uma lista de dicionarios com os dados coletados nos links, na primeira condição do if armazena o primeiro resultado com a evidencia
            if idx == 0:
                dados_coletados.append({
                    'nome': item['nome'],
                    'link': item['link'],
                    'beneficio': dado1,
                    'nis': dado2,
                    'Valor': dado4,
                    'imagem': base64_image  # Imagem base64 apenas para o primeiro item
                })
            else:
                # Para os demais itens, não adiciona a imagem
                dados_coletados.append({
                    'nome': item['nome'],
                    'link': item['link'],
                    'beneficio': dado1,
                    'nis': dado2,
                    'Valor': dado4
                })

        except Exception as e:
            print("Erro ao processar o link: {e}")
            

    # Converte os dados coletados em DataFrame
    df = pd.DataFrame(dados_coletados)


    # Salva todos os dados em um arquivo JSON
    df.to_json("dados_coletados.json", orient="records", force_ascii=False, indent=4)

    # Exibe apenas o primeiro registro como JSON
    if not df.empty:
        primeiro_registro_json = df.iloc[[0]].to_json(orient="records", force_ascii=False, indent=4)
        print("\n Primeiro registro em JSON:")
        print(primeiro_registro_json)
        
        # Decodificando o base64 para obter os dados da imagem
        image_data = base64.b64decode(base64_image)

        # Abrindo a imagem com PIL
        image = Image.open(BytesIO(image_data))

        # Exibindo a imagem
        image.show()

        # Retornando o DataFrame e o JSON após a exibição da imagem
        return df, primeiro_registro_json  # <- agora está no final da função

 #----------------------------------------------------------------------------------------------------------------------------------------  
    

# Chamada da função
cpf_nome_nis = parametro_pessoal() #Chama a função de informar CPF, NOME OU NIS
opcoes = parametro_busca() #Chama a função para selecionar o tipo de beneficio, por ora apenas 1 tipo de beneficio na lista
Abrir = abrir_site() #Chama o RPA que vai fazer as buscas das informações, codigo principal
