import numpy as np
def trace_angle(x1,x2,y1,y2):
    """ Compute the trace angle in degrees, angle that forms the grain boundary
    x1, y1: starting point of the boundary.
    x2, y2: ending point of the boundary
    """
    nl = [0, 0]
    nl[0] = x2 - x1
    nl[1] = y2 - y1

    if nl[1] == 0:
        trace = np.pi
    else:
        # inplane = np.arctan(nl[1]/nl[0]) + np.pi/2
        trace = np.pi - np.arctan(nl[1] / nl[0])

    if trace < 0:
        trace = np.pi + trace
    if trace > np.pi:
        trace = trace - np.pi

    ### second trace angle since out of plane is from 0 to 90.
    inplane2 = trace + np.pi

    trace=np.degrees(trace)
    return trace