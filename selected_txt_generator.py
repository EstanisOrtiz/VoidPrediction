### RUN FUNCTION
import numpy as np
import os.path
# Custom modules
from modules import void_parameter as vdpr
from modules import selected_gb as selgb
from modules import voiddetect as vd

inputs = ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
          '2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009',
          '3_001', '3_002', '3_003', '3_004', '3_005', '3_006', '3_007', '3_008', '3_009', '3_010',
          '4_001', '4_002', '4_003', '4_004', '4_005', '4_007', '4_008', '4_009',
          '5_001', '5_002', '5_003', '5_004', '5_005', '5_006', '5_007', '5_008', '5_009', '5_010', '5_011',
          '6_001', '6_002', '6_003', '6_004', '6_005', '6_006', '6_007', '6_008', '6_009', '6_010']

#inputs=['1_003']

# Create the selected.txt
for input in inputs:
    pa_current = os.environ['PWD']
    pa_parent = os.path.dirname(pa_current)
    pa_pic = pa_current + '/pyinputs/' + input + '.jpg'
    pa_selected = pa_current + '/output/' + input + '/selected.txt'
    pa_txt = pa_current + '/pyinputs/' + input + '.txt'

    ### Read data from text file
    gbdata = np.genfromtxt(pa_txt)
    selected, dist, void_id, pt3= selgb.selected_gb(input)



    width = np.amax(gbdata[:, 17])
    height = np.amax(gbdata[:, 18])
    # define maximum void area as a multiple of average grain size (last number is factor of multiplication)
    maxarea = width * height / np.amax(gbdata[:, 20]) * 2.5

    centers, radii, vheight, voidimage, drawing = vd.findvoid(pa_pic, input, maxarea)

    void_dic,  min_length, dis_par, ipd_total, pred_lines,same_inter_total = vdpr.void_parameter(gbdata, selected,dist,void_id,centers,radii,drawing)

    prox_par=vdpr.proximity_parameter(gbdata, selected, void_id, centers, radii, drawing, ipd_total,void_dic)
    # void_dic: Key=selected boundary & Value=Void Parameter.

    ### Create directory if it does not exist already: CREATE DIRECTORY FOR OUTPUTS
    pathout = pa_current + '/output/' + input     # Output path
    os.system('mkdir -p ' + pathout)
    infile = '/selected.txt'            # Name and loc of output txt
    fout = open(pathout + infile, 'w')  # .txt location

    fout.write('# Column 1:    Selected grain boundary location of the input sample\n')
    fout.write('# Column 2:    Void parameter value\n')
    fout.write('# Column 3:    Distance from the grain boundary to the center void\n')
    fout.write('# Column 4:    Void ID\n')
    fout.write('# Column 5:    Sorted GB by distance from the center of the void\n')
    fout.write('# Column 6-7:  Supposed intersections point of GB with void edge, x and y\n')
    fout.write('# Column 8-9:  Supposed GB junction point\n')
    fout.write('# Column 10:   Reconstructed length of GB continuity\n')
    fout.write('# Column 11:   Proximity parameter.\n\n')

    for j, sele in enumerate(selected):
        vp=void_dic.get(sele)
        p3=pt3.get(sele)
        int_pts=ipd_total.get(sele)
        sorted_dis=dis_par.get(sele)
        prox=prox_par.get(sele)
        # Values without other intesection or is not sorted
        if sorted_dis==None:
            sorted_dis=0
        if int_pts==None:
            int_pts=[[[-1, -1], [-1, -1]], -1]
        length_sup = int_pts[1]
        pt4_x = int_pts[0][1][0]
        pt4_y = int_pts[0][1][1]

        fout.write(str(sele)+'\t'+str(vp)+'\t'+str(format(dist[sele], '.15f'))+'\t'+str(void_id[j])+'\t'+str(sorted_dis))
        fout.write('\t'+str(p3[0])+'\t'+str(p3[1]))
        fout.write('\t'+str(pt4_x)+'\t'+str(pt4_y))
        fout.write('\t' + str(length_sup))
        fout.write('\t' + str(prox))
        fout.write('\n')

    fout.close()
    print('Selected file for ', input, 'is DONE')