import cv2
import numpy as np
import os.path
import math

# Custom modules
from modules import voiddetect as vd
from modules import void_parameter as vdpr
from modules import checkCircle as check
from modules import selected_gb as selgb

## Gather inputs
inputs = ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
          '2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009',
          '3_001', '3_002', '3_003', '3_004', '3_005', '3_006', '3_007', '3_008', '3_009', '3_010',
          '4_001', '4_002', '4_003', '4_004', '4_005', '4_007', '4_008', '4_009',
          '5_001', '5_002', '5_003', '5_004', '5_005', '5_006', '5_007', '5_008', '5_009', '5_010', '5_011',
          '6_001', '6_002', '6_003', '6_004', '6_005', '6_006', '6_007', '6_008', '6_009', '6_010']

#inputs=['1_003']

saver=1     # 1 - Save the figures; 0 - Show the figures

for name in inputs:
    print(name)
    lattice = 'bcc'

    ### get current directory
    pa_current = os.environ['PWD']
    # os.chdir(os.path.dirname(path_current))
    pa_parent = os.path.dirname(pa_current)

    # define paths for convenience
    pa_pic = pa_current + '/pyinputs/' + name + '.jpg'
    pa_txt = pa_current + '/pyinputs/' + name + '.txt'
    pa_selected_old = pa_current + '/saboutputs/' + name + '/selected.txt'
    pa_selected = pa_current + '/output/' + name + '/selected.txt'

    ### Read data from text file
    gbdata = np.genfromtxt(pa_txt)
    selected_data = np.genfromtxt(pa_selected)
    selected_data_old = np.genfromtxt(pa_selected_old)

    # define maximum void area as a multiple of average grain size (last number is factor of multiplication)
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    maxarea = width * height / np.amax(gbdata[:, 20]) * 2.5

    ### run voiddetect module and return centers and radii of detected voids
    centers, radii, vheight, voidimage, drawing = vd.findvoid(pa_pic, name, maxarea)

    # Starting points
    staptsx = gbdata[:, 15]
    staptsy = gbdata[:, 16]
    # Ending points
    endptsx = gbdata[:, 17]
    endptsy = gbdata[:, 18]
    mis_angle = gbdata[:,6]
    trace = gbdata[:,14]
    # Find dimensions for picture
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    ### Selected data
    selected=selected_data[:,0]
    distance=selected_data[:,2]
    void_id=selected_data[:,3]
    p3_x=selected_data[:,5]
    p3_y=selected_data[:,6]
    prox_par=selected_data[:,10]

    selected_selgb, dist_selgb, void_id_selgb, pt3_selgb = selgb.selected_gb(name)

    # Distances from txt to dictionary:
    distance_dic={}
    prox_par_dic={}
    void_id_dic={}
    #pt_int_dic={}
    for gbid, dis, prox, p3x,p3y,vid in zip(selected, distance,prox_par,p3_x,p3_y,void_id):
        distance_dic[gbid]=dis
        prox_par_dic[gbid] = prox
        void_id_dic[gbid]=vid

        #pt_int_dic[gbid]=(int(p3x),int(p3y))
        #if prox!=0:
            #prox_par_dic[gbid]=prox

    dic_void, min_length, dis_par, inter_points_dic, pred_lines,same_inter_total= vdpr.void_parameter(gbdata, selected, distance_dic, void_id, centers, radii, drawing)

    # Blank image
    height_factor = drawing.shape[0]/np.int64(height)
    width_factor = drawing.shape[1]/np.int64(width)

    # Categories gb image, [gray:gb, pink:new selected, green:old selected, orange:small gb]
    image_void = 255 * np.ones(shape=[drawing.shape[0], drawing.shape[1], 3], dtype=np.uint8)
    # Only all selected void gb in blue
    image_check = 255 * np.ones(shape=[drawing.shape[0], drawing.shape[1], 3], dtype=np.uint8)
    # Definitive image.
    image = 255 * np.ones(shape=[drawing.shape[0], drawing.shape[1], 3], dtype=np.uint8)
    #Parameter void - Only for documentation pictures
    image_vp = 255 * np.ones(shape=[drawing.shape[0], drawing.shape[1], 3], dtype=np.uint8)

    for j, _ in enumerate(endptsx): # Grain Boundary
        thickness = 2
        x_s = np.int64(width_factor * staptsx[j])
        y_s = np.int64(height_factor * staptsy[j])
        x_e = np.int64(width_factor * endptsx[j])
        y_e = np.int64(height_factor * endptsy[j])
        s_p = (np.int64(x_s), np.int64(y_s))
        e_p = (np.int64(x_e), np.int64(y_e))
        leng = np.asarray(e_p) - np.asarray(s_p)
        length = np.linalg.norm(leng)

        #if j==500:
            #distan_test_2 = np.sqrt(((x_e - x_s) ** 2) + ((y_e - y_s) ** 2))

        # IMAGE VOID
        if length < min_length and j in selected:  # Too small gb
            color = (0, 140, 255)
        elif j in selected_data_old: # Old code
            color = (0, 255, 0)
        elif j in selected: # New selected gb
            color = (255, 153, 255)
        else:
            color= (245, 245, 245) # Grey
        image_void = cv2.line(image_void, s_p, e_p, color, thickness)

        # IMAGE
        if j in selected and length > min_length:
            color1 = (0, 255, 0)
        #elif j in selected and length < min_length:
            #color1 = (255, 255, 255)  # Blank
        else:
            color1 = (245, 245, 245)
        image = cv2.line(image, s_p, e_p, color1, thickness)

        # IMAGE CHECK
        if j in selected and length>min_length:
            image_check = cv2.line(image_check, s_p, e_p, (255,0,0), 1)
            x_m=(e_p[0]+s_p[0])/2
            y_m=(e_p[1]+s_p[1])/2
            mid_gb = (int(x_m), int(y_m))
            cv2.circle(image_check, mid_gb, 2, (0, 0, 0), -1)
            vp=dic_void[j]
            cv2.putText(image_check, str(vp), mid_gb, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

            image_vp = cv2.line(image_vp, s_p, e_p, (255, 0, 0), 1)

            # Print proximity parameter
            parox=round(prox_par_dic.get(j),2)
            cv2.putText(image_vp, str(parox), mid_gb, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


            if void_id_dic.get(j)==3:
                prox, p3s = check.inside_len(s_p, e_p, centers[3], radii[3],width_factor,height_factor)
                len_org = check.distance(p3s[0], p3s[1])

                for p3 in p3s:
                    if p3[0] > 0 and p3[1] > 0:
                        p3d = tuple(np.array(p3, int))
                        cv2.circle(image_vp, p3d, 1, (0, 0, 0), -1)

            """
            # EXTENDED VOID DRAWING
            index=selected.tolist().index(j)
            v_id=void_id[index]
            for vid in range(0,int(void_id.max()+1)):
                if v_id==vid and p3_x[index]>=0:
                    pt3 = (p3_x[index], p3_y[index])
                    #x1, y1, x2, y2 = s_p[], s_p[sel], e_p[sel], e_p[sel]
                    d_gb_s = np.sqrt((x_s - pt3[0]) ** 2 + (y_s - pt3[1]) ** 2)
                    d_gb_e = np.sqrt((x_e - pt3[0]) ** 2 + (y_e - pt3[1]) ** 2)
                    if d_gb_e < d_gb_s:
                        ptt = (x_e, y_e)
                    else:
                        ptt = (x_s, y_s)
                    pt3_draw = (int(pt3[0]), int(pt3[1]))
                    cv2.line(image_vp, ptt, pt3_draw, (0, 255, 0), 1)
            """

    # Draw Voids
    for i, center in enumerate(centers):
        text_loc=(int(center[0]-radii[i]), int(center[1]-radii[i])-10)
        cv2.circle(image, center, 2, (255, 0, 0), -1)
        cv2.circle(image, center, int(radii[i]), (0, 0, 255), 2)
        cv2.putText(image, str(i), text_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.circle(image_void, center, 3, (255, 0, 0), -1)
        cv2.circle(image_void, center, int(radii[i]), (0, 0, 255), 3)
        cv2.putText(image_void, str(i), text_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.circle(image_check, center, 1, (0, 0, 255), -1)
        cv2.circle(image_check, center, int(radii[i]), (0, 0, 255), 1)
        cv2.putText(image_check, str(i), text_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        cv2.circle(image_vp, center, 1, (0, 0, 255), -1)
        cv2.circle(image_vp, center, int(radii[i]), (0, 0, 255), 1)
        cv2.putText(image_vp, str(i), text_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        """ # Documentation Picture - sample 1_004
        if i==22:
            center1=(center[0]*3, center[1]*3)
            radi=int(radii[i]*3)
            cv2.circle(image_vp, center1, 1, (0, 0, 255), -1)
            cv2.circle(image_vp, center1, radi, (0, 0, 255), 2)
            cv2.putText(image_vp, str(i), text_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        """

    for clave, valor in inter_points_dic.items():
        if dic_void[clave] > 0:              # Skip -1 void paramenter (small gb)
            pt4_x = valor[0][1][0]*width_factor
            pt4_y = valor[0][1][1]*height_factor
            n_pt_x = valor[0][0][0]*width_factor
            n_pt_y = valor[0][0][1]*height_factor

            pt4_draw=(int(pt4_x),int(pt4_y))
            n_draw=(int(n_pt_x),int(n_pt_y))
            l = valor[1]

            cv2.circle(image_vp, pt4_draw, 2, (0, 255, 0), -1)
            cv2.line(image_vp, n_draw, pt4_draw, (0, 255, 0), 1)

            dist=distance_dic.get(clave)
            #cv2.putText(image_vp, str(round(dist,3)), pt4_draw, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    """
    # PRINT THE NEAR POINTS:
    for id, nearpt in near_points.items():
        if id not in inter_points_dic.keys():
            nearpt_draw = (int(nearpt[0][0]), int(nearpt[0][1]))
            dist1=nearpt[1]
            if dic_void[id] > 0:  # Skip -1 void paramenter (small gb)
                cv2.circle(image_vp, nearpt_draw, 2, (0, 255, 0), -1)
                cv2.putText(image_vp, str(round(dist1, 3)), nearpt_draw, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)"""

    for cl1, val1 in pred_lines.items():
        for val2 in val1:
            if cl1 not in inter_points_dic.keys():
                dist1 = distance_dic.get(cl1)
                pt1_v=(int(val2[0][0]),int(val2[0][1]))
                pt2_v=(int(val2[1][0]),int(val2[1][1]))

                # Continuety lines
                #cv2.line(image_vp, pt1_v, pt2_v, (0, 255, 0), 1)
                #cv2.circle(image_vp, pt1_v, 2, (0, 255, 0), -1)
                #cv2.putText(image_vp, str(round(dist1, 2)), pt1_v, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                cv2.circle(image, pt1_v, 2, (0, 255, 255), -1)
                cv2.circle(image_check, pt1_v, 2, (0, 255, 255), -1)


    """ IT WORKS WITH DICTIONARY OF ALL INTERSECTIONS POINTS
    print(inter_points_dic[2790])
    for clave, valor in inter_points_dic.items():
        if dic_void[clave]>0: # Skip -1 void paramenter (small gb)
            for v in valor:
                if v is not None:
                    v_x = np.int64(width_factor * v[0])
                    v_y = np.int64(height_factor * v[1]) # Rescalate
                    valor_check = (int(v_x), int(v_y))
                    cv2.circle(image_vp, valor_check, 2, (0, 255, 255), -1)
    """

    # SAVE THE PICTURES
    if saver==1:
        os.system('mkdir -p ' + pa_current + '/output/' + name)
        pa_image = pa_current + '/output/' + name
        cv2.imwrite(os.path.join(pa_image, name + '_' + format(len(centers)) + '.png'), image)
        cv2.imwrite(os.path.join(pa_image, name + '_voids' + '.png'), voidimage)
        cv2.imwrite(os.path.join(pa_image, name + '_drawing' + '.png'), drawing)
        cv2.imwrite(os.path.join(pa_image, str(name) + '_categories' + '.png'), image_void)
        cv2.imwrite(os.path.join(pa_image, str(name) + '_parameter' + '.png'), image_check)
        cv2.imwrite(os.path.join(pa_image, str(name) + '_vp' + '.png'), image_vp)   # Documentation Picture

    # SHOW PICTURE
    elif saver==0:
        #cv2.imshow('Selected GB', image)
        #cv2.imshow('Selected & Void Parameter', image_check)
        #cv2.imshow('GB Categories', image_void)
        cv2.imshow('Testing', image_vp) # Documentation Picture
        cv2.waitKey(0)

    print('Selected file for ', name, 'is DONE')
