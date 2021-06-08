import pandas as pd
import os
from os import path
import numpy as np

# if runs from terminal delete the dot (.)
from .voiddetect import *
#from .void_parameter import *
from .checkCircle import *

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

    # Starting points
    staptsx = gbdata[:, 15]
    staptsy = gbdata[:, 16]
    # Ending points
    endptsx = gbdata[:, 17]
    endptsy = gbdata[:, 18]
    mis_angle = gbdata[:,6]

    ### Selected data
    selected=selected_data[:,0]
    vp=selected_data[:,1]
    distance = selected_data[:, 2]
    void_id = selected_data[:, 3]
    x_j=selected_data[:,7]
    y_j=selected_data[:,8]
    l_pred=selected_data[:,9]
    prox_par = selected_data[:, 10]

    # define maximum void area as a multiple of average grain size (last number is factor of multiplication)
    # Find dimensions for picture
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    maxarea = width * height / np.amax(gbdata[:, 20]) * 2.5
    centers, radii, vheight, voidimage, drawing = findvoid(pa_pic, input_name, maxarea)
    height_factor = drawing.shape[0]/np.int64(height)
    width_factor = drawing.shape[1]/np.int64(width)

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
    gbdata= np.append(gbdata, energy_data, axis=1)

    # Generate Dicc for selected features
    dis_dic={}
    void_id_dic={}
    x_j_dic={}
    y_j_dic={}
    l_pred_dic={}
    junction_dic={}
    vp_dic={}
    prox={}

    for id, dis, vid, xj, yj,lp,vpp,px in zip(selected,distance,void_id,x_j,y_j,l_pred,vp,prox_par):
        dis_dic[id]=dis
        void_id_dic[id]=vid
        x_j_dic[id]= xj
        y_j_dic[id] = yj
        l_pred_dic[id]=lp
        vp_dic[id]=vpp
        prox[id] = px

    for id1 in selected:
        if x_j_dic.get(id1)>0 or y_j_dic.get(id1)>0:
            x_count=np.count_nonzero(np.around(x_j,6) == round(x_j_dic.get(id1),6))
            y_count=np.count_nonzero(np.around(y_j,6) == round(y_j_dic.get(id1),6))
            if x_count==y_count and x_count>=1:
                junction_dic[id1]=y_count
        else:
            junction_dic[id1] = 0

    dist=[]
    vid_all=[]
    xj_all=[]
    yj_all=[]
    lp_all=[]
    junc_all=[]
    prox_all=[]

    for gb1 in range(gbdata.shape[0]):
        #dist.append(dis_dic.get(gb1))
        gb_s = [staptsx[gb1], staptsy[gb1]]
        gb_e = [endptsx[gb1], endptsy[gb1]]
        if gb1 in selected:
            d=[dis_dic.get(gb1)]
            vid_a=[void_id_dic.get(gb1)]
            xj_a=[x_j_dic.get(gb1)]
            yj_a=[y_j_dic.get(gb1)]
            lp_a=[l_pred_dic.get(gb1)]
            junc_a=[junction_dic.get(gb1)]
            prox_a=[prox.get(gb1)]
        else:
            d=[min_dis_allgb_centers(centers, gb_s, gb_e, width_factor,height_factor)]
            vid_a=[-1]
            xj_a=[-1]
            yj_a=[-1]
            lp_a=[-1]
            junc_a=[-1]
            prox_a=[-1]

        dist.append(d)
        vid_all.append(vid_a)
        xj_all.append(xj_a)
        yj_all.append(yj_a)
        lp_all.append(lp_a)
        junc_all.append(junc_a)
        prox_all.append(prox_a)

    #gbdata = np.append(gbdata, dist, axis=1)

    selec_feat=np.concatenate((dist,vid_all,xj_all,yj_all,lp_all,junc_all,prox_all), axis=1)
    gbdata = np.concatenate((gbdata, selec_feat), axis=1)

    #gbdata = np.append(gbdata,selec_feat, axis=1)

    # VOID
    void_data=[]
    for gb2 in range(gbdata.shape[0]):
        if gb2 in selected:
            void=[1]
        else:
            void=[0]
        void_data.append(void)
    gbdata = np.append(gbdata, void_data, axis=1)

    X_void=pd.DataFrame(gbdata)
    Y_void=np.zeros(len(gbdata))

    for i, gbinfo in enumerate(gbdata):
        if i in selected:
            Y_void[i]=vp_dic[i]
        else:
            Y_void[i]=0

    X_void['Void']=Y_void
    void_dataset=X_void
# Merge all the samples remaning the sample tag:

#pd.concat([all samples as list], keys=[sample tags])

    return void_dataset