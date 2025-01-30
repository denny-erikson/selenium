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


env_dir = os.path.expanduser("~")
download_dir = os.path.join(env_dir, 'Downloads')

project_dir = os.path.dirname(os.path.abspath(__file__))
destination_dir = os.path.join(project_dir, 'files')

chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome()

def get_search(case_search, url):
    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))

        buttons = driver.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            button_id = button.get_attribute('id') or ''
            button_name = button.get_attribute('name') or ''

            if case_search.casefold() in button_id.casefold() or case_search.casefold() in button_name.casefold():
                print(f"Botão encontrado! id: {button_id}, name: {button_name}")

                ActionChains(driver).move_to_element(button).click(button).perform()
                print("Botão clicado!")
                
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
                            return destination_file                            
                    else:
                        time.sleep(1)
                        continue
                    break
                else:
                    print("Arquivo XML não encontrado dentro do tempo limite.")
                

    except Exception as e:
        print("Botão não encontrado.")
        print(f"Ocorreu um erro: {e}")
        return None

    finally:
        # Finaliza o navegador
        # driver.quit()
        pass


url = "https://nfe.sgpcloud.net:9088/issweb/consultarautenticidade.jsf?hash=436230ZXAB9WDALIF4D0C426Z5V5CV3B"
case_search = "GerarXml"
xmlfile = get_search(case_search, url)
print(f"xmlfile:  {xmlfile}")
