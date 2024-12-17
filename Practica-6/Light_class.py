import numpy as np
from Vector_class import Vector

class Ligth:
    @staticmethod
    def set_Intensity(color, percentageFactor):

        if percentageFactor > 1:
            percentageFactor = 1
        elif percentageFactor < 0:
            percentageFactor = 0

        r = color[0] * percentageFactor
        g = color[1] * percentageFactor
        b = color[2] * percentageFactor

        new_color = np.array([r, g, b])
        return new_color
    
    def CalculateNormal(v1,v2,v3):
        U = v2 - v1
        V = v3 - v1
        normal = np.cross(U,V)
        normal = Vector.normalize3d(normal)
        return normal
    
    def ApplyFlatShading(normal, color, light):
        ligthIntensityFactor = - (np.dot(normal, light))
        color = Ligth.set_Intensity(color, ligthIntensityFactor)
        return color
    
    def ApplyPhongShading()