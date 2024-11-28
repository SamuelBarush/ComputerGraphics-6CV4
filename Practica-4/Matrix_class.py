import numpy as np


class Matrix:
    @staticmethod
    def identity_matrix():
        return np.identity(4)
    
    def scaling_matrix(sx,sy,sz):
        return np.array([[sx,0,0,0],
                         [0,sy,0,0],
                         [0,0,sz,0],
                         [0,0,0,1]])
    
    def rotation_matrix_x(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[1,0,0,0],
                         [0,c,-s,0],
                         [0,s,c,0],
                         [0,0,0,1]])
    
    def rotation_matrix_y(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[c,0,s,0],
                         [0,1,0,0],
                         [-s,0,c,0],
                         [0,0,0,1]])
    
    def rotation_matrix_z(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[c,-s,0,0],
                         [s,c,0,0],
                         [0,0,1,0],
                         [0,0,0,1]])
    
    def translation_matrix(tx,ty,tz):
        return np.array([[1,0,0,tx],
                         [0,1,0,ty],
                         [0,0,1,tz],
                         [0,0,0,1]])
    
    def convert (vertices):
        num_vertices = vertices.shape[0]
        homogeneous_matrix = np.ones((num_vertices, 4))
        homogeneous_matrix[:,:3] = vertices

        return homogeneous_matrix
    
    def matrix_vector_product(matrix, vector):
        return matrix @ vector

    