import cv2
import numpy as np
import os.path

# Custom modules
from modules import voiddetect as vd
from modules import void_parameter as vdpr

## Gather inputs
inputs = ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
          '2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009',
          '3_001', '3_002', '3_003', '3_004', '3_005', '3_006', '3_007', '3_008', '3_009', '3_010',
          '4_001', '4_002', '4_003', '4_004', '4_005', '4_007', '4_008', '4_009',
          '5_001', '5_002', '5_003', '5_004', '5_005', '5_006', '5_007', '5_008', '5_009', '5_010', '5_011',
          '6_001', '6_002', '6_003', '6_004', '6_005', '6_006', '6_007', '6_008', '6_009', '6_010']

#inputs=['1_001']

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
    dic_void, min_length, dis_par = vdpr.void_parameter(gbdata, selected, distance, void_id, centers, drawing)
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
    #image_vp = 255 * np.ones(shape=[drawing.shape[0]*3, drawing.shape[1]*3, 3], dtype=np.uint8)

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
        elif j in selected and length < min_length:
            color1 = (255, 255, 255)  # Blank
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

        '''
        # Image test - Documentation Picture - sample 1_004
        void_22=[1151,1166,959,888,1020]
        if j in void_22:
            s_p1=(s_p[0]*3,s_p[1]*3)
            e_p1=(e_p[0]*3,e_p[1]*3)

            image_vp = cv2.line(image_vp, s_p1, e_p1, (255, 0, 0), 2)
            x_m = (e_p1[0] + s_p1[0]) / 2
            y_m = (e_p1[1] + s_p1[1]) / 2
            mid_gb = (int(x_m), int(y_m))
            cv2.circle(image_vp, mid_gb, 2, (0, 0, 0), -2)'''


    # Draw Voids
    for i, center in enumerate(centers):
        text_loc=(int(center[0]-radii[i]), int(center[1]-radii[i])-10)
        cv2.circle(image, center, 3, (255, 0, 0), -1)
        cv2.circle(image, center, int(radii[i]), (0, 0, 255), 3)
        cv2.putText(image, str(i), text_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.circle(image_void, center, 3, (255, 0, 0), -1)
        cv2.circle(image_void, center, int(radii[i]), (0, 0, 255), 3)
        cv2.putText(image_void, str(i), text_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.circle(image_check, center, 1, (0, 0, 255), -1)
        cv2.circle(image_check, center, int(radii[i]), (0, 0, 255), 1)
        cv2.putText(image_check, str(i), text_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        """ # Documentation Picture - sample 1_004
        if i==22:
            center1=(center[0]*3, center[1]*3)
            radi=int(radii[i]*3)
            cv2.circle(image_vp, center1, 1, (0, 0, 255), -1)
            cv2.circle(image_vp, center1, radi, (0, 0, 255), 2)
            cv2.putText(image_vp, str(i), text_loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        """

    # SAVE THE PICTURES
    os.system('mkdir -p ' + pa_current + '/output/' + name)
    pa_image = pa_current + '/output/' + name
    cv2.imwrite(os.path.join(pa_image, name + '_' + format(len(centers)) + '.png'), image)
    cv2.imwrite(os.path.join(pa_image, name + '_voids' + '.png'), voidimage)
    cv2.imwrite(os.path.join(pa_image, name + '_drawing' + '.png'), drawing)
    cv2.imwrite(os.path.join(pa_image, str(name) + '_categories' + '.png'), image_void)
    cv2.imwrite(os.path.join(pa_image, str(name) + '_voidparameter' + '.png'), image_check)
    #cv2.imwrite(os.path.join(pa_image, str(name) + '_vp' + '.png'), image_vp)   # Documentation Picture

    # SHOW PICTURE
    #cv2.imshow('Selected GB', image)
    #cv2.imshow('Selected & Void Parameter', image_check)
    #cv2.imshow('GB Categories', image_void)
    #cv2.imshow('Testing', image_vp) # Documentation Picture
    #cv2.waitKey(0)
