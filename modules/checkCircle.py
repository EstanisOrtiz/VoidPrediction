import numpy as np
import math

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

def circle_line_segment_intersection(circle_center, circle_radius, pt1, pt2, full_line=True, tangent_tol=1e-9):
    """ Find the points at which a circle intersects a line-segment.  This can happen at 0, 1, or 2 points.
    :param circle_center: The (x, y) location of the circle center
    :param circle_radius: The radius of the circle
    :param pt1: The (x, y) location of the first point of the segment
    :param pt2: The (x, y) location of the second point of the segment
    :param full_line: True to find intersections along full line - not just in the segment.
                      False will just return intersections within the segment.
    :param tangent_tol: Numerical tolerance at which we decide the intersections are close enough to consider it a tangent
    :return Sequence[Tuple[float, float]]: A list of length 0, 1, or 2,
                                           where each element is a point at which the circle intercepts a line segment.
    """
    (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2)**.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:  # No intersection between circle and line
        return []
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
            fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
            intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
        if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
            return [intersections[0]]
        else:
            return intersections

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    if x>0 and y>0:
        inter_point=[x,y]
        return inter_point
    else:
        pass

def l_intersection(line1,line2):
    p1, p2=line1
    q1, q2=line2
    X1, Y1 = p1
    X2, Y2 = p2
    X3, Y3 = q1
    X4, Y4 = q2

    #I1 = [min(X1, X2), max(X1, X2)]
    #I2 = [min(X3, X4), max(X3, X4)]
    #Ia = [max(min(X1, X2), min(X3, X4)),
          #min(max(X1, X2), max(X3, X4))]

    if (max(X1, X2) < min(X3, X4)):
        return False  # There is no mutual abcisses

    A1 = (Y1 - Y2) / (X1 - X2)  # Pay attention to not dividing by zero
    A2 = (Y3 - Y4) / (X3 - X4)  # Pay attention to not dividing by zero
    b1 = Y1 - A1 * X1 # = Y2 - A1 * X2
    b2 = Y3 - A2 * X3 # = Y4 - A2 * X4
    if (A1 == A2):
        return False  # Parallel segments

    Xa = (b2 - b1) / (A1 - A2)  # Once again, pay attention to not dividing by zero
    Ya = A1 * Xa + b1
    #Ya = A2 * Xa + b2
    Pa=[Xa, Ya]

    if ((Xa < max(min(X1, X2), min(X3, X4))) or
            (Xa > min(max(X1, X2), max(X3, X4)))):
        return False  # intersection is out of bound
    elif str(Xa)!='nan' and str(Ya)!='nan':
        return Pa
    else:
        return False

def min_distance_from_center(center, line):
    distances=[]
    for point in line:
        x=point[0]
        y=point[1]
        x_c=center[0]
        y_c=center[1]
        distances.append(math.sqrt(((x_c - x) ** 2) + ((y_c - y) ** 2)))
    d=min(distances)
    pt=line[distances.index(d)]
    return d, pt

def min_distance_from_center_real(center, line, width_factor=1,height_factor=1):
    """ All inputs are escalated, this funcition determine the real distance"""
    distances=[]
    for point in line:
        x=point[0]/width_factor
        y=point[1]/height_factor
        x_c=center[0]/width_factor
        y_c=center[1]/height_factor
        distances.append(math.sqrt(((x_c - x) ** 2) + ((y_c - y) ** 2)))
    d=min(distances)
    pt=line[distances.index(d)]
    return d

def min_dis_allgb_centers(centers, gb_s,gb_e,width_factor=1,height_factor=1):
    distances=[]
    x1=gb_s[0]/width_factor
    y1=gb_s[1]/height_factor
    x2=gb_e[0]/width_factor
    y2=gb_e[1]/height_factor
    gb_m=[(x1+x2)/2 , (y1+y2)/2]
    for center in centers:
        x_c=center[0]/width_factor
        y_c=center[1]/height_factor
        di=math.sqrt(((x_c - gb_m[0]) ** 2) + ((y_c - gb_m[1]) ** 2))
        distances.append(di)
    d=min(distances)
    ind=distances.index(d)
    min_center=centers[ind]
    return d

def inside_len(gb_s,gb_e,center, radi,width_factor=1,height_factor=1):
    """
    :param gb_s: Gb Start point scaled (x1, y1)
    :param gb_e: Gb End point scaled (x2,y2)
    :param center: Void center (cx,cy)
    :param radi: Void radi
    :param width_factor:
    :param height_factor:
    :return prox: Defined length of the gb inside of the void, microns
    :return ps: [point touching the void edge, defined end point inside the void] - Not real values, its scaled
    """
    # Real values - Don't compare with circle values
    x1r=gb_s[0] / width_factor
    y1r=gb_s[1] / height_factor
    x2r=gb_e[0] / width_factor
    y2r=gb_e[1] / height_factor
    length=((x2r-x1r)**2 + (y2r-y1r)**2)**0.5

    # Re-scaled value
    x1,y1 = gb_s
    x2,y2 = gb_e

    p1=(x1 - center[0])**2 + (y1 - center[1])**2
    p2=(x2 - center[0])**2 + (y2 - center[1])**2

    p3=circle_line_segment_intersection(center, radi, gb_s, gb_e,full_line=False)

    if len(p3)==0: # The segment is all inside or outside
        if p1 < (radi ** 2) and p2 < (radi ** 2):  # Full inside
            prox=length
            ps=[gb_s,gb_e]
        else: # Outside
            prox=0
            ps=[(-1,-1),(-1,-1)] # NO POINTS

    elif len(p3)==1: # One intersecction point
        p3 = p3[0]

        # Scale values
        x3r = p3[0] / width_factor
        y3r = p3[1] / height_factor

        if p1 > (radi ** 2): # gb_e inside
            prox = ((x3r - x2r) ** 2 + (y3r - y2r) ** 2) ** 0.5
            ps=[gb_e,p3]

        elif p2 > (radi ** 2): # gb_s inside
            prox = ((p3[0] - gb_s[0]) ** 2 + (p3[1] - gb_s[1]) ** 2) ** 0.5
            ps=[gb_s,p3]

    elif len(p3)==2:
        p31=p3[0]
        p32=p3[1]

        x31r = p31[0] / width_factor
        y31r = p31[1] / height_factor
        x32r = p32[0] / width_factor
        y32r = p32[1] / height_factor

        prox=((x32r-x31r)**2 + (y32r-y31r)**2)**0.5
        ps=[p31,p32]

    return prox, ps

def distance(p0,p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
