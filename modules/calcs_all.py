import os.path
import math
import numpy as np
from modules import conversions as convs

def calcs_all(name, lattice, gbdata, pa_parent, dim, proc, k):

    print('Calculating energy values')

    path = pa_parent+'/wield/bin'
    os.chdir(path)
    os.system('mkdir '+name)
    Eul1 = gbdata[:,(0,1,2)]
    Eul2 = gbdata[:,(3,4,5)]

    xe1 = gbdata[:, 16]
    ye1 = gbdata[:, 15]
    xe2 = gbdata[:, 18]
    ye2 = gbdata[:, 17]
    i = 0

    ### Matrix to transform coordinates into WIELD default frame.
    Base = ([[1,0,0],[0,0,-1],[0,1,0]])

    if dim == 1:
        while i < len(gbdata):

            # Euler Rotation Matrix
            e1 = convs.eultomat(Eul1[i,:])
            e2 = convs.eultomat(Eul2[i,:])

            nl = [0,0]
            nl[0]=xe1[i]-xe2[i]
            nl[1]=ye1[i]-ye2[i]
            if nl[0]==0:
                inplane = np.pi/2 + np.pi/2
            else:
                inplane = np.arctan(nl[1]/nl[0]) + np.pi/2
            if inplane < 0:
                inplane = np.pi + inplane
            if inplane >= np.pi:
                inplane = inplane - np.pi

            c, s = np.cos(inplane), np.sin(inplane)
            R = np.matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])
            Rt = convs.transpose(R)

            g1 = np.matmul(Rt, e1)
            g2 = np.matmul(Rt, e1)

            gg1 = np.matmul(Base, g1)
            gg2 = np.matmul(Base, g2)

            #### Create temporary input file for convenience

            infile = str(name)+'.in'
            fout = open(infile, 'w')
            fout.write('$Energy1D\n#$Energy2D\n$a 3.615\n$Sigma1 $a*0.175\n$Sigma2 $Sigma1\n')
            fout.write('$Epsilon 0.5\n$GroundZ1 1 1 1\n$GroundZ2 1 1 1\n$GroundX1 -1 1 0\n$GroundX2 -1 1 0\n$Tolerance 1E-8\n$AlphaX1 $a\n$AlphaY1 $a\n$AlphaZ1 $a\n$Order1 8\n$X1 0.    0.     0.     0.     0. $a/2. -$a/2.  $a/2. -$a/2. $a/2.  $a/2. -$a/2. -$a/2.\n$Y1 0. $a/2.  $a/2. -$a/2. -$a/2.    0.     0.     0.     0. $a/2. -$a/2.  $a/2. -$a/2.\n$Z1 0. $a/2. -$a/2.  $a/2. -$a/2. $a/2.  $a/2. -$a/2. -$a/2.    0.     0.     0.     0.\n$AlphaX2 $AlphaX1\n$AlphaY2 $AlphaY1\n$AlphaZ2 $AlphaZ1\n$Order2  $Order1\n$X2      $X1\n$Y2      $Y1\n$Z2      $Z1\n')
            fout.write('$OutFile ../bin/'+name+'/en_'+str(i)+'.out\n')
            fout.write('$BungeEuler1 '+str(np.degrees(Eul1[i,0]))+' '+str(np.degrees(Eul1[i,1]))+' '+str(np.degrees(Eul1[i,2]))+'\n')
            fout.write('$BungeEuler2 '+str(np.degrees(Eul2[i,0]))+' '+str(np.degrees(Eul2[i,1]))+' '+str(np.degrees(Eul2[i,2]))+'\n')
            fout.write('$TraceAngle '+str(np.degrees(inplane))+'\n')
            #fout.write('$RotAxes1 z x z x\n$Rots1  ($phi2_1) ($Phi_1) ($phi1_1) 90\n')
            #fout.write('$RotAxes2 z x z x\n$Rots2  ($phi2_2) ($Phi_2) ($phi1_2) 90\n')

            ### Line for 1D calculations
            fout.write('$ThetaRotX1 1\n$ThetaRotX2 1\n$ThetaMin -90\n$ThetaMax 90\n$DTheta 5')
            ### Line for 2D calculations
            #fout.write('$ThetaMin 0\n$ThetaMax 360\n$DTheta 10\n$RMin 0\n$RMax 1\n$DR 0.1\n')
            fout.close()

            os.system('./wield '+str(infile)+' -n '+str(proc))

            print (name, 'Boundary', i,'/',len(gbdata))
            i = i +1
    #elif dim ==2:
        #e1 = convs.eultomat(Eul1[k,:])
        #e2 = convs.eultomat(Eul2[k,:])

        #gg1 = np.matmul(Base, e1)
        #gg2 = np.matmul(Base, e2)

        ##### Create temporary input file for convenience
        #infile = 'infile.in'
        #fout = open(infile, 'w')
        #fout.write('$Energy2D\ninclude ../'+lattice+'.in\n')
        #fout.write('$OutFile ../bin/'+name+'/en2D_'+str(i)+'.out\n')
        #fout.write('$AxisX1 '+str(gg1[0,0])+' '+str(gg1[1,0])+' '+str(gg1[2,0])+' \n$AxisY1 '+str(gg1[0,2])+' '+str(gg1[1,2])+' '+str(gg1[2,2])+'\n')
        #fout.write('$AxisX1 '+str(gg2[0,0])+' '+str(gg2[1,0])+' '+str(gg2[2,0])+' \n$AxisY1 '+str(gg2[0,2])+' '+str(gg2[1,2])+' '+str(gg2[2,2])+'\n')
        #fout.write('$ThetaRotX1 1 \n$ThetaRotX2 1\n')
        #fout.write('$ThetaMin 0\n$ThetaMax 360 \n$DTheta 5\n')
        #fout.write('$RMin 0\n$Rmax 1\n$DR 0.01')
        #fout.close()

        #os.system('./main infile.in -n '+str(proc))
        ##print 'Boundaries remaining:', len(gbdata)-i
    else:
        print('Wrong dimension')


    print('Energy calculations for '+name+'finished.')
    try:
        os.system('mkdir '+pa_parent+'/ebsd_energy/outputs/'+name+'/energy')
    except:
        print ('path already exists')
    os.system('mv -v '+path+'/'+name+'/ '+pa_parent+'/ebsd_energy/outputs/'+name+'/energy')