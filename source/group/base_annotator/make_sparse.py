import glob
import matplotlib.pyplot as plt
from skimage import io
import scipy.sparse as sp
import numpy as np

def get_annotations():
    annotations = get_validated_user_input("Annotations(default - Labels.tif): ", "str")
    return annotatins

def make_sparse(annotations):
    sparses = []
    for layer in annotations:
        sparses.append(sp.csr_matrix(layer))
    return sparses

def save_sparse(sparses):
    i=0
    for sparse_matrix in sparses:
        sp.save_npz('sparse_matrix_'+str(i)+'.npz', sparse_matrix)
        i = i+1

#TESTING 3D SPARSE REPRESENTATION OF ANNOTATIONS#
class Sparse3D():
    """
    Class to store and access 3 dimensional sparse matrices efficiently
    """
    def __init__(self, *sparseMatrices):
        """
        Constructor
        Takes a stack of sparse 2D matrices with the same dimensions
        """
        self.data = sp.vstack(sparseMatrices, "dok")
        self.shape = (len(sparseMatrices), *sparseMatrices[0].shape)
        self._dim1_jump = np.arange(0, self.shape[1]*self.shape[0], self.shape[1])
        self._dim1 = np.arange(self.shape[0])
        self._dim2 = np.arange(self.shape[1])

    def __getitem__(self, pos):
        if not type(pos) == tuple:
            if not hasattr(pos, "__iter__") and not type(pos) == slice:
                return self.data[self._dim1_jump[pos] + self._dim2]
            else:
                return Sparse3D(*(self[self._dim1[i]] for i in self._dim1[pos]))
        elif len(pos) > 3:
            raise IndexError("too many indices for array")
        else:
            if (not hasattr(pos[0], "__iter__") and not type(pos[0]) == slice or
                not hasattr(pos[1], "__iter__") and not type(pos[1]) == slice):
                if len(pos) == 2:
                    result = self.data[self._dim1_jump[pos[0]] + self._dim2[pos[1]]]
                else:
                    result = self.data[self._dim1_jump[pos[0]] + self._dim2[pos[1]], pos[2]].T
                    if hasattr(pos[2], "__iter__") or type(pos[2]) == slice:
                        result = result.T
                return result
            else:
                if len(pos) == 2:
                    return Sparse3D(*(self[i, self._dim2[pos[1]]] for i in self._dim1[pos[0]]))
                else:
                    if not hasattr(pos[2], "__iter__") and not type(pos[2]) == slice:
                        return sp.vstack([self[self._dim1[pos[0]], i, pos[2]]
                                          for i in self._dim2[pos[1]]]).T
                    else:
                        return Sparse3D(*(self[i, self._dim2[pos[1]], pos[2]]
                                          for i in self._dim1[pos[0]]))

    def toarray(self):
        return np.array([self[i].toarray() for i in range(self.shape[0])])
if (__name__ == '__main__'):
    annotations = get_annotations()
    sparses = make_sparse(annotations)
    save_sparse(sparses)
