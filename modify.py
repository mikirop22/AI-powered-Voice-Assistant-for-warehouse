"""import csv
import random

import pandas as pd

# Definir la ruta del archivo CSV
csv_file = "c:/Users/janbe/Desktop/products.csv"
# Definir las columnas adicionales
new_columns = ["fila", "columna", "costat"]

# Leer el archivo CSV y almacenar los datos en una lista de diccionarios
data = []
with open(csv_file, 'r', newline='') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        data.append(row)

# Iterar sobre los datos y agregar las nuevas columnas con valores aleatorios
for row in data:
    row['fila'] = random.randint(1, 10)
    row['columna'] = random.randint(1, 10)
    row['costat'] = random.choice(['L', 'R'])
    row['stock'] = random.randint(100,5000)

# Escribir los datos actualizados de vuelta al archivo CSV
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys(), delimiter=';')
    writer.writeheader()
    writer.writerows(data)

print("Se han añadido las nuevas variables al archivo CSV con éxito.")"""

# Función para limpiar el nombre
def clean_name(name):
    # Reemplazar comas por puntos decimales
    name = name.replace(",", ".")
    # Reemplazar guiones por espacios
    name = name.replace("-", " ")
    # Reemplazar '/' por 'por'
    name = name.replace("/", " por ")
    # Reemplazar 'ml' por 'mililitros'
    name = name.replace("ml", "mililitros")
    # Reemplazar 'mg' por 'miligramos'
    name = name.replace("mg", "miligramos")
    
    for i, nom in enumerate(name):
        if nom == 'x' or nom == 'X':
            if name[i+1].isdigit() and name[i-1].isdigit():
                name = name.replace("x", " por ")
                
    name = name.replace(' ', '_').replace('.', '')  # Aquí asignamos el resultado de los reemplazos nuevamente a 'name'
    
    return name


import pandas as pd

# Leer el conjunto de datos
df = pd.read_csv("products_new.csv", sep=";")

# Limpiar los nombres en el dataframe
df["cleaned_name"] = df["name"].apply(clean_name)

# Guardar el nuevo DataFrame en un archivo CSV
df.to_csv("products_new.csv", sep=";", index=False)