# importing necessary modules
import matplotlib.pyplot as plt
from random import randint
import numpy as np


class IFS:

    def __init__(self, coeffs):
        self.coeffs = coeffs
        self.data = np.array([[0, 0]])
        self.T = self.create_funcs()
        # print(self.data)

    def create_funcs(self):
        T = []
        for c in self.coeffs:
            t = np.array(c[:4]).reshape(2, 2)
            h = np.array(c[4:])
            T.append((t, h))

        return T

    def create_attractor(self, n_iter):
        for n in range(n_iter):
            for point in self.data:
                for t in self.T:
                    self.data = np.vstack((
                        self.data,
                        point.dot(t[0]) + t[1],
                    ))
        self.data = self.data.T


n_iter = 7
C = [
    (0.5, 0, 0, 0.5, 0, 0),
    (0.5, 0, 0, 0.5, 0.5, 0),
    (0.5, 0, 0, 0.5, 0.25, 0.433),
]
ifs = IFS(C)
ifs.create_attractor(n_iter)
plt.scatter(ifs.data[0], ifs.data[1], s = 50 / n_iter, edgecolor ='green', marker='s')
plt.show()