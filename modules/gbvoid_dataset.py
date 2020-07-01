import numpy as np
import pandas as pd
import os


# Custom modules
from modules import voiddetect as vd
from modules import select_voidboundaries as sel

def gbvoid_dataset(input_name):

    ### get current directory
    pa_current = os.getcwd()
    pa_parent = os.path.dirname(pa_current)

    # define paths for convenience
    pa_pic = pa_current + '/pyinputs/' + input_name + '.jpg'
    pa_txt = pa_current + '/pyinputs/' + input_name + '.txt'
    pa_selected = pa_current + '/output/' + input_name + '/' + 'selected.txt'

    ### Read data from text file
    gbdata = np.genfromtxt(pa_txt)
    selected_data = np.genfromtxt(pa_selected)

    X_void=pd.DataFrame(gbdata)


    Y_void=np.zeros(len(gbdata))
    for i, gbinfo in enumerate(gbdata):
        if i in selected_data:
            Y_void[i]=1
        else:
            Y_void[i]=0

    X_void['Void']=Y_void

    #Y_void=pd.DataFrame(Y_void)

    void_dataset=X_void

    return void_dataset