class OBJLoader:
    def __init__(self, filename):
        self.vertices = []
        self.faces = []
        self.load_obj(filename)

    def load_obj(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                parts = line.split()
                if not parts:
                    continue
                if parts[0] == 'v':  # Vértice
                    self.vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif parts[0] == 'f':  # Cara (triángulo)
                    face = [int(index.split('/')[0]) - 1 for index in parts[1:]]
                    self.faces.append(face)
