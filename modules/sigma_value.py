import numpy as np
import os.path
import time

start_time = time.time()

def sigma_value(name): # Name sample
    ## Input data
    pa_current = os.getcwd()
    pa_txt = pa_current + '/pyinputs/' + name + '.txt'
    gbdata = np.genfromtxt(pa_txt)
    Eul1 = gbdata[:, (0, 1, 2)]  # RAD
    Eul2 = gbdata[:, (3, 4, 5)]  # RAD
    trace = gbdata[:, 14] # Degrees


    ### Create directory if it does not exist already: CREATE DIRECTORY FOR OUTPUTS
    pathin = pa_current + '/energy_input/' + name     # Input path, .in files
    pathout = pa_current + '/energy_output/' + name  # Output path, .ref files
    os.system('mkdir -p ' + pathin)
    os.system('mkdir -p ' + pathout)
    for i in range(len(trace)): #i: gb pos.
    #while i < len(gbdata):
        #### Create temporary input file for convenience
        infile = '/en_' + str(i) + '.in'  # Name of input file
        fout = open(pathin + infile, 'w')  # .in location

        fout.write('#$Energy2D\n$CSL\n$a 3.217\n$Sigma1 0.1\n$Sigma2 $Sigma1\n')
        fout.write('$Epsilon 0.25\n$Order1 64\n$Order2 $Order1\n\n$AlphaX1 $a\n$AlphaY1 $a\n$AlphaZ1 $a\n\n')
        fout.write('$X1 0. 0.5*$a 0.5*$a 0.5*$a 0.5*$a -0.5*$a -0.5*$a -0.5*$a -0.5*$a\n')
        fout.write('$Y1 0. 0.5*$a 0.5*$a -0.5*$a -0.5*$a 0.5*$a 0.5*$a -0.5*$a -0.5*$a\n')
        fout.write('$Z1 0. 0.5*$a -0.5*$a 0.5*$a -0.5*$a 0.5*$a -0.5*$a 0.5*$a -0.5*$a\n')
        fout.write('\n$AlphaX2 $AlphaX1\n$AlphaY2 $AlphaY1\n$AlphaZ2 $AlphaZ1\n')
        fout.write('$X2 $X1\n$Y2 $Y1\n$Z2 $Z1\n\n$Tolerence 1E-16\n\n')

        ### No rotation, only tilt angle (same as misorientation angle) sigma value
        #fout.write('$ThetaRotX1 1\n$ThetaRotX2 1\n$ThetaMin ' + str(misor) +'\n$ThetaMax ' + str(misor) +'\n$DTheta 0.1\n')
        fout.write('$ThetaRotX1 1\n$ThetaRotX2 1\n$ThetaMin 0.0\n$ThetaMax 0.0\n$DTheta 0.1\n')

        fout.write('\n$BungeEuler1 ' + str(np.degrees(Eul1[i, 0])) + ' ' + str(np.degrees(Eul1[i, 1])) + ' ' + str(np.degrees(Eul1[i, 2])) + '\n')
        fout.write('$BungeEuler2 ' + str(np.degrees(Eul2[i, 0])) + ' ' + str(np.degrees(Eul2[i, 1])) + ' ' + str(np.degrees(Eul2[i, 2])) + '\n')
        fout.write('$TraceAngle ' + str(trace[i]) + '\n')

        outfile = str(pathout)+ '/en_' + str(i) + '.ref'
        fout.write('\n$OutFile ' + str(outfile))
        #fout.write('\n$OutFile output.ref')

        #fout.write('$RotAxes1 z x z x\n$Rots1  ($phi2_1) ($Phi_1) ($phi1_1) 90\n')
        #fout.write('$RotAxes2 z x z x\n$Rots2  ($phi2_2) ($Phi_2) ($phi1_2) 90\n')

        ## SAVE THE INPUT
        fout.close()
        print('./bin/wield ' + str(pathin) + str(infile) +' -v -n 2')
        os.system('./bin/wield ' + str(pathin) + str(infile) +' -v -n 2')
        #os.system('./bin/wield tests/energy_input/'+ str(name) + str(infile)+' -v -n 2')
        print(name, 'Boundary', i, '/', len(gbdata))

"""
inputs = ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
          '2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009',
          '3_001', '3_002', '3_003', '3_004', '3_005', '3_006', '3_007', '3_008', '3_009', '3_010',
          '4_001', '4_002', '4_003', '4_004', '4_005', '4_007', '4_008', '4_009',
          '5_001', '5_002', '5_003', '5_004', '5_005', '5_006', '5_007', '5_008', '5_009', '5_010', '5_011',
          '6_001', '6_002', '6_003', '6_004', '6_005', '6_006', '6_007', '6_008', '6_009', '6_010']
"""
inputs=['1_001']

for name in inputs:
    sigma_value(name)

print ("It took", time.time() - start_time, "to finish")