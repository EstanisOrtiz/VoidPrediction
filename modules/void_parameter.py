from collections import defaultdict
from .checkCollision import *

def void_parameter(gbdata, selected, centers, radii, drawing):
    """
    :param gbdata: All data of the ebsd sample.
    :param selected: Position of the grains boundary inside affected by a void.
    :param centers: All coordinates of the each void center.
    :param radii: All radii values of each void.
    :param drawing: Size of the sample.
    :return: gb_par -> Dictionary with Key=selected boundary & Value=Void Parameter.
    """
    ### Starting points
    staptsx = gbdata[:, 15]
    staptsy = gbdata[:, 16]
    #### Ending points
    endptsx = gbdata[:, 17]
    endptsy = gbdata[:, 18]
    # Find dimensions for picture
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])

    height_factor = drawing.shape[0]/np.int64(height)
    width_factor = drawing.shape[1]/np.int64(width)
    void_gb=defaultdict(list)
    void_par = {}
    gb_par={}
    s=range(len(centers))

    for i, center in enumerate(centers):  # Centers, i= number of void
        number_of_gb_in_void = 0
        for j, _ in enumerate(endptsx):
            if j in selected:  # Only void values are in 'j'
                x_s = np.int64(width_factor * staptsx[j])
                y_s = np.int64(height_factor * staptsy[j])
                x_e = np.int64(width_factor * endptsx[j])
                y_e = np.int64(height_factor * endptsy[j])
                if checkCollision(x_s, x_e, y_s, y_e, center[0], center[1], radii[i]) is True:
                    number_of_gb_in_void += 1
                    void_gb[i].append(j)

        if number_of_gb_in_void != 0:
            if number_of_gb_in_void <= 2:
                void_parameter = 1
            elif number_of_gb_in_void == 3:
                void_parameter = 0.75
            elif number_of_gb_in_void == 4:
                void_parameter = 0.5
            else:
                void_parameter = 0.25
        elif number_of_gb_in_void == 0:
            void_parameter = 0

        void_par[i] = void_parameter

    for n in s:
        for gb in void_gb[n]:
            gb_par[gb]=void_par[n]

    # Sort keys - Interesting, it breaks the dictionary form, it can be useful.
    #dictionary_items = gb_par.items()
    #sorted_items = sorted(dictionary_items)
    return gb_par