import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os.path

# Custom modules
from modules import voiddetect as vd
# Column 1-3:   right hand average orientation (phi1, PHI, phi2 in radians)
# Column 4-6:   left hand average orientation (phi1, PHI, phi2 in radians)
# Column 7:     Misorientation Angle
# Column 8-10:  Misorientation Axis in Right Hand grain
# Column 11-13: Misorientation Axis in Left Hand grain
# Column 14:    length (in microns)
# Column 15:    trace angle (in degrees)
# Column 16-19: x,y coordinates of endpoints (in microns)
# Column 20-21: IDs of right hand and left hand grains

def void_analysis(name, pa_pic,gbdata, selected_data):

    pa_pic = pa_current + '/pyinputs/' + name + '.jpg'

    ### Read data from text file
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    # define maximum void area as a multiple of average grain size (last number is factor of multiplication)
    maxarea = width * height / np.amax(gbdata[:, 20]) * 2.5

    ### run voiddetect module and return centers and radii of detected voids
    centers, radii, vheight, voidimage, drawing = vd.findvoid(pa_pic, name, maxarea)

    # vheight: Get height of the picture to set up an approximate area (height*height)

    ### Starting points
    staptsx = gbdata[:, 15]
    staptsy = gbdata[:, 16]
    #### Ending points
    endptsx = gbdata[:, 17]
    endptsy = gbdata[:, 18]
    mis_angle = gbdata[:,6]
    trace_angle = gbdata[:,14]
    # Find dimensions for picture
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    # IDs of right hand and left hand grains
    lhgrain=gbdata[:, 19]
    rhgrain=gbdata[:, 20]

    ratio = height / vheight
    num_voids=len(centers)
    num_boundaries=len(gbdata)

    # Void statistics
    void_ratio=(num_voids/num_boundaries)*100
    void_trace = []
    void_Y=np.zeros(len(gbdata))
    for i, gbinfo in enumerate(gbdata):
        if i in selected_data:
            void_trace.append(trace_angle[i])
            void_Y[i]=1
        else:
            void_Y[i]=0

    #os.system('mkdir ' + pa_current + '/outputs/' + name)

    return trace_angle, mis_angle, void_Y

# Column 1-3:   right hand average orientation (phi1, PHI, phi2 in radians)
# Column 4-6:   left hand average orientation (phi1, PHI, phi2 in radians)
# Column 7:     Misorientation Angle
# Column 8-10:  Misorientation Axis in Right Hand grain
# Column 11-13: Misorientation Axis in Left Hand grain
# Column 14:    length (in microns)
# Column 15:    trace angle (in degrees)
# Column 16-19: x,y coordinates of endpoints (in microns)
# Column 20-21: IDs of right hand and left hand grains
