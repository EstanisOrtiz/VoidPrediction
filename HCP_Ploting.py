import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import time

a1 = 1
a2 = np.sqrt(3) * a1
c = 1.587 * a1

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# vertices
v = np.array([[a1 / 2, a2 / 2, -c / 2], [-a1 / 2, -a2 / 2, -c / 2], [-a1 / 2, a2 / 2, c / 2], [a1 / 2, a2 / 2, c / 2],
              [-a1 / 2, a2 / 2, -c / 2], [a1 / 2, -a2 / 2, -c / 2], [-a1 / 2, -a2 / 2, c / 2],
              [a1 / 2, -a2 / 2, c / 2]])
ax.scatter3D(v[:, 0], v[:, 1], v[:, 2], )

# generate list of sides' polygons
verts = [[v[0], v[3], v[2], v[4]], [v[0], v[5], v[7], v[3]], [v[4], v[2], v[6], v[1]], [v[1], v[5], v[7], v[6]],
         [v[0], v[4], v[1], v[5]], [v[2], v[3], v[7], v[6]]]

# plot sides
ax.add_collection3d(Poly3DCollection(verts,
                                     facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))


atoms = np.array([[0, 0, 0],
                  [0.5 * a1, -0.5 * np.sqrt(3.0) * a1, 0],
                  [0.5 * a1, 0.5 * np.sqrt(3.0) * a1, 0],
                  [-0.5 * a1, -0.5 * np.sqrt(3.0) * a1, 0],
                  [-0.5 * a1, 0.5 * np.sqrt(3.0) * a1, 0],

                  [0, 1/3* np.sqrt(3.0) * a1, 0.5 * c],
                  [0.5 * a1, -1/6 * np.sqrt(3.0) * a1, 0.5 * c],
                  [-0.5 * a1,-1/6 * np.sqrt(3.0) * a1, 0.5 * c],

                  [0, 1/3 * np.sqrt(3.0) * a1, -0.5 * c],
                  [0.5 * a1, -1/6 * np.sqrt(3.0) * a1, -0.5 * c],
                  [-0.5 * a1, -1/6 * np.sqrt(3.0) * a1, -0.5 * c]])

plane_neutral=atoms[:5]
plane_top=atoms[5:8]
plane_bottom=atoms[8:]

atoms_label = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11')

for x, y, z in atoms:
    ax.scatter(x, y, z, s=60, color='black', marker='o')

#for x, y, z, a_label in atoms, atoms_label:
    #ax.scatter(x, y, z, s=60 ,color='black', marker='o')
    #ax.text(x, y, z, label, a_label)

plt.figure(1)
ax.set_xlabel('X = a')
ax.set_ylabel('Y = √3*a')
ax.set_zlabel('Z = c')

plt.figure(2)
plt.subplot(3,1,1)
plt.plot([i[0] for i in plane_top], [j[1] for j in plane_top], 'ro')
plt.title('Top surface')
plt.grid()
plt.ylabel('Y = √3*a')

plt.subplot(3,1,2)
plt.plot([i[0] for i in plane_neutral], [j[1] for j in plane_neutral], 'ro')
plt.title('Mid Surface')
plt.grid()
plt.ylabel('Y = √3*a')

plt.subplot(3,1,3)
plt.plot(plane_bottom[:,0], plane_bottom[:,1], 'ro')
plt.title('Bottom Surface')
plt.grid()
plt.xlabel('X = a')
plt.ylabel('Y = √3*a')

plt.show()

time.sleep(2)
plt.close()

