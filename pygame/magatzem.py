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
        
    def add_pick_location_id(self, pos, product_id):
        self.pick_locations_id.append(((pos, product_id)))

    def set_obstacle(self, x, y):
        self.obstacles.add((x, y))


    def set_one_way_aisle(self, x, y, direction):
        self.one_way_aisles[(x, y)] = direction

    def heuristic(self, x, y, path):
        # Calcula la distancia acumulada desde el punto de inicio hasta el punto actual en el camino
        return len(path)

    def a_star(self, start_x, start_y, end_x, end_y, path):
        pq = [(0, 0, start_x, start_y, [])]  # Priority queue (f-score, g-score, x, y, path)
        visited = []

        while pq:
            f, g, x, y, path = heapq.heappop(pq)

            if (x, y) == (end_x, end_y):
                return path + [(x, y)]

            visited.append((x, y))

            
            
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in self.obstacles and (nx, ny) not in visited:
                        new_path = path + [(x, y)]
                        new_g = g + 1  # Se incrementa en 1 la distancia recorrida
                        h = self.heuristic(nx, ny, new_path)  # Usa la distancia acumulada como heurística
                        f = new_g + h
                        heapq.heappush(pq, (f, new_g, nx, ny, new_path))
                            
            """else:
                
                for dx, dy in [(1, 0), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if (nx, ny) not in self.obstacles and (nx, ny) not in visited:
                            new_path = path + [(x, y)]
                            new_g = g + 1  # Se incrementa en 1 la distancia recorrida
                            h = self.heuristic(nx, ny, new_path)  # Usa la distancia acumulada como heurística
                            f = new_g + h
                            heapq.heappush(pq, (f, new_g, nx, ny, new_path))"""
                        

        return None  # No path found
        
    """def a_star(self, start_x, start_y, end_x, end_y, path):
        pq = [(0, 0, start_x, start_y, [])]  # Priority queue (f-score, g-score, x, y, path)
        visited = []

        while pq:
            f, g, x, y, path = heapq.heappop(pq)

            if (x, y) == (end_x, end_y):
                return path + [(x, y)]

            visited.append((x, y))

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in self.obstacles and (nx, ny) not in visited:
                        new_path = path + [(x, y)]
                        new_g = g + 1  # Se incrementa en 1 la distancia recorrida
                        h = self.heuristic(nx, ny, new_path)  # Usa la distancia acumulada como heurística
                        f = new_g + h
                        heapq.heappush(pq, (f, new_g, nx, ny, new_path))

        return None  # No path found"""


    def find_path(self, start_x, start_y):
        remaining_pick_locations = list(self.pick_locations)
        path = []
        current_x, current_y = start_x, start_y
        while remaining_pick_locations:
            min_distance = float('inf')
            closest_location = None
            for location in remaining_pick_locations:
                distance = abs(location[0] - current_x) + abs(location[1] - current_y)
                if distance < min_distance:
                    min_distance = distance
                    closest_location = location
            next_x, next_y = closest_location
            next_path = self.a_star(current_x, current_y, next_x, next_y, [])
            if next_path is not None:
                if not path:
                    path = next_path
                else:
                    path += next_path[1:]
                current_x, current_y = next_x, next_y
                remaining_pick_locations.remove((next_x, next_y))
            else:
                print("No se encontró un camino desde ({}, {}) hasta ({}, {})".format(current_x, current_y, next_x, next_y))
                break

            # Llegamos a un punto de recogida, verificamos si estamos en la misma columna
            if (current_x, current_y) in self.pick_locations:
                columnes = [element[1] for element in remaining_pick_locations]
                if current_x not in columnes:
                    if current_x != 0 and current_x != self.width - 1:
                        closest_column = 0 if current_x <= self.width / 2 else self.width - 1
                        next_column_path = self.a_star(current_x, current_y, closest_column, current_y, [])
                        if next_column_path is not None:
                            path += next_column_path[1:]
                            current_x, current_y = closest_column, current_y
                        else:
                            print("No se encontró un camino hacia la columna {}".format(closest_column))
                            break
            
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