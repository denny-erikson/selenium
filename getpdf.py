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
import requests


env_dir = os.path.expanduser("~")
download_dir = os.path.join(env_dir, 'Downloads')

project_dir = os.path.dirname(os.path.abspath(__file__))
destination_dir = os.path.join(project_dir, 'files')

# Configuração do ChromeOptions para ativar DevTools Protocol
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--log-level=0")
chrome_options.add_argument("--enable-blink-features=NetworkService,NetworkServiceInProcess")
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(options=chrome_options)

def get_search(url):
    case_search = "Imprimir NFS-e".replace(' ', '').casefold()
    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'button')))

        buttons = driver.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            button_id = button.get_attribute('id') or ''
            button_name = button.get_attribute('name') or ''
            print(f"Botãos testados! id: {button_id}, name: {button_name}")

            case_search = "Imprimir NFS-e".replace(' ', '').casefold()

            try:
                spans = button.find_elements(By.TAG_NAME, 'span')
                for span in spans:
                    span_text = span.text.replace(' ', '').casefold()
                    print(f"span encontrado! name: {button_name}, span_text: {span_text}")

                    if case_search in span_text:
                        print(f"Botão encontrado! id: {button_id}, name: {button_name}, span_text: {span_text}")
                        ActionChains(driver).move_to_element(button).click(button).perform()
                        print("Botão clicado!")

                        # Espera a nova guia abrir
                        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

                        # Alterna para a nova guia
                        second_window_handle = driver.window_handles[1]
                        if driver.current_window_handle != second_window_handle:
                            driver.switch_to.window(second_window_handle)
                            print("Nova guia aberta! URL:", driver.current_url)

                            
                            # Captura o URL do PDF do elemento <embed>
                            embed_element = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.TAG_NAME, 'embed'))
                            )
                            pdf_url = embed_element.get_attribute('src')
                            print(f"URL do PDF: {pdf_url}")

                            time.sleep(5)

                            # Capturar logs de rede para encontrar a URL do PDF
                            logs = driver.get_log("performance")
                            pdf_url = None
                            for entry in logs:
                                message = entry["message"]
                                if "Network.responseReceived" in message and "application/pdf" in message:
                                    try:
                                        url_start = message.index("url") + 6
                                        url_end = message.index('"', url_start)
                                        pdf_url = message[url_start:url_end]
                                        break
                                    except ValueError:
                                        continue

                            if pdf_url:
                                print(f"URL do PDF encontrada: {pdf_url}")

                                # Baixar o PDF
                                response = requests.get(pdf_url)
                                if response.status_code == 200:
                                    with open("arquivo.pdf", "wb") as f:
                                        f.write(response.content)
                                    print("PDF baixado com sucesso!")
                                else:
                                    print("Erro ao baixar o PDF.")
                            else:
                                print("Não foi possível capturar a URL do PDF.")
            except Exception as e:
                print(f"Erro ao tentar encontrar o span: {e}")
                continue
                

    except Exception as e:
        print("Botão não encontrado.")
        print(f"Ocorreu um erro: {e}")
        return None

    finally:
        # Finaliza o navegador
        # driver.quit()
        pass


url = "https://nfe.sgpcloud.net:9088/issweb/consultarautenticidade.jsf?hash=436230ZXAB9WDALIF4D0C426Z5V5CV3B"

pdffile = get_search(url)
print(f"pdffile:  {pdffile}")
