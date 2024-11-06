import sys
import sdl2
import sdl2.ext
from obj_loader import OBJLoader
from renderer import Renderer3D

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Rotating 3D OBJ Model", size=(800, 600))
    window.show()

    renderer = sdl2.ext.Renderer(window)
    running = True

    # Carga el archivo .obj
    obj = OBJLoader('cube.obj')

    # Caras
    print("Caras del Cubo")
    print(obj.faces)

    # Vértices
    print("Vértices del Cubo")
    print(obj.vertices)

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

        # Actualiza la pantalla
        renderer.present()

    sdl2.ext.quit()

if __name__ == "__main__":
    sys.exit(run())