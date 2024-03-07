import time
from selenium import webdriver
from getpass import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException, NoSuchElementException

# Solicitar credenciais do usuário
print("Digite suas credenciais para que a automação realize a extração da fatura da vivo")
email = input("Digite seu e-mail: ")
senha = getpass("Digite sua senha: ")
print("Iniciando extração, não mexa no mouse nem no teclado ate o final do processo")

# Abrir navegador e acessar portal da vivo
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://mve.vivo.com.br/")
time.sleep(1)

# Fazer login
element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='login-input']"))
)
login_email = driver.find_element(By.XPATH, "//input[@id='login-input']")
login_email.send_keys(email)
btn_login = driver.find_element(By.XPATH, "//button[@type='submit']")
btn_login.click()

element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
)
login_password = driver.find_element(By.XPATH, "//input[@type='password']")
login_password.send_keys(senha)
btn_login = driver.find_element(By.XPATH, "//button[@type='submit']")
btn_login.click()

#Pular pagina de atualização de dados
element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Você precisa atualizar seu número de celular')] "))
    )
skip_btn = driver.find_element(By.XPATH, "//button[@id='button-skip-update']")
skip_btn.click()

try:
    # Verifica se o elemento está presente e visível
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='dialog-close dialog-icon']"))
    )

    # Executa as ações se o elemento estiver presente e visível
    btn_fechar_download = driver.find_element(By.XPATH, "//div[@class='dialog-close dialog-icon']")
    btn_fechar_download.click()

    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "cancel-download-confirm-button"))
    )

    driver.find_element(By.ID, "cancel-download-confirm-button").click()

except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    # Lidere com o caso em que os elementos não estão presentes ou visíveis
    print("Elementos não estão presentes ou visíveis. Pulando para o restante do código.")


#Acessar pagina das contas
element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Ver contas')]"))
    )

ver_contas = driver.find_element(By.XPATH, "//span[contains(text(), 'Ver contas')]")
ver_contas.click()


#Localizar a ultima conta
element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='dropdown-right'][1]"))
    )

btn_baixar_agora = driver.find_element(By.XPATH, "//div[@id='dropdown-right'][1]")
btn_baixar_agora.click()

#Baixar conta detalhada 
element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Conta detalhada (.pdf)')]"))
    )

btn_conta_detalhada = driver.find_element(By.XPATH, "//button[contains(text(),'Conta detalhada (.pdf)')]")
btn_conta_detalhada.click()

element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Download realizado com sucesso')]"))
    )

time.sleep(20)
driver.quit()

print("Fim da extração")