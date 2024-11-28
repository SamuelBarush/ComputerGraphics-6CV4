import sys
import sdl2
import sdl2.ext
import numpy as np
from OBJLoader import OBJLoader
from Matrix_class import Matrix
from Vector_class import Vector
from Render_class import Render

FOV = 120
FPS = 60
DISTANCE = 5

WIDTH = 800
HEIGHT = 600

def project(v, fov, distance, width, height):
    x = v[0]
    y = v[1]
    z = v[2]

    factor = fov / (distance + z)  # Calcula el factor de proyección
    x_2d = int(x * factor + width // 2)  # Proyecta la coordenada X
    y_2d = int(-y * factor + height // 2)  # Proyecta la coordenada Y
    return np.array([x_2d, y_2d])

def update(obj, angle_x, angle_y, angle_z):
    translation = (0, 0, 0)

    Matrix_scaled = Matrix.scaling_matrix(1, 1, 1)
    Matrix_rotated_x = Matrix.rotation_matrix_x(angle_x)
    Matrix_rotated_y = Matrix.rotation_matrix_y(angle_y)
    Matrix_rotated_z = Matrix.rotation_matrix_z(angle_z)
    Matrix_translated = Matrix.translation_matrix(*translation)

    Matrix_Transformation = Matrix_translated @ Matrix_rotated_x @ Matrix_rotated_y @ Matrix_rotated_z @ Matrix_scaled

    transformed_vertices = []

    for face in obj.faces:
        v1_index, v2_index, v3_index = face[:3]
        v0 = obj.vertices[v1_index]
        v1 = obj.vertices[v2_index]
        v2 = obj.vertices[v3_index]

        if not Render.backface_culling(v0, v1, v2):
            continue

        vector4d_0 = Vector.convert3d_to_4d(v0)
        vector4d_1 = Vector.convert3d_to_4d(v1)
        vector4d_2 = Vector.convert3d_to_4d(v2)
        vector4d_0 = Matrix.matrix_vector_product(Matrix_Transformation, vector4d_0)
        vector4d_1 = Matrix.matrix_vector_product(Matrix_Transformation, vector4d_1)
        vector4d_2 = Matrix.matrix_vector_product(Matrix_Transformation, vector4d_2)
        vector3d_0 = Vector.convert4d_to_3d(vector4d_0)
        vector3d_1 = Vector.convert4d_to_3d(vector4d_1)
        vector3d_2 = Vector.convert4d_to_3d(vector4d_2)
        vector2d_0 = project(vector3d_0, FOV, DISTANCE, WIDTH, HEIGHT)
        vector2d_1 = project(vector3d_1, FOV, DISTANCE, WIDTH, HEIGHT)
        vector2d_2 = project(vector3d_2, FOV, DISTANCE, WIDTH, HEIGHT)
        transformed_vertices.append(vector2d_0)
        transformed_vertices.append(vector2d_1)
        transformed_vertices.append(vector2d_2)
        
    return transformed_vertices

    #for v in obj.vertices:
    #    vector4d = Vector.convert3d_to_4d(v)
    #    vector4d = Matrix.matrix_vector_product(Matrix_Transformation, vector4d)
    #    vector3d = Vector.convert4d_to_3d(vector4d)
    #    vector2d = project(vector3d, FOV, DISTANCE, WIDTH, HEIGHT)

    #    transformed_vertices.append(vector2d)

    #return transformed_vertices

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Rotating 3D OBJ Model", size=(WIDTH, HEIGHT))
    window.show()

    renderer = sdl2.ext.Renderer(window)

    # Carga el archivo .obj
    obj = OBJLoader('cube.obj')

    running = True

    angle_x = 0
    angle_y = 0
    angle_z = 0

    # Estados para las funciones
    draw_edges = False
    color_faces = False
    draw_vertices = False

    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_i:
                    draw_edges = not draw_edges  # Cambia el estado de dibujar aristas
                elif event.key.keysym.sym == sdl2.SDLK_f:
                    color_faces = not color_faces  # Cambia el estado de colorear caras
                elif event.key.keysym.sym == sdl2.SDLK_v:
                    draw_vertices = not draw_vertices  # Cambia el estado de dibujar vértices

        # Limpia la pantalla
        renderer.clear(sdl2.ext.Color(0, 0, 0))

        # Actualiza los vértices
        vertices = update(obj, angle_x, angle_y, angle_z)

        # Dibuja las aristas
        if draw_edges:
            Render.render(obj.faces, vertices, renderer)

        # Dibuja los vértices
        if draw_vertices:
            Render.draw_vertices(vertices, renderer)

        # Dibuja las caras
        if color_faces:
            Render.DrawFilledTriangle(vertices, renderer)

        # Actualiza los ángulos
        angle_x += 0.01
        angle_y += 0.01
        angle_z += 0.01

        # Actualiza la pantalla
        renderer.present()

        # Espera para mantener el Frame Rate
        sdl2.SDL_Delay(int(1000 / FPS))

    sdl2.ext.quit()

if __name__ == "__main__":
    sys.exit(run())