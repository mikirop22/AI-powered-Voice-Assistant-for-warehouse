import pygame



pygame.init()

width = 1525
height = 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mi Juego")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()
