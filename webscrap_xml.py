from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import shutil

chrome_options = Options()
# chrome_options.add_argument("--headless")


driver = webdriver.Chrome()

try:
    url = "https://nfe.sgpcloud.net:9088/issweb/consultarautenticidade.jsf?hash=436230ZXAB9WDALIF4D0C426Z5V5CV3B"
    case_search = "GerarXml"

    # Acessa a página
    driver.get(url)

    # Aguarda até que os botões sejam carregados
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))

    # Encontra os botões na página
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for button in buttons:
        button_id = button.get_attribute('id') or ''
        button_name = button.get_attribute('name') or ''

        # Verifica se o botão termina com o texto desejado
        if case_search.casefold() in button_id.casefold() or case_search.casefold() in button_name.casefold():
            print(f"Botão encontrado! id: {button_id}, name: {button_name}")

            # Clica no botão
            ActionChains(driver).move_to_element(button).click(button).perform()
            print("Botão clicado!")

            download_dir = r'C:\\Users\\denny.pimenta\\Downloads'  # Substitua pelo caminho correto do diretório de download
            destination_dir = r'C:\\Users\\denny.pimenta\\dev\\python\\selenium\\files'  # Substitua pelo caminho correto do diretório de destino
            timeout = 60  # Tempo máximo de espera em segundos
            end_time = time.time() + timeout

            while time.time() < end_time:
                for filename in os.listdir(download_dir):
                    if filename.endswith('.xml'):
                        print(f"Arquivo XML encontrado: {filename}")
                        source_file = os.path.join(download_dir, filename)
                        destination_file = os.path.join(destination_dir, filename)
                        shutil.copy(source_file, destination_file)
                        print(f"Arquivo XML copiado para: {destination_file}")
                        break
                else:
                    time.sleep(1)
                    continue
                break
            else:
                print("Arquivo XML não encontrado dentro do tempo limite.")
            

except Exception as e:
    print("Botão não encontrado.")
    print(f"Ocorreu um erro: {e}")

finally:
    # Finaliza o navegador
    # driver.quit()
    pass