import numpy as np

class Vector:
    @staticmethod

    def convert2d_to_3d(v):
        return np.array([v[0], v[1], 0])

    def convert3d_to_4d(v):
        return np.array([v[0], v[1], v[2], 1])
    
    def convert4d_to_3d(v):
        return np.array([v[0], v[1], v[2]])
    