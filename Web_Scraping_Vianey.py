import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL base de la página web de Vianney
base_url = 'https://vianney.com.mx/collections/novedades-%F0%9F%94%A5?page={}'

all_data = []

# Pagina inicial  
numero_pagina = 1

# Final de las paginas
fin_paginas = False

while not fin_paginas:

    url = base_url.format(numero_pagina)

    r = requests.get(url)
    print(f"Pagina {numero_pagina}: {r.status_code}")
    
    soup = BeautifulSoup(r.content, 'html.parser')
    productos = soup.find_all('a', class_='product-info__caption')

    if not productos:
        print("No hay más páginas disponibles.")
        fin_paginas = True
        continue

    for producto in productos:
        titulo = producto.find('span', class_='title').text.strip()
        url_producto = 'https://vianney.com.mx' + producto.get('href')
        precio = producto.find('span', class_='money').text.strip()
        precio_anterior_etiqueta = producto.find('span', class_='was_price')
        # Por si no tiene la clase "was_price" el articulo
        precio_anterior = None
        if precio_anterior_etiqueta:
            precio_anterior_span = precio_anterior_etiqueta.find('span', class_='money')
            if precio_anterior_span:
                precio_anterior = precio_anterior_span.text.strip()
        all_data.append({'TITULO': titulo, 'URLS': url_producto, 'PRECIO_OFERTA': precio, 'PRECIO_ANTERIOR': precio_anterior})

    # Verificar si el botón de "Siguiente" está presente en la página
    next_button = soup.find('span', class_='next')
    if not next_button:
        print("No hay más páginas disponibles.")
        fin_paginas = True
        continue
    numero_pagina += 1


df = pd.DataFrame(all_data)

# Imprimir en consola
print(df)

# (Pongan su direcorio xd)
df.to_csv('D:/ACTIVIDADES INNI/6to Semestre/Programacion para Internet/Articulos_Vianey.csv', index=False)

try:
    df.to_csv('Articulos_Vianey.csv', index=False)
    print("Archivo CSV generado exitosamente.")
except Exception as e:
    print("Error al generar el archivo CSV:", e)
