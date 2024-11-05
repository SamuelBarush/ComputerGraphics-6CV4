import math
import sdl2.ext
from bresenham import Bresenham

class Renderer3D:
    def __init__(self, renderer, width, height, fov, distance):
        self.renderer = renderer
        self.width = width
        self.height = height
        self.fov = fov
        self.distance = distance

    def project_vertex(self, v):
        factor = self.fov / (self.distance + v[2])
        x_2d = int(v[0] * factor + self.width // 2)
        y_2d = int(-v[1] * factor + self.height // 2)
        return x_2d, y_2d

    def rotate_vertex(self, v, angle_x, angle_y, angle_z):
        x, y, z = v

        # Rotación en el eje X
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        y_new = y * cos_x - z * sin_x
        z_new = y * sin_x + z * cos_x
        y, z = y_new, z_new

        # Rotación en el eje Y
        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        x_new = x * cos_y + z * sin_y
        z_new = -x * sin_y + z * cos_y
        x, z = x_new, z_new

        # Rotación en el eje Z
        cos_z = math.cos(angle_z)
        sin_z = math.sin(angle_z)
        x_new = x * cos_z - y * sin_z
        y_new = x * sin_z + y * cos_z
        x, y = x_new, y_new

        return [x, y, z]
    
    def render_triangle(self,v1,v2,v3):
        if v1[1] > v2[1]:
            v1, v2 = v2, v1  # Intercambiar v1 y v2
        if v1[1] > v3[1]:
            v1, v3 = v3, v1  # Intercambiar v1 y v3
        if v2[1] > v3[1]:
            v2, v3 = v3, v2  # Intercambiar v2 y v3

        if v2[1] != v1[1]:
            for y in range(v1[1],v2[1]):
                x_start = self.interpolateX(v1,v2,y)
                x_end = self.interpolateX(v1,v3,y)
                self.drawScanLine(y,x_start,x_end)
        if v3[1] != v2[1]:
            for y in range(v2[1],v3[1]):
                x_start = self.interpolateX(v2,v3,y)
                x_end = self.interpolateX(v1,v3,y)
                self.drawScanLine(y,x_start,x_end)

    def interpolateX(self,v_start,v_end,y):
        dy  = v_end[1] - v_start[1]
        dx = v_end[0] - v_start[0]
        return v_start[0] + dx * ((y - v_start[1]) / dy)
    
    def drawScanLine(self,y,x_start,x_end):
        for x in range (int(x_start),int(x_end)):
            self.renderer.draw_point((x, y), sdl2.ext.Color(255, 255, 0))

    def fill_obj(self, vertices, faces, angle_x, angle_y, angle_z):
        # Rota y proyecta los vértices
        transformed_vertices = [self.rotate_vertex(v, angle_x, angle_y, angle_z) for v in vertices]
        projected_vertices = [self.project_vertex(v) for v in transformed_vertices]

        # Dibuja las caras visibles
        for face in faces:
            v1 = projected_vertices[face[0]]
            v2 = projected_vertices[face[1]]
            v3 = projected_vertices[face[2]]
            self.render_triangle(v1, v2, v3)

    def draw_circle(self, center, radius, color):
        x_center, y_center = center
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                if x * x + y * y <= radius * radius:  # Verifica si el punto está dentro del círculo
                    self.renderer.draw_point((x_center + x, y_center + y), color)

    def draw_vertices(self, vertices, angle_x, angle_y, angle_z):
        transformed_vertices = [self.rotate_vertex(v, angle_x, angle_y, angle_z) for v in vertices]
        projected_vertices = [self.project_vertex(v) for v in transformed_vertices]

        radius = 5  # Tamaño del círculo que representa el vértice
        for v in projected_vertices:
            self.draw_circle((v[0], v[1]), radius, sdl2.ext.Color(255, 0, 0))  # Dibuja un círculo rojo alrededor del vértice

    def render_obj(self, vertices, faces, angle_x, angle_y, angle_z):
        # Rota y proyecta los vértices
        transformed_vertices = [self.rotate_vertex(v, angle_x, angle_y, angle_z) for v in vertices]
        projected_vertices = [self.project_vertex(v) for v in transformed_vertices]

        # Dibuja las caras visibles
        for face in faces:
            for i in range(3):
                v1 = projected_vertices[face[i]]
                v2 = projected_vertices[face[(i + 1) % 3]]
                Bresenham.draw_line(v1[0], v1[1], v2[0], v2[1], self.renderer, sdl2.ext.Color(255, 255, 255))