import numpy as np
import os.path
# Custom modules
from modules import voiddetect as vd
from modules import checkCircle as check
from modules import intersection_dic as ipd


def selected_gb(name): # Name sample
    """
    Return output/[input sample]/selected.txt with the values of
    the new selected grain boundary position for the input sample.

    The selected grain boundary are detected via the checkCollision module.
    It disregard the grain boundary relevence into the void.
    """
    ### get current directory
    pa_current = os.environ['PWD']

    # define paths for convenience
    pa_pic = pa_current + '/pyinputs/' + name + '.jpg'
    pa_txt = pa_current + '/pyinputs/' + name + '.txt'

    ## Input data
    gbdata = np.genfromtxt(pa_txt)
    pa_selected_old = pa_current + '/saboutputs/' + name + '/selected.txt'
    selected_data_old = np.genfromtxt(pa_selected_old)
    ### Starting points
    staptsx = gbdata[:, 15]
    staptsy = gbdata[:, 16]
    #### Ending points
    endptsx = gbdata[:, 17]
    endptsy = gbdata[:, 18]
    # Find dimensions for picture
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    # define maximum void area as a multiple of average grain size (last number is factor of multiplication)
    maxarea = width * height / np.amax(gbdata[:, 20]) * 2.5

    ### run voiddetect module and return centers and radii of detected voids
    centers, radii, vheight, voidimage, drawing = vd.findvoid(pa_pic, name, maxarea)
    height_factor = drawing.shape[0]/np.int64(height)
    width_factor = drawing.shape[1]/np.int64(width)

    sel=[]
    dist={}
    void_id=[]
    pt3={}
    ipd_total={}
    near_points={}

    for i, center in enumerate(centers):  # Centers
        location_dic_samevoid={}
        for j, _ in enumerate(endptsx):   # j boundary tag
            x_s = np.int64(width_factor * staptsx[j])
            y_s = np.int64(height_factor * staptsy[j])
            x_e = np.int64(width_factor * endptsx[j])
            y_e = np.int64(height_factor * endptsy[j])

            gb=[(x_s,y_s),(x_e,y_e)]

            if check.checkCollision(x_s, x_e, y_s, y_e, center[0], center[1], radii[i]) is True:
                sel.append(j)

                d = check.min_distance_from_center_real(center, gb, width_factor, height_factor)
                dist[j]=d

                void_id.append(i)

                gb_s=(x_s, y_s)
                gb_e=(x_e, y_e)

                inter_points = check.circle_line_segment_intersection(center, radii[i], gb_s, gb_e)
                inter_point_within = check.circle_line_segment_intersection(center, radii[i], gb_s, gb_e, full_line=False)

                for pt in inter_points:
                    if pt not in inter_point_within:
                        pt3[j]=(format(pt[0], '.15f'), format(pt[1], '.15f'))
                        #pt3.append(pt)

    # Compute the distance from the mid point of the gb with the near void center
    for k, __ in enumerate(endptsx):   # k boundary tag
        gbs=[staptsx[k], staptsy[k]]
        gbe=[endptsx[k], endptsy[k]]
        if k not in sel:
            d_r = check.min_dis_allgb_centers(centers, gbs, gbe,width_factor,height_factor)
            dist[k]=d_r

        #ipd_partial=ipd.intersection_dic(location_dic_samevoid,center,radii[i])
        #ipd_total.update(ipd_partial)

        #near_partial=ipd.near_point(location_dic_samevoid, center, radii[i])
        #near_points.update(near_partial)

    for n,se in enumerate(sel):
        if se not in pt3.keys():
            pt3[se]=(-1,-1)
    # Pt3 it a dicc key:selected gb, value: interesection points


    return sel, dist, void_id, pt3
