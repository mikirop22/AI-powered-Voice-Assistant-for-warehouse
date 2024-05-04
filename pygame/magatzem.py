import heapq
from visualitzar import visualitza

class Warehouse:
    def __init__(self, width, height, magatzem):
        self.width = width
        self.height = height
        self.grid = [[0] * width for _ in range(height)]  # Initialize grid with all zeros
        self.pick_locations = []
        self.pick_locations_id = []
        self.obstacles = set()
        self.one_way_aisles = {}
        self.magatzem = magatzem

    def add_pick_location(self, x, y):
        self.pick_locations.append((x, y))
        self.pick_locations = sorted(self.pick_locations, key=lambda location: location[1])
        
    def add_pick_location_id(self, pos, product_id):
        self.pick_locations_id.append(((pos, product_id)))

    def set_obstacle(self, x, y):
        self.obstacles.add((x, y))


    def set_one_way_aisle(self, x, y, direction):
        self.one_way_aisles[(x, y)] = direction

    def heuristic(self, x, y, path):
        # Calcula la distancia acumulada desde el punto de inicio hasta el punto actual en el camino
        return len(path)        
    
    def min_moves_to_point(self, current_x, current_y, destino_x, destino_y):
        camino = [(current_x, current_y)]  # Inicializamos el camino con el punto inicial
            
        if current_y != destino_y and (current_x != 0 or current_x != 11):
            closest_column = 0 if current_x <= self.width / 2 else self.width - 1

            if current_x < closest_column:
                for x in range(current_x, closest_column):
                    camino.append((x + 1, current_y))
                    current_x = x + 1
 
            else:
                moure_x = abs(closest_column-current_x)
                for x in range(1,moure_x+1):
                    print(current_x- x)
                    camino.append((current_x - x, current_y))
                current_x = closest_column 
                    
            if current_y < destino_y:
                for y in range(current_y, destino_y):
                    camino.append((current_x, y + 1))
                    current_y = y + 1
            else:
                for y in range(destino_y, current_y):
                    camino.append((current_x, y - 1))
                    current_y = y - 1

        if current_x < destino_x:
            
            for x in range(current_x, destino_x):
                camino.append((x + 1, current_y))
                current_x = x + 1   
        else:
            moure_x = abs(destino_x-current_x)
            for x in range(1,moure_x+1):
                print(current_x- x)
                camino.append((current_x - x, current_y))
            current_x = destino_x 
            

        return camino


    def find_min_path(self, start_x, start_y):
        print(self.pick_locations)
        remaining_pick_locations = list(self.pick_locations)
        path = []
        
        for punt in remaining_pick_locations:
            cami = self.min_moves_to_point(start_x, start_y, punt[0], punt[1])
            start_x, start_y = punt[0], punt[1]
            path = path + cami
            
        return path
        
    def visualize_path(self, path):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pick_locations:
                    print('P', end=' ')  # Highlight picking locations
                elif (x, y) in self.obstacles:
                    print('#', end=' ')  # Obstacle
                elif (x, y) in path:
                    print('*', end=' ')  # Path
                else:
                    print('.', end=' ')  # Free space
            print()
        print('final', path)
        visualitza(self.magatzem, path, self.pick_locations_id)

"""# Example usage:
warehouse = Warehouse(5, 5)
warehouse.add_pick_location(1, 2)
warehouse.add_pick_location(3, 4)
warehouse.set_obstacle(2, 2)
warehouse.set_one_way_aisle(2, 3, 'down')

start_x, start_y = 0, 0
path = warehouse.find_path(start_x, start_y)
warehouse.visualize_path(path)"""