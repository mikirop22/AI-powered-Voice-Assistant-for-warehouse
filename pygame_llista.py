import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir tamaño de la ventana
WIDTH, HEIGHT = 400, 300

# Crear ventana
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lista de Productos")

# Fuente para el texto
font = pygame.font.SysFont(None, 24)

# Lista de productos y sus cantidades
productos = {}
productos["Producto 1"] = 0
productos["Producto 2"] = 0

# Función para dibujar la lista de productos
def draw_product_list():
    y = 20
    for producto, cantidad in productos.items():
        text_surface = font.render(f"{producto}: {cantidad}", True, BLACK)
        window.blit(text_surface, (20, y))
        y += 30

# Bucle principal
while True:
    window.fill(WHITE)

    # Dibujar lista de productos
    draw_product_list()

    # Actualizar ventana
    pygame.display.flip()

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_a:  # Añadir producto
                # Aquí puedes implementar la lógica para añadir un producto y aumentar su cantidad
                pass
