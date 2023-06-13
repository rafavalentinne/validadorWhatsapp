from time import sleep
import pandas as pd
from selenium import webdriver
import openpyxl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

validos = []
invalidos = []

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:\Perfil Chrome\Zap2")
navegador = webdriver.Chrome(options=chrome_options)

navegador.get('https://web.whatsapp.com/')

while len(navegador.find_elements('id', 'side')) < 1:
    sleep(1)

arquivo = pd.read_excel('base 2.xlsx')
base = pd.DataFrame(arquivo)

for i, cpf in enumerate(base["cpf"]):
    telefone = base.loc[i, 'telefone']
    i = i + 1
    link = f'https://web.whatsapp.com/send?phone={telefone}&text='
    navegador.get(link)

    try:
        elemento = WebDriverWait(navegador, 6).until(EC.presence_of_element_located(            (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')))
        navegador.find_element('xpath','//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').click()
        print(i, 'WhatsApp Válido')
        validos.append(telefone)
        base.loc[base["cpf"] == cpf, 'Whatsapp'] = 'Valido'
        base.to_excel('Numeros Validados2.xlsx', index=False)

    except Exception:
        print(i, 'WhatsApp Inválido')
        invalidos.append(telefone)
        base.loc[base["cpf"] == cpf, 'Whatsapp'] = 'Invalido'
        base.to_excel('Numeros Validados2.xlsx', index=False)
        pass

print('Fim do Código')
print('Whatsapp Válidos')
print(len(validos))
print('Whatsapp Inválidos')
print(len(invalidos))
