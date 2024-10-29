import sys
import math
import sdl2
import sdl2.ext

# Parámetros de proyección
WIDTH, HEIGHT = 800, 600
FOV = 500  # Campo de visión para la proyección en perspectiva
DISTANCE = 5
FPS = 60  # Establece el límite de FPS deseado
FRAME_DELAY = 1000 // FPS  # Retraso entre fotogramas en milisegundos

# Tamaño de los puntos que representan las aristas y caras
POINT_SPACING = 0.1  # Distancia entre puntos en cada arista y dentro de las caras

# Función para proyectar un vértice 3D a 2D usando perspectiva
def project_vertex_perspective(v, width, height, fov, distance):
    factor = fov / (distance + v[2])
    x_2d = int(v[0] * factor + width // 2)
    y_2d = int(-v[1] * factor + height // 2)
    return x_2d, y_2d

# Función para proyectar un vértice 3D a 2D usando proyección ortogonal
def project_vertex_orthogonal(v, width, height, scale=100):
    x_2d = int(v[0] * scale + width // 2)
    y_2d = int(-v[1] * scale + height // 2)
    return x_2d, y_2d

# Genera puntos en una línea usando interpolación lineal
def generate_points_on_line(v1, v2, spacing=POINT_SPACING):
    points = []
    distance = math.sqrt(sum((v2[i] - v1[i]) ** 2 for i in range(3)))
    steps = int(distance / spacing)
    for i in range(steps + 1):
        t = i / steps
        point = [
            v1[j] * (1 - t) + v2[j] * t
            for j in range(3)
        ]
        points.append(point)
    return points

# Genera una cuadrícula de puntos dentro de una cara del cubo
def generate_points_in_face(v1, v2, v3, v4, spacing=POINT_SPACING):
    points = []
    # Interpolamos entre los bordes de la cara
    for i in range(int(1 / spacing) + 1):
        t = i * spacing
        p1 = [v1[j] * (1 - t) + v4[j] * t for j in range(3)]
        p2 = [v2[j] * (1 - t) + v3[j] * t for j in range(3)]
        points += generate_points_on_line(p1, p2, spacing)
    return points

# Aplica rotación en los ejes X, Y, Z
def rotate_vertex(v, angle_x, angle_y, angle_z):
    x, y, z = v
    # Rotación en el eje X
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    # Rotación en el eje Y
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
    # Rotación en el eje Z
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
    return [x, y, z]

# Crea los vértices y aristas de un cubo
def create_cube():
    vertices = [
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    # Caras del cubo (4 vértices cada una)
    faces = [
        (0, 1, 2, 3),  # Cara trasera
        (4, 5, 6, 7),  # Cara delantera
        (0, 1, 5, 4),  # Cara inferior
        (2, 3, 7, 6),  # Cara superior
        (0, 3, 7, 4),  # Cara izquierda
        (1, 2, 6, 5)   # Cara derecha
    ]
    return vertices, edges, faces

# Renderiza el cubo con aristas y puntos en las caras
def render_cube(renderer, vertices, edges, faces, angle_x, angle_y, angle_z, perspective=True):
    rotated_vertices = [rotate_vertex(v, angle_x, angle_y, angle_z) for v in vertices]
    
    if perspective:
        projected_vertices = [project_vertex_perspective(v, WIDTH, HEIGHT, FOV, DISTANCE) for v in rotated_vertices]
    else:
        projected_vertices = [project_vertex_orthogonal(v, WIDTH, HEIGHT) for v in rotated_vertices]

    # Renderiza las aristas
    for edge in edges:
        v1, v2 = rotated_vertices[edge[0]], rotated_vertices[edge[1]]
        edge_points = generate_points_on_line(v1, v2)
        for point in edge_points:
            if perspective:
                x, y = project_vertex_perspective(point, WIDTH, HEIGHT, FOV, DISTANCE)
            else:
                x, y = project_vertex_orthogonal(point, WIDTH, HEIGHT)
            renderer.draw_point((x, y), sdl2.ext.Color(255, 255, 255))

    # Renderiza los puntos en el interior de las caras
    for face in faces:
        v1, v2, v3, v4 = [rotated_vertices[i] for i in face]
        face_points = generate_points_in_face(v1, v2, v3, v4)
        for point in face_points:
            if perspective:
                x, y = project_vertex_perspective(point, WIDTH, HEIGHT, FOV, DISTANCE)
            else:
                x, y = project_vertex_orthogonal(point, WIDTH, HEIGHT)
            renderer.draw_point((x, y), sdl2.ext.Color(255, 255, 255))

# Ejecuta el programa
def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("3D Cube with Points on Faces and Edges", size=(WIDTH, HEIGHT))
    window.show()

    renderer = sdl2.ext.Renderer(window)
    running = True

    # Crea el cubo, aristas y caras
    vertices, edges, faces = create_cube()

    # Ángulos de rotación
    angle_x, angle_y, angle_z = 0, 0, 0

    while running:
        start_time = sdl2.SDL_GetTicks()  # Obtiene el tiempo de inicio del frame

        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

        # Limpia la pantalla
        renderer.clear(sdl2.ext.Color(0, 0, 0))

        # Actualiza ángulos para la vista perspectiva
        angle_x += 0.01
        angle_y += 0.01
        angle_z += 0.01

        # Renderiza el cubo en vista perspectiva (rotando)
        render_cube(renderer, vertices, edges, faces, angle_x, angle_y, angle_z, perspective=True)

        # Renderiza el cubo en vista ortogonal (fija)
        render_cube(renderer, vertices, edges, faces, math.pi / 6, math.pi / 6, 0, perspective=False)

        # Actualiza la pantalla
        renderer.present()

        # Control de FPS: Calcula el tiempo que tomó el frame y ajusta el retraso
        frame_time = sdl2.SDL_GetTicks() - start_time
        if frame_time < FRAME_DELAY:
            sdl2.SDL_Delay(FRAME_DELAY - frame_time)

    sdl2.ext.quit()

if __name__ == "__main__":
    sys.exit(run())