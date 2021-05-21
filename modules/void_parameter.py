import numpy as np
from modules import intersection_dic as ipd

def void_parameter(gbdata, selected, dist, void_id, centers,radii, drawing,test=None):
    """
    :param gbdata: All data of the ebsd sample.
    :param selected: Position of the grains boundary inside affected by a void.
    :param dist: Dictionary of distance of selected gb from center of the void.
    :param centers: All coordinates of the each void center.
    :param radii: All radii values of each void.
    :param drawing: Size of the sample.
    :return: gb_par -> Dictionary with Key=selected boundary & Value=Void Parameter.
    :return: min_length: minim distance of the grain boundary, if it is less it counts like noise
    :return: dis_par: dictionary key=selected gb & value=ranking
    :return: pred_lines:
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

    height_factor = drawing.shape[0] / np.int64(height)
    width_factor = drawing.shape[1] / np.int64(width)

    void_dic={}

    for i, center in enumerate(centers):
        t = []
        for k, _ in enumerate(selected):
            if i==void_id[k]:
                t.append(selected[k])
        void_dic[i]=t
    #for j,sel in enumerate(selected):
        #dist_dic[sel]=dist[j]

    gb_par={}
    dis_par={}      # Sorted selected gb dictionary by distance from the center of the void to the near point of the gb
    ipd_total={}
    pred_lines={}
    same_inter_total={}

    min_length = 6  # Justify this min value
    f = 1.05        # Distance percentage tolerance

    for i, center in enumerate(centers):  # Centers, i= number of void
        same_void_sel = void_dic[i]
        location_dic_samevoid={}
        pre_dic={}
        for sel in same_void_sel:
            sel=int(sel)
            x_s = np.int64(width_factor * staptsx[sel])
            y_s = np.int64(height_factor * staptsy[sel])
            x_e = np.int64(width_factor * endptsx[sel])
            y_e = np.int64(height_factor * endptsy[sel])

            s_p = (np.int64(x_s), np.int64(y_s))
            e_p = (np.int64(x_e), np.int64(y_e))

            l = np.asarray(e_p) - np.asarray(s_p)
            l = np.linalg.norm(l)
            if l > min_length:  # Only void values are in 'j'
                #pre_dic[sel] = dist_dic[sel]
                pre_dic[sel] = dist[sel]
                location_dic_samevoid[sel] = [s_p, e_p]
            else:
                gb_par[sel]= -1

        ipd_partial, pred_lines_dic_partial,same_inter_dic=ipd.intersection_dic(location_dic_samevoid,center,radii[i], width_factor,height_factor)
        same_inter_total.update(same_inter_dic)
        #near_partial=ipd.near_point(location_dic_samevoid,center,radii[i])
        ipd_total.update(ipd_partial)
        pred_lines.update(pred_lines_dic_partial)
        sorted_values = sorted(pre_dic, key=lambda k: (pre_dic[k], k))
        dpr=1



        for key in sorted_values:
            dis_par[key]=dpr
            dpr=dpr+1

        dis_gb=[]
        for key in pre_dic.keys():
            dis_gb.append(key)

        if len(pre_dic)<=2:                        # Simple Junction the vp value are 1
            for p,_ in enumerate(pre_dic):
                gb_par[dis_gb[p]] = 1
        else:
            for r,di in enumerate(pre_dic.values()):
                vpr = 1
                for t,dis in enumerate(pre_dic.values()):
                    if di<=(dis*f) and r!=t:        #
                        gb_par[dis_gb[r]]= round(vpr,2)
                    elif r!=t:
                        gb_par[dis_gb[r]] = round(vpr,2)
                        vpr = vpr-0.1
                    if vpr<=0:                      # More than 10 gb
                        gb_par[dis_gb[r]]=0.05

    # Sort keys - Interesting, it breaks the dictionary form, it can be useful.
    # dictionary_items = gb_par.items()
    # sorted_items = sorted(dictionary_items)
    return gb_par, min_length, dis_par, ipd_total, pred_lines, same_inter_total