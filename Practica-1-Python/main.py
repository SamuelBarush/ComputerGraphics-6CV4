import pygame
import numpy as np
import math

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
window_width = 800
window_height = 600

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("3D Cube Renderer - Orthogonal and Perspective Projection")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Definir los puntos del cubo en 3D
def create_cube():
    points = [
        np.array([-1, -1, -1]),
        np.array([1, -1, -1]),
        np.array([1, 1, -1]),
        np.array([-1, 1, -1]),
        np.array([-1, -1, 1]),
        np.array([1, -1, 1]),
        np.array([1, 1, 1]),
        np.array([-1, 1, 1])
    ]
    return points

cube_points = create_cube()

# Parámetros de la proyección
fov = 120  # Campo de visión (para perspectiva)
scale = np.array([window_width // 100, window_height // 100])  # Escala ajustada
distance_from_camera = 5  # Distancia desde la "cámara" (para perspectiva)
rotation = [0, 0, 0]  # Inicialización de las rotaciones en x, y, z

# Variable para alternar entre proyección ortogonal y perspectiva
use_perspective = True  # Cambiar a False para proyección ortogonal

# Función para rotar un punto en 3D
def rotate_point(point, angle_x, angle_y, angle_z):
    rotation_x = np.array([
        [1, 0, 0],
        [0, math.cos(angle_x), -math.sin(angle_x)],
        [0, math.sin(angle_x), math.cos(angle_x)]
    ])

    rotation_y = np.array([
        [math.cos(angle_y), 0, math.sin(angle_y)],
        [0, 1, 0],
        [-math.sin(angle_y), 0, math.cos(angle_y)]
    ])

    rotation_z = np.array([
        [math.cos(angle_z), -math.sin(angle_z), 0],
        [math.sin(angle_z), math.cos(angle_z), 0],
        [0, 0, 1]
    ])

    rotated_point = np.dot(rotation_x, point)
    rotated_point = np.dot(rotation_y, rotated_point)
    rotated_point = np.dot(rotation_z, rotated_point)

    return rotated_point

# Proyección ortogonal: ignora la profundidad (z)
def orthogonal_project(point):
    return point[:2]  # Solo devolver (x, y), ignorando z

# Proyección en perspectiva: tiene en cuenta la distancia al observador
def perspective_project(point):
    factor = fov / (distance_from_camera - point[2])
    projected_point = point[:2] * factor
    return projected_point

# Interpolación lineal para dividir las aristas del cubo en puntos
def interpolate(p1, p2, num_points):
    return [(p1 * (1 - t) + p2 * t) for t in np.linspace(0, 1, num_points)]

# Dibujar las aristas del cubo con puntos
def draw_edges(points, rotation):
    rotated_points = [rotate_point(point, *rotation) for point in points]
    
    # Aplicar la proyección que se esté utilizando
    if use_perspective:
        projected_points = [perspective_project(p) for p in rotated_points]
    else:
        projected_points = [orthogonal_project(p) for p in rotated_points]

    # Convertir los puntos proyectados a coordenadas de pantalla
    screen_points = [(int(p[0] * scale[0]) + window_width // 2, int(p[1] * scale[1]) + window_height // 2) for p in projected_points]

    # Definir las aristas del cubo
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Base del cubo
        (4, 5), (5, 6), (6, 7), (7, 4),  # Parte superior del cubo
        (0, 4), (1, 5), (2, 6), (3, 7)   # Conexiones verticales
    ]

    # Dibujar puntos a lo largo de cada arista
    num_points_per_edge = 5
    for edge in edges:
        p1, p2 = screen_points[edge[0]], screen_points[edge[1]]
        edge_points = interpolate(np.array(p1), np.array(p2), num_points_per_edge)
        for point in edge_points:
            pygame.draw.circle(screen, WHITE, (int(point[0]), int(point[1])), 3)

# Dibujar las caras del cubo con puntos
def draw_faces(points, rotation):
    rotated_points = [rotate_point(point, *rotation) for point in points]
    
    # Aplicar la proyección
    if use_perspective:
        projected_points = [perspective_project(p) for p in rotated_points]
    else:
        projected_points = [orthogonal_project(p) for p in rotated_points]

    # Convertir los puntos proyectados a coordenadas de pantalla
    screen_points = [(int(p[0] * scale[0]) + window_width // 2, int(p[1] * scale[1]) + window_height // 2) for p in projected_points]

    # Definir las caras del cubo (cada cara es un rectángulo formado por 4 puntos)
    faces = [
        (0, 1, 2, 3),  # Cara trasera
        (4, 5, 6, 7),  # Cara delantera
        (0, 1, 5, 4),  # Cara lateral izquierda
        (2, 3, 7, 6),  # Cara lateral derecha
        (0, 3, 7, 4),  # Cara inferior
        (1, 2, 6, 5)   # Cara superior
    ]

    num_points_per_face = 5  # Número de puntos por cara

    # Dibujar puntos en cada cara del cubo
    for face in faces:
        p1, p2, p3, p4 = screen_points[face[0]], screen_points[face[1]], screen_points[face[2]], screen_points[face[3]]
        
        # Interpolar puntos en la cuadrícula de la cara
        for t1 in np.linspace(0, 1, num_points_per_face):
            for t2 in np.linspace(0, 1, num_points_per_face):
                point_on_face = (1 - t1) * ((1 - t2) * np.array(p1) + t2 * np.array(p2)) + t1 * ((1 - t2) * np.array(p4) + t2 * np.array(p3))
                pygame.draw.circle(screen, WHITE, (int(point_on_face[0]), int(point_on_face[1])), 2)

# Ciclo principal del programa
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Incrementar la rotación del cubo
    rotation[0] += 0.01  # Rotación en X
    rotation[1] += 0.01  # Rotación en Y
    rotation[2] += 0.01  # Rotación en Z

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar las aristas del cubo con puntos
    draw_edges(cube_points, rotation)

    # Dibujar las caras del cubo con puntos
    draw_faces(cube_points, rotation)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    clock.tick(30)

# Salir de Pygame
pygame.quit()
