import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base de la página web de Vianney
base_url = 'https://vianney.com.mx/collections/novedades-%F0%9F%94%A5?page={}'

all_data = []

# Pagina inicial 
page_number = 1

# Final de las paginas
end_of_pages = False


while not end_of_pages:

    url = base_url.format(page_number)

    r = requests.get(url)
    print(f"Status code for page {page_number}: {r.status_code}")
    
    soup = BeautifulSoup(r.content, 'html.parser')
    productos = soup.find_all('a', class_='product-info__caption')


    if not productos:
        print("No hay más páginas disponibles.")
        end_of_pages = True
        continue

    for producto in productos:
        titulo = producto.find('span', class_='title').text.strip()
        url_producto = 'https://vianney.com.mx' + producto.get('href')
        precio = producto.find('span', class_='money').text.strip()
        all_data.append({'TITULO': titulo, 'URLS': url_producto, 'PRECIOS': precio})

    # Verificar si el botón de "Siguiente" está presente en la página
    next_button = soup.find('span', class_='next')
    if not next_button:
        print("No hay más páginas disponibles.")
        end_of_pages = True
        continue
    page_number += 1


df = pd.DataFrame(all_data)

# Imprimir en consola
print(df)

# (Pongan su direcorio xd)
df.to_csv('D:/ACTIVIDADES INNI/6to Semestre/Programacion para Internet/Novedades_Vianey.csv', index=False)

try:
    df.to_csv('datos_vianney_todas_paginas.csv', index=False)
    print("Archivo CSV generado exitosamente.")
except Exception as e:
    print("Error al generar el archivo CSV:", e)
