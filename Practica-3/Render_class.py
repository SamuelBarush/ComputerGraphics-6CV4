import sdl2.ext
from bresenham import Bresenham

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

