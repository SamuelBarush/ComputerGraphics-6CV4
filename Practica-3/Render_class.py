import sdl2.ext
import numpy as np
from Vector_class import Vector
from Bresenham_class import Bresenham

class Render:
    @staticmethod
    def render(faces, vertices, renderer):
        for face in faces:
            for i in range(len(face)):
                v1_index = face[i]
                v2_index = face[(i+1)%len(face)]
                v1 = vertices[v1_index]
                v2 = vertices[v2_index]
                Bresenham.draw_line(v1[0], v1[1], v2[0], v2[1], renderer, sdl2.ext.Color(255, 255, 255))
    
    def draw_circle(center, radius, color, renderer):
        x_center = center[0]
        y_center = center[1]
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                if x**2 + y**2 <= radius**2:
                    renderer.draw_point((x_center + x, y_center + y), color)

    def draw_ellipse(center, rx, ry, color, rendered):
        x_center = center[0]
        y_center = center[1]
        for x in range(-rx, rx + 1):
            for y in range(-ry, ry + 1):
                if (x/rx)**2 + (y/ry)**2 <= 1:
                    rendered.draw_point((x_center + x, y_center + y), color)

    def draw_vertices(vertices, renderer):
        for v in vertices:
            #renderer.draw_point((v[0], v[1]), sdl2.ext.Color(255, 255, 255))
            Render.draw_circle((v[0], v[1]), 2, sdl2.ext.Color(255, 0, 0), renderer)

    def draw_point(point, color, renderer):
        renderer.draw_point(point, color)
    
    def draw_line(x1, y1, x2, y2, renderer, color):
        Bresenham.draw_line(x1, y1, x2, y2, renderer, color)


    def backface_culling(v0, v1, v2):
        # Calcular el vector normal
        vA = Vector.convert2d_to_3d(v0)
        vB = Vector.convert2d_to_3d(v1)
        vC = Vector.convert2d_to_3d(v2)
        vAB = vB - vA
        vAC = vC - vA
        n = np.cross(vAB, vAC)

        # Calcular el vector de la cámara entre el punto del triangulo y la cámara
        camera = np.array([0, 0, 5])
        cameraRay = vA - camera

        # Calcular el producto punto
        dot_product = np.dot(n, cameraRay)

        return dot_product <= 0


    def FillFlatBottomTriangle(v1, v2, v3, color, renderer):
        x0, y0 = v1
        x1, y1 = v2
        x2, y2 = v3

        # Evitar división por cero
        dx1 = x1 - x0
        dx2 = x2 - x0
        dy = y1 - y0  # Asumimos que y2 == y1

        if dx1 == 0:
            m1 = float('inf')  # Pendiente infinita (línea vertical)
        else:
            m1 = dy / dx1

        if dx2 == 0:
            m2 = float('inf')
        else:
            m2 = dy / dx2

        for i in range(dy + 1):  # Aseguramos que se dibujen todos los puntos
            y = y0 + i
            x_start = x0 + i / m1 if m1 != float('inf') else x0
            x_end = x0 + i / m2 if m2 != float('inf') else x0
            Bresenham.draw_line(int(x_start), int(y), int(x_end), int(y), renderer, color)


    def FillFlatTopTriangle(v1, v2, v3, color, renderer):
        x0, y0 = v1
        x1, y1 = v2
        x2, y2 = v3

        # Evitar división por cero
        dx1 = x2 - x0
        dx2 = x2 - x1
        dy = y2 - y0  # Asumimos que y0 == y1

        if dx1 == 0:
            m1 = float('inf')
        else:
            m1 = dy / dx1

        if dx2 == 0:
            m2 = float('inf')
        else:
            m2 = dy / dx2

        for i in range(dy + 1):
            y = y2 - i
            x_start = x2 - i / m1 if m1 != float('inf') else x2
            x_end = x2 - i / m2 if m2 != float('inf') else x2
            Bresenham.draw_line(int(x_start), int(y), int(x_end), int(y), renderer, color)


    def DrawFilledTriangle(faces, vertices, renderer):
        for face in faces:
            v1_index, v2_index, v3_index = face[:3]
            v0 = vertices[v1_index]
            v1 = vertices[v2_index]
            v2 = vertices[v3_index]


            if not Render.backface_culling(v0, v1, v2):
                continue

            # Ordenar los vértices por coordenada Y
            vertices_sorted = sorted([v0, v1, v2], key=lambda v: v[1])
            v0, v1, v2 = vertices_sorted

            if v1[1] == v2[1]:  # Triángulo con base plana inferior
                Render.FillFlatBottomTriangle(v0, v1, v2, sdl2.ext.Color(255, 0, 0), renderer)
            elif v0[1] == v1[1]:  # Triángulo con base plana superior
                Render.FillFlatTopTriangle(v0, v1, v2, sdl2.ext.Color(0, 255, 0), renderer)
            else:  # Triángulo general
                # Dividir en dos triángulos
                mx = v0[0] + (v1[1] - v0[1]) * (v2[0] - v0[0]) / (v2[1] - v0[1])
                my = v1[1]
                v_split = (mx, my)

                Render.FillFlatBottomTriangle(v0, v1, v_split, sdl2.ext.Color(255, 0, 0), renderer)
                Render.FillFlatTopTriangle(v_split, v1, v2, sdl2.ext.Color(0, 255, 0), renderer)
