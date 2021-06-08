import numpy as np
from modules import checkCircle as check

def intersection_dic(location_dic,center,radi,width_factor,height_factor):  # CHECK if height_factor and width_factor are necessary
    """
    :param location_dic: Dictionary {gb_id: [gb_start,gb_end]} of selected gb of the same void.
    :param gb_start: Start point of the grain boundary
    :param gb_end: End point of the grain boundary
    :param center: Center of the void []
    :param radi: Radio of the void
    :return: ipd: dictionary with {tag of the gb and value [x,y],l} where x and y are the coordinates of the first
    intersection between the other supposed continuity of the gb inside the void and l is distance of it
    supposed continuity. l -> microns.
    :return: pred_lines_dic: dic key=selected gb & Value=juncton point
    :return: same_inter: key=selected gb & Value=
    """
    gb_start=[]
    gb_end=[]
    gb_id=location_dic.keys()

    for gbs in location_dic.values():
        gb_start.append(gbs[0])
        gb_end.append(gbs[1])

    pred_lines=[]
    for gb_s, gb_e in zip(gb_start,gb_end):
        x1,y1,x2,y2=gb_s[0],gb_s[1],gb_e[0],gb_e[1]
        inter_points = check.circle_line_segment_intersection(center, radi, gb_s, gb_e)
        inter_point_within=check.circle_line_segment_intersection(center, radi, gb_s, gb_e , full_line=False)

        # Boundary that is defined inside the void and it have two possible continuity, select the larger contin.
        if len(inter_point_within)==0:
            cont_distances=[]
            x_mid_point=(x1+x2)/2
            y_mid_point=(y1+y2)/2
            for cont in inter_points:
                c_d=np.sqrt((x_mid_point - cont[0]) ** 2 + (y_mid_point - cont[1]) ** 2)
                cent_d=np.sqrt((x_mid_point - center[0]) ** 2 + (y_mid_point - center[1]) ** 2)
                cont_distances.append(c_d)
                if cent_d<=radi: # gb inside the gb void
                    ii = cont_distances.index(max(cont_distances))  # max is deleted
                    inter_point_within.append(inter_points[ii])

                elif cent_d>radi:
                    ii = cont_distances.index(min(cont_distances))  # min is deleted
                    inter_point_within.append(inter_points[ii])
                else:
                    print('WARNING!! - intersection_dic.py - line 47')
                    print(cent_d)
                    print(radi)
            #inter_point_within.append(inter_points[ii])

        for pt in inter_points:
            if pt not in inter_point_within:
                d_gb_s=np.sqrt((x1 - pt[0])**2 + (y1 - pt[1])**2)
                d_gb_e=np.sqrt((x2 - pt[0])**2 + (y2 - pt[1])**2)
                if d_gb_e<d_gb_s:
                    p3=(x2,y2)
                else:
                    p3=gb_s
                pred_lines.append([list(p3),list(pt)])
        if inter_points==inter_point_within:
            pred_lines.append([list(gb_s),[gb_s[0]+(10**-6),gb_s[1]+(10**-6)]])

    intersection={}
    all_near_pt={}
    pred_lines_dic={}
    all_min_position=[]

    for key,line1 in zip(gb_id,pred_lines):
        pred_lines_dic[key]=pred_lines
        near_pt=line1[0]
        near_pt_microns=[near_pt[0]/width_factor, near_pt[1]/height_factor]
        #dis_value, near_pt = check.min_distance_from_center(list(center), line1)
        int_points = []
        l = []
        for line2 in pred_lines:
            if line1!=line2:
                if check.l_intersection(line1, line2):
                    intersection_point = check.l_intersection(line1, line2)

                    # Compute predicted longitude in microns.
                    # Rewrite position in microns
                    xnear=near_pt[0]/width_factor
                    xinter=intersection_point[0]/width_factor
                    ynear=near_pt[1]/height_factor
                    yinter=intersection_point[1]/height_factor

                    #long = np.sqrt((near_pt[0] - intersection_point[0]) ** 2 + (near_pt[1] - intersection_point[1]) ** 2)
                    long=np.sqrt((xnear - xinter) ** 2 + (ynear - yinter) ** 2)
                    # microns
                    intersection_point_microns=[xinter,yinter]
                    int_points.append(intersection_point_microns)
                    #int_points.append(intersection_point)
                    l.append(long)

        if len(l)>0:
            l_sorted=sorted(l)
            min_ind=l.index(l_sorted[0])
            #index=l.index(min(l))
            min_position = int_points[min_ind] # Select the shorest supposed contin.
            intersection[key]=[min_position, min(l)]
            all_min_position.append(min_position)
        #all_near_pt[key]=near_pt
        all_near_pt[key]=near_pt_microns

    ipd={}
    same_inter = {}
    for i, (clave, valor) in enumerate(intersection.items()):
        int_keys = []
        min_pos=valor[0]
        dist=valor[1]
        #tol=1                 # Increase tol for test sample
        tol=0.03               # Radi tolerance to detect the lines around the intersection point.
        for n, (clave2, valor2) in enumerate(intersection.items()):  # Check common min inters points
            if clave!=clave2:
                pt1=valor2[0]
                pt2=all_near_pt[clave]
                ps=check.circle_line_segment_intersection(min_pos, tol, pt1, pt2)
                if len(ps)>0:
                    line = [all_near_pt[clave], min_pos]
                    ipd[clave] = [line, dist]
                    int_keys.append(clave2)
                    same_inter[clave]=int_keys

    # Distance and not intersecction points for gb that doesn't have:
    for gbid, value in ipd.items():
        if gbid not in location_dic.keys():
            print(location_dic.get(gbid))
            #start=location_dic.get()
            #end=
            #check.min_distance_from_center(center, lin)

    return ipd, pred_lines_dic, same_inter


def near_point(location_dic,center,radi): # FIX IT
    gb_start=[]
    gb_end=[]
    gb_id=location_dic.keys()

    for gbs in location_dic.values():
        gb_start.append(gbs[0])
        gb_end.append(gbs[1])

    pred_lines=[]
    for gb_s, gb_e in zip(gb_start,gb_end):
        x1,y1,x2,y2=gb_s[0],gb_s[1],gb_e[0],gb_e[1]
        inter_points = check.circle_line_segment_intersection(center, radi, gb_s, gb_e)
        inter_point_within=check.circle_line_segment_intersection(center, radi, gb_s, gb_e , full_line=False)
        # Boundary that is defined inside the void and it have two possible continuity, select the longest contin.
        if len(inter_point_within)==0:
            cont_distances=[]
            x_mid_point=(x1+x2)/2
            y_mid_point=(y1+y2)/2
            for cont in inter_points:
                c_d=np.sqrt((x_mid_point - cont[0]) ** 2 + (y_mid_point - cont[1]) ** 2)
                cont_distances.append(c_d)
            ii=cont_distances.index(min(cont_distances))
            inter_point_within.append(inter_points[ii])

        for pt in inter_points:
            if pt not in inter_point_within:
                d_gb_s=np.sqrt((x1 - pt[0])**2 + (y1 - pt[1])**2)
                d_gb_e=np.sqrt((x2 - pt[0])**2 + (y2 - pt[1])**2)
                if d_gb_e<d_gb_s:
                    p3=(x2,y2)
                else:
                    p3=gb_s
                pred_lines.append([list(p3),list(pt)])

    all_near_pt={}
    for key,line1 in zip(gb_id,pred_lines):
        dis_value, near_pt = check.min_distance_from_center(list(center), line1)
        all_near_pt[key]=[near_pt, dis_value]

    return all_near_pt


def intersection_dic_test(gb_start,gb_end,center,radi): # FIX IT - LOOK 'intersection_dic
    """
    :param gb_start: All start point of the grain boundary
    :param gb_end: All end point of the grain boundary
    :param center: Center of the void []
    :param radi: Radio of the void
    :return: ipd: dictionary with {tag of the gb and value [x,y],l} where x and y are the coordinates of the first
    intersection between the other supposed continuity of the gb inside the void and l is distance of it
    supposed continuity
    """
    pred_lines=[]
    iii=0
    for gb_s, gb_e in zip(gb_start,gb_end):
        x1,y1,x2,y2=gb_s[0],gb_s[1],gb_e[0],gb_e[1]
        inter_points = check.circle_line_segment_intersection(center, radi, gb_s, gb_e)
        inter_point_within=check.circle_line_segment_intersection(center, radi, gb_s, gb_e , full_line=False)

        # Boundary that is defined inside the void and it have two possible continuity, select the longest contin.
        if len(inter_point_within)==0:
            cont_distances=[]
            x_mid_point=(x1+x2)/2
            y_mid_point=(y1+y2)/2
            for cont in inter_points:
                c_d=np.sqrt((x_mid_point - cont[0]) ** 2 + (y_mid_point - cont[1]) ** 2)
                cont_distances.append(c_d)
            ii=cont_distances.index(min(cont_distances))
            #print(inter_points[ii])
            inter_point_within.append(inter_points[ii])

        for pt in inter_points:
            if pt not in inter_point_within:
                d_gb_s=np.sqrt((x1 - pt[0])**2 + (y1 - pt[1])**2)
                d_gb_e=np.sqrt((x2 - pt[0])**2 + (y2 - pt[1])**2)
                if d_gb_e<d_gb_s:
                    p3=(x2,y2)
                else:
                    p3=gb_s
                pred_lines.append([list(p3),list(pt)])
        iii=iii+1

    #inter_points_dic={}
    intersection={}
    all_min_position=[]
    all_near_pt={}
    for j,line1 in enumerate(pred_lines):
        dis_value, near_pt = check.min_distance_from_center(list(center), line1)
        int_points = []
        l = []
        for line2 in pred_lines:
            if line1!=line2:
                if check.l_intersection(line1, line2):
                    interserction_point = check.l_intersection(line1, line2)
                    long = np.sqrt((near_pt[0] - interserction_point[0]) ** 2 + (near_pt[1] - interserction_point[1]) ** 2)
                    int_points.append(interserction_point)
                    l.append(long)
        #inter_points_dic[j] = [int_points, l]
        if len(l)>0:
            index=l.index(min(l))
            min_position=int_points[index]
            intersection[j]=[min_position, min(l)]
            all_min_position.append(min_position)
        all_near_pt[j]=near_pt

    ipd={}
    for i, (clave, valor) in enumerate(intersection.items()):
        min_pos=valor[0]
        dist=valor[1]
        counter = all_min_position.count(min_pos)
        values = np.array(all_min_position)
        ii = np.where(values == min_pos)[0]

        if counter>1:
            line=[all_near_pt[i],min_pos]
            ipd[clave]=[line,dist]
        #elif counter>2:
            #line=[all_near_pt[i],min_pos]
            #ipd[clave]=[line,dist]
    return ipd