from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
import time

# Ruta al controlador de Selenium. Descarga el controlador adecuado para tu navegador desde https://selenium-python.readthedocs.io/installation.html#drivers

# Ruta al EdgeDriver
driver_path = "C:/Users/Usuario/OneDrive - Universitat Politècnica de Catalunya/Escritorio/HackUPC/edgedriver_win64/msedgedriver.exe"

# Opciones para Edge con el modo IE
options = webdriver.EdgeOptions()
options.use_chromium = True  # Indica que quieres usar la versión Chromium de Edge
options.add_argument("ie.mode=IE11")  # Activa el modo IE

# Especificar la ruta del ejecutable con Service
service = Service(executable_path=driver_path)

# Inicializar el navegador con las opciones y el servicio
driver = webdriver.Edge(service=service, options=options)


# URL de la página web
url = "https://www.naturalreaders.com/online/"

# Abrir la página web en el navegador
driver.get(url)

# Esperar unos segundos para que se cargue la página completamente
time.sleep(5)

# Encontrar el cuadro de texto donde se introduce el texto
text_box = driver.find_element_by_xpath("//textarea[@name='text']")

# Introducir el texto que deseas convertir a voz
text_to_speak = "Tu texto aquí"
text_box.send_keys(text_to_speak)

# Hacer clic en el botón de reproducción para generar el audio
play_button = driver.find_element_by_xpath("//button[@aria-label='Play']")
play_button.click()

# Esperar unos segundos para que se genere el audio
time.sleep(10)

# Hacer clic en el botón de descarga para descargar el audio en formato MP3
download_button = driver.find_element_by_xpath("//button[@aria-label='Download']")
download_button.click()

# Esperar unos segundos para que se complete la descarga
time.sleep(5)

# Cerrar el navegador
driver.quit()

""" 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.naturalreaders.com/online/"

# Abrir el sitio web
driver = webdriver.Chrome()  # Asegúrate de tener el driver correcto para tu navegador
driver.get(url)

try:
    # Esperar hasta que el cuadro de texto esté disponible
    text_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "editArea"))
    )

    # Introducir el texto que deseas convertir a voz
    text = "Tu texto aquí"
    text_area.send_keys(text)

    # Ejecutar JavaScript para hacer clic en el botón de reproducción
    driver.execute_script("document.getElementById('playBtn').click();")

    # Esperar hasta que el botón de descarga esté disponible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "saveButton"))
    )

    # Ejecutar JavaScript para hacer clic en el botón de descarga
    driver.execute_script("document.getElementById('saveButton').click();")

finally:
    # Cerrar el navegador después de una pausa
    time.sleep(5)
    driver.quit()
""" 
