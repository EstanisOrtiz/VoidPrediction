import numpy as np
import os.path
# Custom modules
from modules import voiddetect as vd
from modules import checkCircle as check
from modules import void_parameter as vdpr

def selected_gb(name): # Name sample
    """
    Return output/[input sample]/selected.txt with the values of
    the new selected grain boundary position for the input sample.

    The selected grain boundary are detected via the checkCollision module.
    It disregard the grain boundary relevence into the void.
    """
    ### get current directory
    pa_current = os.environ['PWD']

    # define paths for convenience
    pa_pic = pa_current + '/pyinputs/' + name + '.jpg'
    pa_txt = pa_current + '/pyinputs/' + name + '.txt'

    ## Input data
    gbdata = np.genfromtxt(pa_txt)
    pa_selected_old = pa_current + '/saboutputs/' + name + '/selected.txt'
    selected_data_old = np.genfromtxt(pa_selected_old)
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

    sel=[]
    dist=[]
    void_id=[]

    for i, center in enumerate(centers):  # Centers
        for j, _ in enumerate(endptsx):
            x_s = np.int64(width_factor * staptsx[j])
            y_s = np.int64(height_factor * staptsy[j])
            x_e = np.int64(width_factor * endptsx[j])
            y_e = np.int64(height_factor * endptsy[j])

            if check.checkCollision(x_s, x_e, y_s, y_e, center[0], center[1], radii[i]) is True:
                sel.append(j)
                d=check.checkDist(x_s, x_e, y_s, y_e, center[0], center[1], radii[i])
                dist.append(d)
                void_id.append(i)

    return sel, dist, void_id


### RUN FUNCTION
inputs = ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
          '2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009',
          '3_001', '3_002', '3_003', '3_004', '3_005', '3_006', '3_007', '3_008', '3_009', '3_010',
          '4_001', '4_002', '4_003', '4_004', '4_005', '4_007', '4_008', '4_009',
          '5_001', '5_002', '5_003', '5_004', '5_005', '5_006', '5_007', '5_008', '5_009', '5_010', '5_011',
          '6_001', '6_002', '6_003', '6_004', '6_005', '6_006', '6_007', '6_008', '6_009', '6_010']

#inputs=['1_001']

# Create the selected.txt
for input in inputs:
    pa_current = os.environ['PWD']
    pa_parent = os.path.dirname(pa_current)
    pa_pic = pa_current + '/pyinputs/' + input + '.jpg'
    pa_selected = pa_current + '/output/' + input + '/selected.txt'
    pa_txt = pa_current + '/pyinputs/' + input + '.txt'

    ### Read data from text file
    gbdata = np.genfromtxt(pa_txt)
    selected, dist, void_id = selected_gb(input)
    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    # define maximum void area as a multiple of average grain size (last number is factor of multiplication)
    maxarea = width * height / np.amax(gbdata[:, 20]) * 2.5

    centers, radii, vheight, voidimage, drawing = vd.findvoid(pa_pic, input, maxarea)

    void_dic,  min_length, dis_par = vdpr.void_parameter(gbdata, selected, dist, void_id, centers, drawing)

    # void_dic: Key=selected boundary & Value=Void Parameter.

    ### Create directory if it does not exist already: CREATE DIRECTORY FOR OUTPUTS
    pathout = pa_current + '/output/' + input     # Output path
    os.system('mkdir -p ' + pathout)
    infile = '/selected.txt'            # Name and loc of output txt
    fout = open(pathout + infile, 'w')  # .txt location

    fout.write('# Column 1:   Selected grain boundary location of the input sample\n')
    fout.write('# Column 2:   Void parameter value\n')
    fout.write('# Column 3:   Distance from the grain boundary to the void\n')
    fout.write('# Column 4:   Void ID\n')
    fout.write('# Column 5:   Sorted GB by distance from the center of the void\n\n')


    for j, sele in enumerate(selected):
        vp=void_dic.get(sele)
        sorted_dis=dis_par.get(sele)
        if sorted_dis==None:
            sorted_dis=0
        fout.write(str(sele)+'\t'+str(vp)+'\t'+str(format(dist[j], '.15f'))+'\t'+str(void_id[j])+'\t'+str(sorted_dis))
        fout.write('\n')
    fout.close()
    print('Selected file for ', input, 'is DONE')
