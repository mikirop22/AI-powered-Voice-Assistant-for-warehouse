import csv
import random

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

print("Se han añadido las nuevas variables al archivo CSV con éxito.")
