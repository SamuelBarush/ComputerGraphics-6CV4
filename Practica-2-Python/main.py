import pygame
from LineDrawing_class import LineDrawing
from Line_class import Line

# Inicializar pygame
pygame.init()

# Definir dimensiones de la pantalla (ancho y alto)
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Plano Cartesiano con Cuadrícula de Píxeles")

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)  # Color gris para las celdas

# Tamaño del píxel de la cuadrícula
CELL_SIZE = 10  # Cambié el tamaño a 20 para mayor visibilidad

# Dibujar la cuadrícula
def draw_grid():
    for x in range(0, width, CELL_SIZE):
        for y in range(0, height, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)  # Dibujar borde de la celda

# Dibujar el plano cartesiano (ejes)
def draw_axes():
    # Eje Y (vertical en el centro de la pantalla)
    pygame.draw.line(screen, RED, (width // 2, 0), (width // 2, height), 2)
    # Eje X (horizontal en el centro de la pantalla)
    pygame.draw.line(screen, RED, (0, height // 2), (width, height // 2), 2)

line_drawing = LineDrawing(screen, CELL_SIZE, width, height)
#line = Line(screen)


x1, y1 = 0, 0
x2, y2 = -10, 20

x3, y3 = 0, 0
x4, y4 = 10, 20

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Llenar el fondo de blanco
    screen.fill(WHITE)

    # Dibujar la cuadrícula y los ejes
    draw_grid()
    draw_axes()

    line_drawing.bresenham(x1, y1, x2, y2,RED)
    #line.bresenham(x1, y1, x2, y2)
    line_drawing.dda(x3, y3, x4, y4,GREEN)
    #line.dda(x3, y3, x4, y4)

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de pygame
pygame.quit()
