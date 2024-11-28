import numpy as np

class OBJLoader:
    def __init__(self, filename):
        self.vertices = np.array([])  # Matriz de vértices XYZ
        self.faces = []
        self.load_obj(filename)

    def load_obj(self, filename):
        vertices_list = []  # Lista para almacenar vértices temporalmente
        with open(filename, 'r') as file:
            for line in file:
                parts = line.split()
                if not parts:
                    continue
                if parts[0] == 'v':  # Si es un vértice
                    vertices_list.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif parts[0] == 'f':  # Si es una cara (triángulo)
                    face = [int(index.split('/')[0]) - 1 for index in parts[1:]]
                    self.faces.append(face)
        # Convertimos la lista de vértices en un arreglo NumPy
        self.vertices = np.array(vertices_list, dtype=np.float32)

