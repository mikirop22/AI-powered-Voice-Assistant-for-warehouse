import csv
from magatzem import Warehouse

warehouse = Warehouse(10, 10)

# Llegeix les dades del document products_new.csv i guarda les ubicacions dels productes
product_locations = {}
with open('c:/Users/janbe/Desktop/products_new.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Salta la primera fila (encapçalament)
    for row in reader:
        product_id = row[0]
        fila = int(row[3]) - 1  # Les files comencen des de 1, però l'índex de la llista comença des de 0
        columna = int(row[4]) - 1  # Les columnes comencen des de 1, però l'índex de la llista comença des de 0
        product_locations[product_id] = (fila, columna)

# Pregunta a l'usuari els IDs dels productes fins que introdueixi "fi"
product_ids = []
while True:
    product_id = input("Entra l'ID del producte (o 'fi' per acabar): ")
    if product_id == "fi":
        break
    if product_id in product_locations:
        product_ids.append(product_id)
    else:
        print("ID de producte invàlid. Torna-ho a provar.")

print("Productes seleccionats:")
for product_id in product_ids:
    print("- ID:", product_id)

# Allista els productes seleccionats
for product_id in product_ids:
    (x,y) = product_locations[product_id]
    warehouse.add_pick_location(x,y)

# Busca i visualitza el camí mínim per recollir els productes seleccionats al magatzem
print("\nCamí mínim per recollir els productes:")
start_x, start_y = 0, 0
path = warehouse.find_path(start_x, start_y)
warehouse.visualize_path(path)