import pygame

BLACK = (0, 0, 0)

class Line:
    def __init__(self, screen, cell_size):
        self.screen = screen
        self.cell_size = cell_size

    def draw_pixel(self, x, y, color=BLACK):
        """Dibuja un 'píxel' en la posición dada escalada por el tamaño de la celda."""
        pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def dda(self, x1, y1, x2, y2):
        """Algoritmo DDA para trazar una línea desde (x1, y1) hasta (x2, y2)."""
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        # Incremento por cada paso
        x_inc = dx / steps
        y_inc = dy / steps

        x, y = x1, y1
        for i in range(steps + 1):
            self.draw_pixel(round(x), round(y), BLACK)
            x += x_inc
            y += y_inc

    def bresenham(self, x1, y1, x2, y2):
        """Algoritmo Bresenham para trazar una línea desde (x1, y1) hasta (x2, y2)."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.draw_pixel(x1, y1, BLACK)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy