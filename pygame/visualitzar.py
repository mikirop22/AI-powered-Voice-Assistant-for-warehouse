import pygame
import random

# Dimensiones de la ventana y de cada celda
ANCHO = 1400
ALTO = 700
CELDA_ANCHO = ANCHO // 7
CELDA_ALTO = ALTO // 7

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Cargar la imagen "estanteria.jpg"
imagen_estanteria = pygame.image.load("pygame/estanteria.jpg")
# Escalar la imagen al tamaño de la celda
imagen_estanteria = pygame.transform.scale(imagen_estanteria, (CELDA_ANCHO, int(CELDA_ALTO / 3)))

# Cargar la imagen del suelo
imagen_suelo = pygame.image.load("pygame/terra.jpg")
# Escalar la imagen al tamaño de la celda
imagen_suelo = pygame.transform.scale(imagen_suelo, (CELDA_ANCHO, int(CELDA_ALTO / 3)))

# Función para generar un número aleatorio de identificación
def generar_id():
    return random.randint(1, 10)

# Crear la matriz 5x5 con listas dentro de cada celda
matriz = [[ [generar_id(), None, generar_id()] for _ in range(5)] for _ in range(5)]
for fila in matriz:
    fila.append([None, None, None])

for fila in matriz:
    fila.insert(0, [None, None, None])

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Representación de Matriz")

# Bucle principal
ejecutando = True
camino = []  # Lista para almacenar las posiciones visitadas por el círculo
posiciones_destino = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]  # Lista de posiciones que el círculo debe visitar
indice_destino = 0  # Índice actual en la lista de posiciones de destino
posicion_actual = posiciones_destino[indice_destino]  # Coordenadas actuales del círculo
ultima_posicion = False  # Bandera para indicar si el círculo llegó a la última posición
while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False

    # Dibujar la matriz y el camino
    ventana.fill(BLANCO)
    for i in range(5):
        for j in range(5+2):
            celda = matriz[i][j]
            for k, elemento in enumerate(celda):
                ventana.blit(imagen_suelo, (j * CELDA_ANCHO, i * CELDA_ALTO + k * (CELDA_ALTO / 3)))
                if elemento is not None:
                    # Dibujar la imagen de la estantería como fondo
                    ventana.blit(imagen_estanteria, (j * CELDA_ANCHO, i * CELDA_ALTO + k * (CELDA_ALTO / 3)))

                # Lista de IDs para los cuales queremos dibujar círculos azules
                ids_a_dibujar_azul = [2, 4, 7]
                # Dibujar el círculo azul cuando el elemento esté en la lista de IDs
                if elemento in ids_a_dibujar_azul:
                    pygame.draw.circle(ventana, AZUL, (j * CELDA_ANCHO + CELDA_ANCHO // 2, i * CELDA_ALTO + k * (CELDA_ALTO // 3) + CELDA_ALTO // 6), 10)

    # Dibujar el camino
    for pos in camino:
        pygame.draw.rect(ventana, ROJO, (pos[0] * CELDA_ANCHO + CELDA_ANCHO // 2 - 5, pos[1] * CELDA_ALTO + CELDA_ALTO // 2 - 5, 10, 10))

    # Calcular el movimiento gradual del círculo si no ha llegado a la última posición
    if not ultima_posicion:
        x_actual, y_actual = posicion_actual
        x_destino, y_destino = posiciones_destino[indice_destino]
        dx = (x_destino - x_actual) * CELDA_ANCHO // 20
        dy = (y_destino - y_actual) * CELDA_ALTO // 20

        # Dibujar el círculo en la posición actual
        pygame.draw.circle(ventana, NEGRO, (x_actual * CELDA_ANCHO + CELDA_ANCHO // 2, y_actual * CELDA_ALTO + CELDA_ALTO // 2), 20)

        # Actualizar la posición actual del círculo
        if x_actual != x_destino or y_actual != y_destino:
            posicion_actual = (x_actual + dx // CELDA_ANCHO, y_actual + dy // CELDA_ALTO)
            if posicion_actual not in camino:
                camino.append(posicion_actual)
        else:
            if indice_destino == len(posiciones_destino) - 1:
                ultima_posicion = True
            else:
                indice_destino = (indice_destino + 1) % len(posiciones_destino)
                posicion_actual = posiciones_destino[indice_destino]
                if posicion_actual not in camino:
                    camino.append(posicion_actual)

    pygame.display.flip()
    pygame.time.delay(100)  # Ajustar el retraso para hacer el movimiento más lento

pygame.quit()
