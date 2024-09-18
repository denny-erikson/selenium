from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
import time
import csv
from datetime import datetime


chrome_options = Options()
# chrome_options.add_argument("--headless")


driver = webdriver.Chrome()
# driver = webdriver.Chrome(options=chrome_options)

driver.get("https://data.anbima.com.br/fundos/385565")

driver.implicitly_wait(10)

def find_element_with_scroll(xpath, scroll_step=100, max_scroll=500):
    current_scroll = 0
    while current_scroll <= max_scroll:
        try:
            element = driver.find_element(By.XPATH, xpath)
            print(f"scroll_step: {scroll_step}")
            return element
        except NoSuchElementException:
            driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            current_scroll += scroll_step
            driver.save_screenshot(f'screenshot-{current_scroll}.png')
            print(f"current_scroll: {current_scroll}")
            time.sleep(1)
    raise Exception(f"Elemento com XPath '{xpath}' não encontrado após rolar {max_scroll} pixels.")

# XPath do elemento que queremos encontrar
xpath_to_find = '//*[@id="root"]/main/div[1]/nav/ul'

try:
    element = find_element_with_scroll(xpath_to_find)
    botao = element.find_element(By.XPATH, './/li[7]/a')

    driver.implicitly_wait(5)
    valor = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[4]/table/tbody/tr[1]/td[3]/span')
    print("Valor capturado:", valor.text)

    data_atual = datetime.now().strftime('%Y-%m-%d')

    script_path = os.path.abspath(__file__)
    script_directory = os.path.dirname(script_path)
    csvfile = os.path.join(script_directory, 'resultado.csv')

    linhas = []
    atualizar = False

    try:
        with open(csvfile, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header
            linhas = [header]  # Include the header in the lines list
            for linha in reader:
                if linha[0] == data_atual:
                    linha[1] = valor.text  # Update the value for the existing date
                    atualizar = True
                linhas.append(linha)
    except FileNotFoundError:
        linhas = [['Data', 'Valor'], [data_atual, valor.text]]  # Create a new file with header and new data

    with open(csvfile, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    print(f"Valor capturado e salvo em {csvfile}")

except Exception as e:
    print(f"error: {e}")

finally: 
    driver.quit()
