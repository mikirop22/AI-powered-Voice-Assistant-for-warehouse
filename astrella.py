import heapq
import math

class Nodo:
    def __init__(self, x, y, padre=None, g=0, h=0):
        self.x = x
        self.y = y
        self.padre = padre
        self.g = g  # Costo acumulado desde el nodo inicial hasta este nodo
        self.h = h  # Heurística (estimación del costo del nodo a la meta)

    def f(self):
        return self.g + self.h

def a_estrella(inicio, objetivo, matriz, ):
    def heuristica(a, b):
        # Heurística de distancia Euclidiana
        return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

    def vecinos(nodo):
        # Obtener vecinos válidos de un nodo en la matriz
        vecinos = []

        # Mover hacia abajo
        if nodo.x + 1 < len(matriz) and matriz[nodo.x + 1][nodo.y] != 1:
            vecinos.append(Nodo(nodo.x + 1, nodo.y))

        # Mover hacia arriba si está en la primera columna
        if nodo.y == 0 and nodo.x - 1 >= 0 and matriz[nodo.x - 1][nodo.y] != 1:
            vecinos.append(Nodo(nodo.x - 1, nodo.y))

        # Mover hacia abajo si está en la última columna
        if nodo.y == len(matriz[0]) - 1 and nodo.x + 1 < len(matriz) and matriz[nodo.x + 1][nodo.y] != 1:
            vecinos.append(Nodo(nodo.x + 1, nodo.y))

        return vecinos


    abierto = []
    cerrado = set()
    heapq.heappush(abierto, (inicio.f(), inicio))

    while abierto:
        _, nodo_actual = heapq.heappop(abierto)

        if (nodo_actual.x, nodo_actual.y) == objetivo:
            # Reconstruir el camino desde el nodo objetivo hasta el nodo inicial
            camino = []
            while nodo_actual:
                camino.append((nodo_actual.x, nodo_actual.y))
                nodo_actual = nodo_actual.padre
            return camino[::-1]

        cerrado.add((nodo_actual.x, nodo_actual.y))

        for vecino in vecinos(nodo_actual):
            if (vecino.x, vecino.y) in cerrado:
                continue

            g = nodo_actual.g + 1  # Costo de moverse a un vecino
            h = heuristica(vecino, Nodo(objetivo[0], objetivo[1]))
            nuevo_nodo = Nodo(vecino.x, vecino.y, nodo_actual, g, h)

            heapq.heappush(abierto, (nuevo_nodo.f(), nuevo_nodo))

    return None

# Ejemplo de uso
matriz = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

inicio = Nodo(0, 0)
objetivo = (4, 4)

camino = a_estrella(inicio, objetivo, matriz)

if camino:
    print("Camino encontrado:", camino)
else:
    print("No se encontró un camino.")
