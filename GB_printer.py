import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os.path

# Custom modules
from modules import voiddetect as vd
from modules import select_voidboundaries as sel
from modules import checkCollision as checkCollision
from modules import void_parameter as void_parameter_function

# z = int(raw_input('How many files would you like to add?: '))
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
    # lattice = raw_input("\n\nCrystal Structure\nIndicate crystal structure.\nType one of the options fcc/bcc/hcp as shown: ")

    ### get current directory
    pa_current = os.environ['PWD']
    # os.chdir(os.path.dirname(path_current))
    pa_parent = os.path.dirname(pa_current)

    # define paths for convenience
    pa_pic = pa_current + '/pyinputs/' + name + '.jpg'
    pa_txt = pa_current + '/pyinputs/' + name + '.txt'
    pa_selected = pa_current + '/saboutputs/' + name + '/' + 'selected.txt'

    ### Read data from text file
    gbdata = np.genfromtxt(pa_txt)
    selected_data = np.genfromtxt(pa_selected)
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    # define maximum void area as a multiple of average grain size (last number is factor of multiplication)
    maxarea = width * height / np.amax(gbdata[:, 20]) * 2.5

    ### run voiddetect module and return centers and radii of detected voids
    centers, radii, vheight, voidimage, drawing = vd.findvoid(pa_pic, name, maxarea)

    ### Select boundaries in void vicinity  - WRONG VALUES, USE selected_data form saboutputs
    selected = sel.selgb(gbdata, centers, radii)

    ### Starting points
    staptsx = gbdata[:, 15]
    staptsy = gbdata[:, 16]
    #### Ending points
    endptsx = gbdata[:, 17]
    endptsy = gbdata[:, 18]
    mis_angle = gbdata[:,6]
    trace = gbdata[:,14]
    # Find dimensions for picture
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    # Column 20-21: IDs of right hand and left hand grains
    lhgrain=gbdata[:, 19]
    rhgrain=gbdata[:, 20]

    #ratio = height / vheight

    #centers = np.asarray(centers) * ratio * 1.054
    #radii = np.asarray(radii) * ratio

    # Blank image
    height_factor = drawing.shape[0]/np.int64(height)
    width_factor = drawing.shape[1]/np.int64(width)
    image_void=255 * np.ones(shape=[drawing.shape[0], drawing.shape[1], 3], dtype=np.uint8)
    image_check =255 * np.ones(shape=[drawing.shape[0], drawing.shape[1], 3], dtype=np.uint8)
    image = 255 * np.ones(shape=[drawing.shape[0], drawing.shape[1], 3], dtype=np.uint8)

    for i, _ in enumerate(endptsx):
        start_point = (np.int64(width_factor*staptsx[i]), np.int64(height_factor*staptsy[i]))
        end_point = (np.int64(width_factor*endptsx[i]), np.int64(height_factor*endptsy[i]))
        thickness = 2
        if i in selected_data:
            color = (0 , 255, 0)
        else:
            color = (0,0,0)
        image = cv2.line(image, start_point, end_point, color, thickness)
        image_void = cv2.line(image_void, start_point, end_point, (245, 245, 245), thickness)


    for i, center in enumerate(centers):
        cv2.circle(image, center, 3, (255, 0, 0), -1)
        cv2.circle(image, center, int(radii[i]), (0, 0, 255), 3)
        cv2.putText(image ,str(i), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)

    void_dicc = {}
    void_parameter_dicc = {}

    for i, center in enumerate(centers): #Centers
        print('-----', str(i), '---------')
        count = 0
        number_of_gb_in_void = 0
        for j, _ in enumerate(endptsx):
            thickness = 4
            x_s = np.int64(width_factor * staptsx[j])
            y_s = np.int64(height_factor * staptsy[j])
            x_e = np.int64(width_factor * endptsx[j])
            y_e = np.int64(height_factor * endptsy[j])
            s_p = (np.int64(x_s), np.int64(y_s))
            e_p = (np.int64(x_e), np.int64(y_e))

            if checkCollision.checkCollision(x_s, x_e, y_s, y_e, center[0], center[1], radii[i], 1) is True:
                image_check = cv2.line(image_check, s_p, e_p, (255,0,0), thickness)
                if j in selected_data:
                    color = (0, 255, 0)
                    number_of_gb_in_void += 1
                else:
                    color = (255, 153, 255)
                    print(j)
                image_void = cv2.line(image_void, s_p, e_p, color, thickness)
            elif checkCollision.checkCollision(x_s, x_e, y_s, y_e, center[0], center[1], radii[i], 1) is False and j in selected_data:
                    color = (255, 255, 0)
                    print("-", str(j), '-')
                    image_void = cv2.line(image_void, s_p, e_p, color, thickness)
            cv2.circle(image_void, center, 3, (255, 0, 0), -1)
            cv2.circle(image_void, center, int(radii[i]), (0, 0, 255), 3)

        if number_of_gb_in_void!=0:
            void_parameter=round((2*(1/number_of_gb_in_void)), 2)
            if void_parameter>1:
                void_parameter=1
            elif void_parameter<0.5:
                void_parameter=0.25
        else:
            void_parameter=0

        cv2.putText(image_void, str(i), center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        parameter_center=(center[0],center[1]+50)
        cv2.putText(image_void, str(void_parameter), parameter_center, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)

        void_parameter_dicc[i]= void_parameter
        void_dicc[i] = number_of_gb_in_void
    # print(void_parameter_dicc) # Num Void and Void Parameter
    # print(void_dicc)  # Num Void and Number of gb inside
    # test_function=void_parameter_function.void_parameter(gbdata, selected_data, centers, radii, drawing)
    # print(test_function)

    # SAVE THE PICTURES
    os.system('mkdir -p ' + pa_current + '/output/' + name)
    pa_image = pa_current + '/output/' + name
    #cv2.imwrite(os.path.join(pa_image, name + '_' + format(len(centers)) + '.png'), image)
    #cv2.imwrite(os.path.join(pa_image, name + '_voids' + '.png'), voidimage)
    #cv2.imwrite(os.path.join(pa_image, name + '_drawing' + '.png'), drawing)
    #cv2.imwrite(os.path.join(pa_image, str(name) + '_selected' + '.png'), image_void)

    # SHOW PICTURE
    cv2.imshow(name, image_void)
    cv2.imshow('CHECK', image_check)
    cv2.waitKey(0)
    break