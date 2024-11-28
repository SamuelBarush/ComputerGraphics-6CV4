import numpy as np

class Ligth:
    def __init__(self):
        Direction = np.array([0, 0, 1])

    def set_Intensity(self, color, percentageFactor):
        r = color[0] * percentageFactor
        g = color[1] * percentageFactor
        b = color[2] * percentageFactor

        new_color = np.array([r, g, b])
        return new_color
    
    @staticmethod
    def CalculateNormal(v1,v2,v3):
        U = v2 - v1
        V = v3 - v1
        normal = np.cross(U,V)
        return normal
