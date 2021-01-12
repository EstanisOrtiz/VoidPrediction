import numpy as np
def checkCollision(x1, x2, y1, y2, x, y, radius):
    """
    :param x1: start coordinate x of the grain boundary.
    :param x2: end coordinate x of the grain boundary.
    :param y1: start coordinate y of the grain boundary.
    :param y2: end coordinate y of the grain boundary.
    :param x: coordinate x of the void center
    :param y: coordinate y of the void center
    :param radius: radii of the void
    :param fos: Factor of safety on the radiius
    :return: boolean expression to whether the grain boundary is or is not inside the void
    """
    #fos: Factor of safety on the radiius
    if radius<5:
        fos=1.8
    elif radius<8:
        fos = 1.5
    else:
        fos = 1

    if x1>(x - radius*fos) and x1<(x + radius*fos) and y1>(y - radius*fos) and y1<(y + radius*fos) \
            or x2>(x - radius*fos) and x2<(x + radius*fos) and y2>(y - radius*fos) and y2<(y + radius*fos):
        a = y1 - y2
        b = x2 - x1
        c = (x1 - x2) * y1 + x1 * (y2 - y1)

        dist = ((abs(a * x + b * y + c)) / np.sqrt(a * a + b * b))
        if (radius == dist):
            # print("Touch")
            return True
        elif (radius > dist):
            # print("Intersect")
            return True
        else:
            # print("Outside")
            return False
    else:
        return False


def checkDist(x1, x2, y1, y2, x, y, radius):
    """
    :param x1: start coordinate x of the grain boundary.
    :param x2: end coordinate x of the grain boundary.
    :param y1: start coordinate y of the grain boundary.
    :param y2: end coordinate y of the grain boundary.
    :param x: coordinate x of the void center
    :param y: coordinate y of the void center
    :param radius: radii of the void
    :return: dist: Distance of line from center of the circle and False if it does not intesect.
    """
    a = y1 - y2
    b = x2 - x1
    c = (x1 - x2) * y1 + x1 * (y2 - y1)

    dist = ((abs(a * x + b * y + c)) / np.sqrt(a * a + b * b))

    return dist

def checkDist_old(x1, x2, y1, y2, x, y, radius):
    """
    :param x1: start coordinate x of the grain boundary.
    :param x2: end coordinate x of the grain boundary.
    :param y1: start coordinate y of the grain boundary.
    :param y2: end coordinate y of the grain boundary.
    :param x: coordinate x of the void center
    :param y: coordinate y of the void center
    :param radius: radii of the void
    :return: dist: Distance of line from center of the circle and False if it does not intesect.
    """
    fos=25
    """
    if radius<5:
        fos = 25
    elif radius<8.5:
        fos = 2.5
    else:
        fos = 1
    """

    if x1>(x - radius*fos) and x1<(x + radius*fos) and y1>(y - radius*fos) and y1<(y + radius*fos) \
            or x2>(x - radius*fos) and x2<(x + radius*fos) and y2>(y - radius*fos) and y2<(y + radius*fos):
        a = y1 - y2
        b = x2 - x1
        c = (x1 - x2) * y1 + x1 * (y2 - y1)

        dist = ((abs(a * x + b * y + c)) / np.sqrt(a * a + b * b))
        if (radius == dist) or (radius > dist):
            # Touch or Intersect
            return dist
        else:
            # Outside
            return False
    else:
        return False