#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Descarga todas las fotografias de un perfil de VSCO en unos pocos segundos
# by Xabierland https://github.com/Xabierland

#Modulos y librerias
from selenium import webdriver, common
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os, requests, time, argparse


def parse_arguments():
    # Definir los argumentos con sus valores por defecto
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", type=float, default=0.5, help="El valor por defecto es 0.5 pero puedes aumentarlo si la velocidad de tu internet es mala.")
    parser.add_argument("-H", "--headerless", action="store_true", default=False, help="Ejecuta el navegador en modo headless (Puede provocar errores)")

    # Analizar los argumentos de la línea de comandos
    args = parser.parse_args()

    # Asignar los valores de los argumentos a variables globales
    global t, headerless
    t = args.time
    headerless = args.headerless

#Mediante la url que recibe como parametro esta funcion crea un carpeta con dicho nombre donde se descargaran
#posteriormente todas las fotografias que descargue el programa
def create_folder(url):
    parsed_url = urlparse(url)
    username = parsed_url.path.split('/')[1]
    folder_name = 'img/'+ username
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

#VSCO tiene una pagina web con carga dinamica, es decir, el contenido carga a medida que se hace
#scroll hacia abajo lo que impide conseguir directamente el contenido html de la pagina con una siemple
#request, es por eso que usamos el navegador selenium para navegar con la pagina y obligarla a cargar
#todo el contenido antes de descargarlo
def load_page(url):
    # Configuro y inicia el navegador Selenium
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    if headerless:
        options.add_argument('--headless')  # Ejecuta el navegador en modo headless
    driver = webdriver.Chrome(options=options)
    
    # Navega a la página web que quieres procesar
    driver.get(url)

    # Haz clic en el boton "Reject All" de las cookies
    time.sleep(t)
    driver.find_element(By.ID, "onetrust-reject-all-handler").click()

    # Haz clic en el boton "Cargar más"
    time.sleep(t)
    driver.find_element(By.CSS_SELECTOR, 'button.css-178kg8n.e1xqpt600').click()

    # Haz scroll hacia abajo hasta el final de la página
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(t)  # Espera a que se cargue el contenido dinámicamente
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Obtén todo el HTML de la página
    html = driver.page_source
    # Cierra el navegador web
    driver.quit()
    return html

#Una vez obtenido el html completo de la pagina nos quedamos unicamente con el contenido que tiene
#una URL que contenga /media/ que es como VSCO guarda las fotografias
def get_media_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=lambda href: href and '/media/' in href)
    return links
    
#Descarga las fotos que recibe por parametro en la carpeta creada
def download_photos(media,folder_name):
    id=0
    for photo in media:
        id+=1
        soup = BeautifulSoup(str(photo), 'html.parser')
        img = soup.find('img')
        url = img['src']
        full_url = urljoin('https:', url)
        response = requests.get(full_url)
        file_name = full_url.split("/")[-1]
        with open(folder_name+"/"+str(id)+'.jpg', "wb") as f:
            f.write(response.content)


def main():
    #Pregunta por la URL
    print("Insert the URL")
    print("Example:(https://vsco.co/Xabierland/gallery)")
    url=input("--> ")
    #Crea la carpeta
    print("Creando carpeta...")
    folder_name=create_folder(url)
    #Descarga el html
    print("Descargando la pagina web...")
    html=load_page(url)
    #Obtiene los links de las fotos
    print("Seleccionando fotografias...")
    media=get_media_url(html)
    #Descarga todas las fotos en la carpeta
    print("Descargando fotografias...")
    download_photos(media,folder_name)
    print("Listo!\n")
    

if __name__=='__main__':
    parse_arguments()
    main()