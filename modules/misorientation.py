import numpy as np

def symmetry_operators(structure, use_miller_bravais=False):
    """ FIX IT - from .sym_op import symmetry_operators as sym
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


def eul2orient(theta):  # Radians
    g = np.array([[np.cos(theta[0]) * np.cos(theta[2]) - np.sin(theta[0]) * np.sin(theta[2]) * np.cos(theta[1]),
                   np.sin(theta[0]) * np.cos(theta[2]) + np.cos(theta[0]) * np.sin(theta[2]) * np.cos(theta[1]),
                   np.sin(theta[2]) * np.sin(theta[1])],
                  [(-1) * np.cos(theta[0]) * np.sin(theta[2]) - np.sin(theta[0]) * np.cos(theta[2]) * np.cos(theta[1]),
                   (-1) * np.sin(theta[0]) * np.sin(theta[2]) + np.cos(theta[0]) * np.cos(theta[2]) * np.cos(theta[1]),
                   np.cos(theta[2]) * np.sin(theta[1])],
                  [np.sin(theta[0]) * np.sin(theta[1]), -np.cos(theta[0]) * np.sin(theta[1]), np.cos(theta[1])]])
    return g


def orient2ang(R1):
    """From the misorientation matrix (R1),
    compute the rotation angle (ang) [rad] and the rotation axis (ax) [u,v,w]
    """

    misang = np.arccos(0.5 * (R1[0][0] + R1[1][1] + R1[2][2] - 1))

    p1 = (R1[1][2] - R1[2][1]) / (2 * np.sin(misang))
    p2 = (R1[2][0] - R1[0][2]) / (2 * np.sin(misang))
    p3 = (R1[0][1] - R1[1][0]) / (2 * np.sin(misang))

    ax = [p1, p2, p3]
    ang = misang
    ax = ax / np.linalg.norm(ax)
    return ang, ax


def symm_mis_angle(euler1, euler2):  # Radians - BCC STRUCTURE - CUBIC
    """ From two respective euler values of touching gb (euler 1 and euler2)
    Compute all the possible symmetric angles (mis_angles) {UNCOMMENT}
     and take the min value (misang) - [RAD]"""
    mis_angles = []
    g1 = eul2orient(euler1)
    g2 = eul2orient(euler2)
    g=misorientation_matrix(g1,g2)

    for sym_op in symmetry_operators('cubic'):
        m_sym=np.dot(g,sym_op)
        ang, ax = orient2ang(m_sym)
        mis_angles.append(ang)
    misang=np.amin(mis_angles)
    return misang #,mis_angles


def misorientation_matrix(g1, g2):  # Radians
    misorientation_matrix = np.dot(g1, np.linalg.inv(g2))
    return misorientation_matrix


