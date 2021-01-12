import pandas as pd
import os
from os import path

from .voiddetect import *
from .void_parameter import *

def gbvoid_dataset(input_name):
    """
    :param input_name: Name of the file to compute
    :return: pandas dataframe with all the features as X and output Y as void parameter value
    """
    ### get current directory
    pa_current = os.getcwd()

    # define paths for convenience
    pa_pic = pa_current + '/pyinputs/' + input_name + '.jpg'
    pa_txt = pa_current + '/pyinputs/' + input_name + '.txt'
    pa_selected = pa_current + '/output/' + input_name + '/selected.txt'

    ### Read data from text file
    gbdata = np.genfromtxt(pa_txt)
    selected_data = np.genfromtxt(pa_selected)

    ### Selected data
    selected=selected_data[:,0]
    vp=selected_data[:,1]

    # define maximum void area as a multiple of average grain size (last number is factor of multiplication)
    # Find dimensions for picture
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    maxarea = width * height / np.amax(gbdata[:, 20]) * 2.5
    centers, radii, vheight, voidimage, drawing = findvoid(pa_pic, input_name, maxarea)

    # SIGMA VALUE - FROM TXT FILES
    energy_data=[]
    for gb in range(gbdata.shape[0]):
        pa_energy = pa_current + '/energy_output/' + input_name + '/' + 'en_' + str(gb) + '.ref'
        if path.exists(pa_energy) is True:
            en=np.genfromtxt(pa_energy)[1]
            energy=[en]
        else:
            energy=[0]
        energy_data.append(energy)
    gbdata= np.append(gbdata,energy_data, axis=1)

    void_data=[]
    for gb1 in range(gbdata.shape[0]):
        if gb1 in selected:
            void=[1]
        else:
            void=[0]
        void_data.append(void)

    gbdata = np.append(gbdata, void_data, axis=1)

    X_void=pd.DataFrame(gbdata)
    Y_void=np.zeros(len(gbdata))

    sel_i=0
    for i, gbinfo in enumerate(gbdata):
        if i in selected:
            Y_void[i]=vp[sel_i]
            sel_i=sel_i+1
        else:
            Y_void[i]=0

    X_void['Void']=Y_void
    void_dataset=X_void
    return void_dataset