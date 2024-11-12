import sdl2.ext
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

    def Render_Triangle(faces, vertices, renderer):
        for face in faces:
            # Obtener los índices de los vértices de la cara
            v1_index, v2_index, v3_index = face[:3]
            v1 = vertices[v1_index]
            v2 = vertices[v2_index]
            v3 = vertices[v3_index]

            # Definir colores para cada vértice
            color1 = sdl2.ext.Color(255, 0, 0)  # Rojo
            color2 = sdl2.ext.Color(0, 255, 0)  # Verde
            color3 = sdl2.ext.Color(0, 0, 255)  # Azul

            # Obtener las coordenadas del triángulo
            triangle = [v1, v2, v3]

            # Calcular el rectángulo que encierra el triángulo
            min_x = int(min(v1[0], v2[0], v3[0]))
            max_x = int(max(v1[0], v2[0], v3[0]))
            min_y = int(min(v1[1], v2[1], v3[1]))
            max_y = int(max(v1[1], v2[1], v3[1]))

            # Iterar sobre el área del rectángulo que encierra el triángulo
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    # Comprobar si el punto (x, y) está dentro del triángulo
                    if Render.point_in_triangle(x, y, triangle):
                        # Calcular los colores interpolados
                        color = Render.interpolate_color(x, y, v1, v2, v3, color1, color2, color3)
                        #renderer.draw_point((x, y), sdl2.ext.Color(255, 255, 0))
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

