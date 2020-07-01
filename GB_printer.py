import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os.path

# Custom modules
from modules import voiddetect as vd
from modules import select_voidboundaries as sel

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

    ### Select boundaries in void vicinity
    selected = sel.selgb(gbdata, centers, radii)

    ### Starting points
    staptsx = gbdata[:, 15]
    staptsy = gbdata[:, 16]
    #### Ending points
    endptsx = gbdata[:, 17]
    endptsy = gbdata[:, 18]
    # mis_angle = gbdata[:,6]
    # Find dimensions for picture
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    # Column 20-21: IDs of right hand and left hand grains
    lhgrain=gbdata[:, 19]
    rhgrain=gbdata[:, 20]

    ratio = height / vheight

    #centers = np.asarray(centers) * ratio * 1.0
    #radii = np.asarray(radii) * ratio

    #os.system('mkdir ' + pa_current + '/outputs/' + name)

    # Blank image
    height_factor = drawing.shape[0]/np.int64(height)
    width_factor = drawing.shape[1]/np.int64(width)

    image = 255 * np.ones(shape=[drawing.shape[0], drawing.shape[1], 3], dtype=np.uint8)

    for i, _ in enumerate(endptsx):
        start_point = (np.int64(width_factor*staptsx[i]), np.int64(height_factor*staptsy[i]))
        end_point = (np.int64(width_factor*endptsx[i]), np.int64(height_factor*endptsy[i]))
        if i in selected_data:
        # if lhgrain[i] in selected or rhgrain[i] in selected:
            thickness = 4
            color = (0 , 255, 0)
        else:
            thickness = 2
            color = (0,0,0)
        image = cv2.line(image, start_point, end_point, color, thickness)

    for i, center in enumerate(centers):
        cv2.circle(image, center, 3, (255, 0, 0), -1)
        cv2.circle(image, center, int(radii[i]), (0, 0, 255), 3)

    #cv2.imshow(name + ' BC', image)chispeante

    os.system('mkdir '+pa_current+'/output/'+name)

    pa_image=pa_current+'/output/'+name
    cv2.imwrite(os.path.join(pa_image, name+'_'+format(len(centers))+'.png'), image)
    cv2.imwrite(os.path.join(pa_image, name + '_voids' + '.png'), voidimage)
    cv2.imwrite(os.path.join(pa_image, name + '_drawing' + '.png'), drawing)

    #np.savetxt((pa_image + '/selected.txt'), selected_data)

    #vis = np.concatenate((image, voidimage), axis=0)
    #cv2.imshow(name+' mix', drawing)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


##### Plot background picture
### Comment/Uncomment as needed
# fig, ax = plt.subplots(1)
# im = plt.imread(pa_pic)
# implot = plt.imshow(im, origin='lower', extent=[0, width, 0, height], aspect='equal')

####Plot points
# IniPlot = zip(staptsx, staptsy, endptsx, endptsy)
# for tuple in IniPlot:
# plt.plot([tuple[0], tuple[2]], [tuple[1], tuple[3]],'#000000')

# for tuple in zip(centers, radii):
# circ = Circle(tuple[0], tuple[1], color='#FFFF00', linewidth=3, fill=False)
# ax.add_patch(circ)

# for row in selected:
# plt.plot([staptsx[row], endptsx[row]], [staptsy[row], endptsy[row]], color='#FF0000', linewidth= 2)
#### Save file (Comment/Uncomment as needed)
# plt.savefig(pa_current+'/outputs/detectpics/'+name+'.png')# , bbox_inches='tight')
# fig.clf()
#### Show plot (Comment/Uncomment as needed)
# plt.show()
### End plot background picture

