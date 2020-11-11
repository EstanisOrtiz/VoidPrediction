import numpy as np

def symmetry_operators(structure, use_miller_bravais=False):
    """Define the equivalent crystal symmetries.

    Those come from Randle & Engler, 2000. For instance in the cubic
    crystal struture, for instance there are 24 equivalent cube orientations.

    struct : Structure of the material (cubic, hexagonal, orthorhombic, tetragonal, triclinic)

    :returns array: A numpy array of shape (n, 3, 3) where n is the \
    number of symmetries of the given crystal structure.
    """
    if structure == 'cubic':
        sym = np.zeros((24, 3, 3), dtype=np.float)
        sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
        sym[1] = np.array([[0., 0., -1.], [0., -1., 0.], [-1., 0., 0.]])
        sym[2] = np.array([[0., 0., -1.], [0., 1., 0.], [1., 0., 0.]])
        sym[3] = np.array([[-1., 0., 0.], [0., 1., 0.], [0., 0., -1.]])
        sym[4] = np.array([[0., 0., 1.], [0., 1., 0.], [-1., 0., 0.]])
        sym[5] = np.array([[1., 0., 0.], [0., 0., -1.], [0., 1., 0.]])
        sym[6] = np.array([[1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
        sym[7] = np.array([[1., 0., 0.], [0., 0., 1.], [0., -1., 0.]])
        sym[8] = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 1.]])
        sym[9] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., 1.]])
        sym[10] = np.array([[0., 1., 0.], [-1., 0., 0.], [0., 0., 1.]])
        sym[11] = np.array([[0., 0., 1.], [1., 0., 0.], [0., 1., 0.]])
        sym[12] = np.array([[0., 1., 0.], [0., 0., 1.], [1., 0., 0.]])
        sym[13] = np.array([[0., 0., -1.], [-1., 0., 0.], [0., 1., 0.]])
        sym[14] = np.array([[0., -1., 0.], [0., 0., 1.], [-1., 0., 0.]])
        sym[15] = np.array([[0., 1., 0.], [0., 0., -1.], [-1., 0., 0.]])
        sym[16] = np.array([[0., 0., -1.], [1., 0., 0.], [0., -1., 0.]])
        sym[17] = np.array([[0., 0., 1.], [-1., 0., 0.], [0., -1., 0.]])
        sym[18] = np.array([[0., -1., 0.], [0., 0., -1.], [1., 0., 0.]])
        sym[19] = np.array([[0., 1., 0.], [1., 0., 0.], [0., 0., -1.]])
        sym[20] = np.array([[-1., 0., 0.], [0., 0., 1.], [0., 1., 0.]])
        sym[21] = np.array([[0., 0., 1.], [0., -1., 0.], [1., 0., 0.]])
        sym[22] = np.array([[0., -1., 0.], [-1., 0., 0.], [0., 0., -1.]])
        sym[23] = np.array([[-1., 0., 0.], [0., 0., -1.], [0., -1., 0.]])

    elif structure == "hexagonal":
        if use_miller_bravais:
            # using the Miller-Bravais representation here
            sym = np.zeros((12, 4, 4), dtype=np.int)
            sym[0] = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
            sym[1] = np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
            sym[2] = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]])
            sym[3] = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
            sym[4] = np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1]])
            sym[5] = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, -1]])
            sym[6] = np.array([[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
            sym[7] = np.array([[0, 0, -1, 0], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 1]])
            sym[8] = np.array([[0, -1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, 0], [0, 0, 0, 1]])
            sym[9] = np.array([[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]])
            sym[10] = np.array([[0, 0, -1, 0], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, -1]])
            sym[11] = np.array([[0, -1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, 0], [0, 0, 0, -1]])
        else:
            sym = np.zeros((12, 3, 3), dtype=np.float)
            s60 = np.sin(60 * np.pi / 180)
            sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
            sym[1] = np.array([[0.5, s60, 0.], [-s60, 0.5, 0.], [0., 0., 1.]])
            sym[2] = np.array([[-0.5, s60, 0.], [-s60, -0.5, 0.], [0., 0., 1.]])
            sym[3] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., 1.]])
            sym[4] = np.array([[-0.5, -s60, 0.], [s60, -0.5, 0.], [0., 0., 1.]])
            sym[5] = np.array([[0.5, -s60, 0.], [s60, 0.5, 0.], [0., 0., 1.]])
            sym[6] = np.array([[1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
            sym[7] = np.array([[0.5, s60, 0.], [s60, -0.5, 0.], [0., 0., -1.]])
            sym[8] = np.array([[-0.5, s60, 0.], [s60, 0.5, 0.], [0., 0., -1.]])
            sym[9] = np.array([[-1., 0., 0.], [0., 1., 0.], [0., 0., -1.]])
            sym[10] = np.array([[-0.5, -s60, 0.], [-s60, 0.5, 0.], [0., 0., -1.]])
            sym[11] = np.array([[0.5, -s60, 0.], [-s60, -0.5, 0.], [0., 0., -1.]])

    elif structure == "orthorhombic":
        sym = np.zeros((4, 3, 3), dtype=np.float)
        sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
        sym[1] = np.array([[1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
        sym[2] = np.array([[-1., 0., -1.], [0., 1., 0.], [0., 0., -1.]])
        sym[3] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., 1.]])
    elif structure == "tetragonal":
        sym = np.zeros((8, 3, 3), dtype=np.float)
        sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
        sym[1] = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 1.]])
        sym[2] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., 1.]])
        sym[3] = np.array([[0., 1., 0.], [-1., 0., 0.], [0., 0., 1.]])
        sym[4] = np.array([[1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
        sym[5] = np.array([[-1., 0., 0.], [0., 1., 0.], [0., 0., -1.]])
        sym[6] = np.array([[0., 1., 0.], [1., 0., 0.], [0., 0., -1.]])
        sym[7] = np.array([[0., -1., 0.], [-1., 0., 0.], [0., 0., -1.]])

    elif structure == 'triclinic':
        sym = np.zeros((1, 3, 3), dtype=np.float)
        sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
    else:
        print('warning, symmetry not supported: %s' % structure)
    return sym