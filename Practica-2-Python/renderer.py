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
    
    def sort_vertices(self, vertices):
        return sorted(vertices,key=lambda v: v[1])
    
    def split_triangle(self, v0, v1, v2):
        v0,v1 ,v2 = self.sort_vertices([v0,v1,v2])
        print("Vertices ordenados:",v0,v1,v2)

        if v1[0] == v2[0]:
            self.fill_flat_top(v0,v1,v2)
        elif v0[0] == v1[0]:
            self.fill_flat_bottom(v0,v1,v2)
        else:
            vy_middle = v1[1]
            vx_middle = v0[0] + ((v2[0] - v0[0]) * (v1[1] - v0[1]) / (v2[1] - v0[1]))
            v_middle = (vx_middle, vy_middle)
            self.fill_flat_bottom(v0, v1, v_middle)
            self.fill_flat_top(v1, v_middle, v2)
    
    def fill_flat_bottom(self, v0, v1, v2):
        # Asegúrate de que v0, v1, y v2 son tuples de longitud 3
        m1 = (v1[0] - v0[0]) / (v1[1] - v0[1]) if v1[1] != v0[1] else 0
        m2 = (v2[0] - v0[0]) / (v2[1] - v0[1]) if v2[1] != v0[1] else 0

        x_start = v0[0]
        x_end = v0[0]

        # Asegúrate de que el rango está correcto
        for y in range(int(v0[1]), int(v2[1]) + 1):  # Usa +1 para incluir v2[1]
            Bresenham.draw_line(int(x_start), y, int(x_end), y, self.renderer, sdl2.ext.Color(255, 0, 0))
            x_start += m1
            x_end += m2


    def fill_flat_top(self, v0, v1, v2):
        m1 = (v2[0] - v0[0]) / (v2[1] - v0[1]) if v2[1] != v0[1] else 0
        m2 = (v2[0] - v1[0]) / (v1[1] - v0[1]) if v1[1] != v0[1] else 0

        x_start = v2[0]
        x_end = v2[0]

        # Asegúrate de que el rango está correcto
        for y in range(int(v2[1]), int(v0[1]) + 1):  # Usa +1 para incluir v0[1]
            Bresenham.draw_line(int(x_start), y, int(x_end), y, self.renderer, sdl2.ext.Color(0, 255, 0))
            x_start += m1
            x_end += m2

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

    def fill_obj (self, vertices, faces, angle_x, angle_y, angle_z):
        # Rota y proyecta los vértices
        transformed_vertices = [self.rotate_vertex(v, angle_x, angle_y, angle_z) for v in vertices]
        projected_vertices = [self.project_vertex(v) for v in transformed_vertices]

        # Dibuja las caras visibles
        for face in faces:

            # Obtiene los vértices de la cara
            v0 = projected_vertices[face[0]]
            v1 = projected_vertices[face[1]]
            v2 = projected_vertices[face[2]]

            self.split_triangle(v0,v1,v2)