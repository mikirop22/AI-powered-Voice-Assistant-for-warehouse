import pygame
from pygame.locals import *

def visualitza(magatzem, camino, pick_locations, nom_quantitas_pos):
    
    visitadas = set()  # Utilizamos un conjunto para un acceso más eficiente
    ids_a_dibujar = [ids[1] for ids in pick_locations]
    pick_locations = [loc[0] for loc in pick_locations]
    # Dimensiones de la ventana y de cada celda
    ANCHO = 1400
    ALTO = 600
    CELDA_ANCHO = 80
    CELDA_ALTO = 60

    # Colores
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    ROJO = (255, 0, 0)
    VERDE = (0, 255, 0)
    AZUL = (0, 0, 255)

    # Cargar la imagen "estanteria.jpg"
    imagen_estanteria = pygame.image.load("treballador/pygame/imatges/estanteria.jpg")
    # Escalar la imagen al tamaño de la celda
    imagen_estanteria = pygame.transform.scale(imagen_estanteria, (CELDA_ANCHO, int(CELDA_ALTO / 3)))

    # Cargar la imagen del suelo
    imagen_suelo = pygame.image.load("treballador/pygame/imatges/terra.jpg")
    # Escalar la imagen al tamaño de la celda
    imagen_suelo = pygame.transform.scale(imagen_suelo, (CELDA_ANCHO, int(CELDA_ALTO / 3)))

    # Cargar la imagen "llibreta.png"
    imagen_llibreta = pygame.image.load("treballador/pygame/imatges/llibreta.png")
    # Escalar la imagen al tamaño deseado
    imagen_llibreta = pygame.transform.scale(imagen_llibreta, (450, 600))

    # Inicializar Pygame
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Magatzem")

    # Fuente para el texto
    fuente = pygame.font.SysFont(None, 24)

    ejecutando = True
    posiciones_destino = camino  # Usar el camino como posiciones destino
    indice_destino = 0  
    posicion_actual = posiciones_destino[indice_destino]  
    ultima_posicion = False  
    pausa = False

    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pausa = not pausa

        # Dibujar la matriz y el camino
        ventana.fill(BLANCO)
        for i in range(10):
            for j in range(10+2):
                celda = magatzem[i][j]
                for k, elemento in enumerate(celda):
                    ventana.blit(imagen_suelo, (j * CELDA_ANCHO, i * CELDA_ALTO + k * (CELDA_ALTO / 3)))
                    if elemento is not None:
                        ventana.blit(imagen_estanteria, (j * CELDA_ANCHO, i * CELDA_ALTO + k * (CELDA_ALTO / 3)))

        for i in range(10):
            for j in range(10+2):
                celda = magatzem[i][j]
                for k, elemento in enumerate(celda):
                    if elemento in ids_a_dibujar:
                        pygame.draw.circle(ventana, AZUL, ((i+1) * CELDA_ANCHO + (CELDA_ANCHO//2), j * CELDA_ALTO + k * (CELDA_ALTO // 3) + 10), 10)

        # Dibujar el camino
        for pos in camino:
            if (int(pos[0]), pos[1]) in visitadas:
                pygame.draw.rect(ventana, ROJO, (pos[0] * CELDA_ANCHO + CELDA_ANCHO // 2 - 5, pos[1] * CELDA_ALTO + CELDA_ALTO // 2 - 5, 10, 10))

        # Dibujar la imagen de la llibreta
        ventana.blit(imagen_llibreta, (ANCHO - imagen_llibreta.get_width(), 0))

        tamano_fuente = 30

        texto = fuente.render(str('PRODUCT'), True, NEGRO)
        ventana.blit(texto, (ANCHO - CELDA_ANCHO * 3.25, 70))
        texto = fuente.render(str('QUANT'), True, NEGRO)
        ventana.blit(texto, (ANCHO - CELDA_ANCHO * 1.25, 70))
       
        tamano_fuente = 20  # Ajusta este valor según lo pequeña que desees la letra
        # Cargar la fuente con el nuevo tamaño
        fuente = pygame.font.Font(None, tamano_fuente)

        for idx, id in enumerate(ids_a_dibujar):
            texto = fuente.render(str(nom_quantitas_pos[id][0]), False, NEGRO)
            ventana.blit(texto, (ANCHO - CELDA_ANCHO * 4, idx * 40 + 115))
            texto = fuente.render(str(nom_quantitas_pos[id][1]), False, NEGRO)
            ventana.blit(texto, (ANCHO - CELDA_ANCHO * 1, idx * 40 + 115))
            # Dibujar el perímetro de un cuadrado al lado del índice
            pygame.draw.rect(ventana, NEGRO, (ANCHO - CELDA_ANCHO * 4 - 32, idx * 40 + 112, 20, 20), 2)
            pos = nom_quantitas_pos[id][2]
            if (pos[0], pos[1]) in visitadas:
                pygame.draw.rect(ventana, VERDE, (ANCHO - CELDA_ANCHO * 4 - 30, idx * 40 + 114, 16, 16))

        if not pausa:  
            # Calcular el movimiento gradual del círculo si no ha llegado a la última posición
            if not ultima_posicion:
                x_actual, y_actual = posicion_actual
                x_destino, y_destino = posiciones_destino[indice_destino]
                dx = (x_destino - x_actual) * CELDA_ANCHO // 40  # Movimiento más lento
                dy = (y_destino - y_actual) * CELDA_ALTO // 40  # Movimiento más lento

                pygame.draw.circle(ventana, NEGRO, (x_actual * CELDA_ANCHO + CELDA_ANCHO // 2, y_actual * CELDA_ALTO + CELDA_ALTO // 2), 20)
                visitadas.add((x_actual, y_actual))  # Marcar la celda como visitada
                
                if (x_actual, y_actual) in pick_locations:
                    pygame.event.wait()
                
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
        pygame.time.delay(500)  # Reducción del retraso para un movimiento más lento

    pygame.quit()
