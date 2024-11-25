import sdl2.ext
import numpy as np
from Bresenham_class import Bresenham

class Render:
    @staticmethod
    def render(faces,vertices,renderer):
        for face in faces:
            for i  in range(len(face)):
                v1_index = face[i]
                v2_index = face[(i+1)%len(face)]
                v1 = vertices[v1_index]
                v2 = vertices[v2_index]
                Bresenham.draw_line(v1[0], v1[1], v2[0], v2[1], renderer, sdl2.ext.Color(255, 255, 255))
    
    def draw_circle(center,radius,color,renderer):
        x_center = center[0]
        y_center = center[1]
        for x in range(-radius,radius + 1):
            for y in range(-radius,radius + 1):
                if x**2 + y**2 <= radius**2:
                    renderer.draw_point((x_center + x, y_center + y), color)

    def draw_ellipse(center,rx,ry,color,rendered):
        x_center = center[0]
        y_center = center[1]
        for x in range(-rx,rx + 1):
            for y in range(-ry,ry + 1):
                if (x/rx)**2 + (y/ry)**2 <= 1:
                    rendered.draw_point((x_center + x, y_center + y), color)

    def draw_vertices(vertices,renderer):
        for v in vertices:
            #renderer.draw_point((v[0], v[1]), sdl2.ext.Color(255, 255, 255))
            Render.draw_circle((v[0], v[1]), 2, sdl2.ext.Color(255, 0, 0), renderer)

    def draw_point(point,color,renderer):
        renderer.draw_point(point, color)
    
    def draw_line(x1, y1, x2, y2, renderer, color):
        Bresenham.draw_line(x1, y1, x2, y2, renderer, color)

    def Render_Triangle(faces, vertices, renderer, camera_position):
        for face in faces:
            v1_index, v2_index, v3_index = face[:3]
            v1 = vertices[v1_index]
            v2 = vertices[v2_index]
            v3 = vertices[v3_index]

            # Extender los vértices 2D a 3D para los cálculos
            v1_3d = np.array([v1[0], v1[1], 0.0])
            v2_3d = np.array([v2[0], v2[1], 0.0])
            v3_3d = np.array([v3[0], v3[1], 0.0])

            # Calcular la normal de la cara en 3D
            edge1 = v2_3d - v1_3d
            edge2 = v3_3d - v1_3d
            normal = np.cross(edge1, edge2)

            # La dirección hacia la cámara debe estar en 3D
            direction_to_camera = camera_position - v1_3d

            # Producto punto entre la normal de la cara y la dirección hacia la cámara
            dot_product = np.dot(normal, direction_to_camera)

            # Si el producto punto es negativo, la cara está orientada hacia la cámara y debe ser renderizada
            if dot_product < 0:
                color1 = sdl2.ext.Color(255, 0, 0)  # Rojo
                color2 = sdl2.ext.Color(0, 255, 0)  # Verde
                color3 = sdl2.ext.Color(0, 0, 255)  # Azul

                triangle = [v1, v2, v3]

                min_x = int(min(v1[0], v2[0], v3[0]))
                max_x = int(max(v1[0], v2[0], v3[0]))
                min_y = int(min(v1[1], v2[1], v3[1]))
                max_y = int(max(v1[1], v2[1], v3[1]))

                for x in range(min_x, max_x + 1):
                    for y in range(min_y, max_y + 1):
                        if Render.point_in_triangle(x, y, triangle):
                            color = Render.interpolate_color(x, y, v1, v2, v3, color1, color2, color3)
                            renderer.draw_point((x, y), color)

    def point_in_triangle(x, y, triangle):
        v1, v2, v3 = triangle

        # Usar el método de coordenadas baricéntricas para comprobar si el punto está dentro del triángulo
        denom = (v2[1] - v3[1]) * (v1[0] - v3[0]) + (v3[0] - v2[0]) * (v1[1] - v3[1])
        a = ((v2[1] - v3[1]) * (x - v3[0]) + (v3[0] - v2[0]) * (y - v3[1])) / denom
        b = ((v3[1] - v1[1]) * (x - v3[0]) + (v1[0] - v3[0]) * (y - v3[1])) / denom
        c = 1 - a - b
        return (a >= 0) and (b >= 0) and (c >= 0)

    def interpolate_color(x, y, v1, v2, v3, color1, color2, color3):
        # Calcular las coordenadas baricéntricas
        denom = (v2[1] - v3[1]) * (v1[0] - v3[0]) + (v3[0] - v2[0]) * (v1[1] - v3[1])
        a = ((v2[1] - v3[1]) * (x - v3[0]) + (v3[0] - v2[0]) * (y - v3[1])) / denom
        b = ((v3[1] - v1[1]) * (x - v3[0]) + (v1[0] - v3[0]) * (y - v3[1])) / denom

        # Interpolar el color
        r = int(color1.r * a + color2.r * b + color3.r * (1 - a - b))
        g = int(color1.g * a + color2.g * b + color3.g * (1 - a - b))
        b = int(color1.b * a + color2.b * b + color3.b * (1 - a - b))

        return sdl2.ext.Color(r, g, b)
    
    def is_right_triangle(v0, v1, v2):
        # Calcular los vectores entre los vértices
        vec0 = (v1[0] - v0[0], v1[1] - v0[1])
        vec1 = (v2[0] - v1[0], v2[1] - v1[1])
        vec2 = (v0[0] - v2[0], v0[1] - v2[1])

        # Calcular los productos escalares entre los vectores
        dot0 = vec0[0] * vec2[0] + vec0[1] * vec2[1]
        dot1 = vec0[0] * vec1[0] + vec0[1] * vec1[1]
        dot2 = vec1[0] * vec2[0] + vec1[1] * vec2[1]

        # Si alguno de los productos escalares es 0, es un triángulo rectángulo
        return dot0 == 0 or dot1 == 0 or dot2 == 0

    def FillRightTriangle(v0, v1, v2, color, rendered):
        # Calcular el área del triángulo
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        # Función para comprobar si un punto está dentro del triángulo
        def point_in_triangle(pt, v0, v1, v2):
            d1 = sign(pt, v0, v1)
            d2 = sign(pt, v1, v2)
            d3 = sign(pt, v2, v0)
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            return not (has_neg and has_pos)
        
        # Obtener el bounding box del triángulo para iterar sobre sus píxeles
        min_x = min(v0[0], v1[0], v2[0])
        max_x = max(v0[0], v1[0], v2[0])
        min_y = min(v0[1], v1[1], v2[1])
        max_y = max(v0[1], v1[1], v2[1])

        # Iterar sobre todos los píxeles en el bounding box y colorear los que estén dentro del triángulo
        for x in range(int(min_x), int(max_x) + 1):
            for y in range(int(min_y), int(max_y) + 1):
                if point_in_triangle((x, y), v0, v1, v2):
                    rendered.draw_point((x, y), color)


    def FillFlatBottomTriangle(v1, v2, v3, color, renderer):
        x0,y0 = v1
        x1,y1 = v2
        x2,y2 = v3

        m1 = - ((y1 - y0) / (x0 - x1))
        m2 = (y2 - y0) / (x2 - x0)

        for i in range( y1 - y0):
            Bresenham.draw_line(x0 + i/m1, y0 + i, x0 + i/m2, y0 + i, renderer, color)

    def FillFlatTopTriangle(v1, v2, v3, color, renderer):
        x0,y0 = v1
        x1,y1 = v2
        x2,y2 = v3

        m1 = -((y2 - y0) / (x2 - x0))
        m2 = -((y2 - y1) / (x2 - x1))

        for i in range( y2 - y1):
            Bresenham.draw_line(x2 + i/m1, y2 - i, x2 + i/m2, y2 - i, renderer, color)
    
    def DrawFilledTriangle(faces,vertices, rendered):
        for face in faces:
            v1_index, v2_index, v3_index = face[:3]
            v0 = vertices[v1_index]
            v1 = vertices[v2_index]
            v2 = vertices[v3_index]
             
            # Ordenar los vértices por su coordenada Y
            vertices_sorted = sorted([v0, v1, v2], key=lambda v: v[1])
            v0, v1, v2 = vertices_sorted


            if Render.is_right_triangle(v0, v1, v2):
                # Colorear el triángulo rectángulo con un color especial (por ejemplo, azul)
                Render.FillRightTriangle(v0, v1, v2, sdl2.ext.Color(0, 0, 255), rendered)
            elif v1[1] == v2[1]:
                Render.FillFlatBottomTriangle(v0,v1,v2,sdl2.ext.Color(255,0,0),rendered)
            elif v0[1] == v1[1]:
                Render.FillFlatTopTriangle(v0,v1,v2,sdl2.ext.Color(0,255,0),rendered)
            else:
            
                # Calcular Mx y My para dividir el triángulo en dos
                mx = (((v2[0] - v0[0])*(v1[1] - v0[1]))/(v2[1] - v0[1])) + v0[0]
                my = v1[1]

                # Dibujar el triángulo superior
                Render.FillFlatBottomTriangle(v0,(mx,my),v1,sdl2.ext.Color(255,0,0),rendered)
                # Dibujar el triángulo inferior
                Render.FillFlatTopTriangle(v0,v1,(mx,my),sdl2.ext.Color(0,255,0),rendered)
