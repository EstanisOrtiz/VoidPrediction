import numpy as np

def checkCollision(x1, x2, y1, y2, x, y, radius):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    # Finding the distance of line
    # from center.
    dist = ((abs(a * x + b * y + c)) /
            np.sqrt(a * a + b * b))

    #dist= abs( (y2-y1)*x - (x2-x1)*y + x2*y1 + y2*x1 )/np.sqrt( (y2-y1)^2 + (x2-x1)^2)

    # Checking if the distance is less
    # than, greater than or equal to radius.
    if (radius == dist):
        # print("Touch")
        return True
    elif (radius > dist):
        # print("Intersect")
        return True
    else:
        # print("Outside")
        return False
