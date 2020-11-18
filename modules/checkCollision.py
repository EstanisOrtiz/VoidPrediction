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
    :return: boolean expression to whether the grain boundary is or is not inside the void
    """
    fos=1.5 # Factor of safety on the radiius

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
