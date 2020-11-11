import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import time

a = 1

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# vertices
v = np.array([[a/2, a/2, -a/2], [-a/2, -a/2, -a/2], [-a/2, a/2, a/2], [a/2, a/2, a/2],
              [-a/2, a/2, -a/2], [a/2, -a/2, -a/2], [-a/2, -a/2, a/2],
              [a/2, -a/2, a/2]])
ax.scatter3D(v[:, 0], v[:, 1], v[:, 2], )

# generate list of sides' polygons
verts = [[v[0], v[3], v[2], v[4]], [v[0], v[5], v[7], v[3]], [v[4], v[2], v[6], v[1]], [v[1], v[5], v[7], v[6]],
         [v[0], v[4], v[1], v[5]], [v[2], v[3], v[7], v[6]]]

# plot sides
ax.add_collection3d(Poly3DCollection(verts,
                                     facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))


atoms = np.array([[0, 0, 0],
                  [0.5*a, 0.5*a, 0.5*a],
                  [0.5*a, 0.5*a, -0.5*a],
                  [0.5*a, -0.5*a, 0.5*a],
                  [0.5*a, -0.5*a, -0.5*a],
                  [-0.5*a, 0.5*a, 0.5*a],
                  [-0.5*a, 0.5*a, -0.5*a],
                  [-0.5*a, -0.5*a, 0.5*a],
                  [-0.5*a, -0.5*a, -0.5*a]])

plane_neutral=atoms[:5]
plane_top=atoms[5:8]
plane_bottom=atoms[8:]

atoms_label = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11')

for x, y, z in atoms:
    ax.scatter(x, y, z, s=100, color='black', marker='o')

#for x, y, z, a_label in atoms, atoms_label:
    #ax.scatter(x, y, z, s=60 ,color='black', marker='o')
    #ax.text(x, y, z, label, a_label)

plt.figure(1)
ax.set_xlabel('X = a')
ax.set_ylabel('Y = a')
ax.set_zlabel('Z = a')

plt.show()

time.sleep(2)
plt.close()