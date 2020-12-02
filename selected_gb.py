import numpy as np
import os.path
import cv2
# Custom modules
from modules import voiddetect as vd
from modules import checkCollision as checkCollision


def selected_gb(name): # Name sample
    ### get current directory
    pa_current = os.environ['PWD']

    # define paths for convenience
    pa_pic = pa_current + '/pyinputs/' + name + '.jpg'
    pa_txt = pa_current + '/pyinputs/' + name + '.txt'

    ## Input data
    gbdata = np.genfromtxt(pa_txt)
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

    image = 255 * np.ones(shape=[drawing.shape[0], drawing.shape[1], 3], dtype=np.uint8)
    ### Create directory if it does not exist already: CREATE DIRECTORY FOR OUTPUTS
    pathout = pa_current + '/output/' + name     # Output path
    os.system('mkdir -p ' + pathout)

    infile = '/selected.txt'  # Name and loc of output txt
    fout = open(pathout + infile, 'w')  # .txt location

    for k, _ in enumerate(endptsx):
        start_point = (np.int64(width_factor*staptsx[k]), np.int64(height_factor*staptsy[k]))
        end_point = (np.int64(width_factor*endptsx[k]), np.int64(height_factor*endptsy[k]))
        thickness = 2
        image = cv2.line(image, start_point, end_point, (245, 245, 245), thickness)
    for l, center in enumerate(centers):
        cv2.circle(image, center, 3, (255, 0, 0), -1)
        cv2.circle(image, center, int(radii[l]), (0, 0, 255), 3)
        cv2.putText(image, str(l), center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)

    for i, center in enumerate(centers):  # Centers
        for j, _ in enumerate(endptsx):

            x_s = np.int64(width_factor * staptsx[j])
            y_s = np.int64(height_factor * staptsy[j])
            x_e = np.int64(width_factor * endptsx[j])
            y_e = np.int64(height_factor * endptsy[j])
            s_p = (np.int64(x_s), np.int64(y_s))
            e_p = (np.int64(x_e), np.int64(y_e))
            thickness = 4
            if checkCollision.checkCollision(x_s, x_e, y_s, y_e, center[0], center[1], radii[i], 1) is True:
                fout.write(str(j))
                fout.write('\n')
                image = cv2.line(image, s_p, e_p, (255, 0, 0), thickness)

    fout.close()
    #cv2.imwrite(os.path.join(pathout, name + '_mydetec.png'), image)
    #cv2.imshow(name, image)
    #cv2.waitKey(0)


inputs = ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
          '2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009',
          '3_001', '3_002', '3_003', '3_004', '3_005', '3_006', '3_007', '3_008', '3_009', '3_010',
          '4_001', '4_002', '4_003', '4_004', '4_005', '4_007', '4_008', '4_009',
          '5_001', '5_002', '5_003', '5_004', '5_005', '5_006', '5_007', '5_008', '5_009', '5_010', '5_011',
          '6_001', '6_002', '6_003', '6_004', '6_005', '6_006', '6_007', '6_008', '6_009', '6_010']
for input in inputs:
    selected_gb(input)