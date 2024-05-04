import csv
from magatzem import Warehouse

magatzem = [[[0, None, 0] for _ in range(10)] for _ in range(10)]
for fila in magatzem:
    fila.append([None, None, None])

for fila in magatzem:
    fila.insert(0, [None, None, None])
    
with open('products_new.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Salta la primera fila (encapçalament)
    for row in reader:
        product_id = row[0]
        fila = int(row[3])-1  # Les files comencen des de 1, però l'índex de la llista comença des de 0
        columna = int(row[4])  # Les columnes comencen des de 1, però l'índex de la llista comença des de 0
        if row[5] == 'L':
            costat = 0
        elif row[5] == 'R':
            costat = 2

        magatzem[fila][columna][costat] = product_id  # Reemplaza el valor en la posición 2 de la lista

"""for fila in magatzem:
    print(fila)"""

warehouse = Warehouse(12, 10, magatzem)

# Llegeix les dades del document products_new.csv i guarda les ubicacions dels productes
product_locations = {}
with open('products_new.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Salta la primera fila (encapçalament)
    for row in reader:
        product_id = row[0]
        fila = int(row[3]) 
        columna = int(row[4]) 
        product_locations[product_id] = (fila, columna)

# Pregunta a l'usuari els IDs dels productes fins que introdueixi "fi"
product_ids = []
quantitas = {}
with open('list.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        product_id = row[0]
        product_ids.append(product_id)
        quantitat = row[1]
        quantitas[product_id] = quantitat
    
"""while True:
    product_id = input("Entra l'ID del producte (o 'fi' per acabar): ")
    if product_id == "fi":
        break
    if product_id in product_locations:
        product_ids.append(product_id)
    else:
        print("ID de producte invàlid. Torna-ho a provar.")"""

print("Productes seleccionats:")
for product_id in product_ids:
    print("- ID:", product_id)

# Allista els productes seleccionats
for product_id in product_ids:
    
    (x,y) = product_locations[product_id]
    warehouse.add_pick_location(x,y)
    warehouse.add_pick_location_id((x,y),product_id)

# Busca i visualitza el camí mínim per recollir els productes seleccionats al magatzem
print("\nCamí mínim per recollir els productes:")
start_x, start_y = 0, 0
path = warehouse.find_min_path(start_x, start_y)

if path is not None:
    warehouse.visualize_path(path)
else:
    print("No se encontró un camino válido.")