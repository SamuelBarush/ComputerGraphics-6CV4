import pygame

BLACK = (0, 0, 0)

class LineDrawing:
    def __init__(self, screen, cell_size, screen_width, screen_height):
        self.screen = screen
        self.cell_size = cell_size  # Tamaño de la celda
        self.origin_x = screen_width // 2  # Nuevo origen X (centro de la pantalla)
        self.origin_y = screen_height // 2 # Nuevo origen Y (centro de la pantalla)

    def draw_pixel(self, x, y, color):
        """Dibuja un 'píxel' rellenando la celda correspondiente, ajustando con el nuevo origen."""
        # Ajustar las coordenadas con respecto al centro de la pantalla
        x = self.origin_x + (x * self.cell_size)
        y = self.origin_y - (y * self.cell_size)  # Restar porque la Y aumenta hacia abajo en Pygame
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, rect)

    def dda(self, x1, y1, x2, y2,color=BLACK):
        """Algoritmo DDA para trazar una línea desde (x1, y1) hasta (x2, y2)."""
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        # Incremento por cada paso
        x_inc = dx / steps
        y_inc = dy / steps

        x, y = x1, y1
        for i in range(steps + 1):
            self.draw_pixel(round(x), round(y), color)
            x += x_inc
            y += y_inc

    def bresenham(self, x1, y1, x2, y2,color=BLACK):
        """Algoritmo Bresenham para trazar una línea desde (x1, y1) hasta (x2, y2)."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.draw_pixel(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
