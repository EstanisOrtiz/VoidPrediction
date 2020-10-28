import numpy as np
import math 


#### Calculates Euler Angles from Miller indices
### Needs two orthonormal vectors to form an orthonormal basis for each crystal. 4 vectors total.  
### hkl is the axis that 'wield' program will rotate about, uvw is the other orthonormal vector

def miltoeul(hkl1, uvw1, hkl2, uvw2): 
	
	#### Normalize vectors	
	hkl1 = hkl1/np.linalg.norm(hkl1)
	uvw1 = uvw1/np.linalg.norm(uvw1)
	hkl2 = hkl2/np.linalg.norm(hkl2)
	uvw2 = uvw2/np.linalg.norm(uvw2)

	### Create third vector for orthonormal basis
	t1 = np.cross(hkl1, uvw1)
	t1 = t1/np.linalg.norm(t1)
	
	t2 = np.cross(hkl2, uvw2)
	t2 = t1/np.linalg.norm(t2)
	
	### Euler angles for first crystal 
	Phi_1 = math.degrees(np.arccos(hkl1[2]))
	phi1_1 = math.degrees(np.arctan(hkl1[0]/(-1*hkl1[1])))
	phi2_1 = math.degrees(np.arctan(uvw1[2]/t1[2]))
	Eul1 = [phi1_1, Phi_1, phi2_1]
	
	### Euler angles for second crystal 
	Phi_2 = math.degrees(np.arccos(hkl2[2]))
	phi1_2 = math.degrees(np.arctan(hkl2[0]/(-1*hkl2[1])))
	phi2_2 = math.degrees(np.arctan(uvw2[2]/t2[2]))
	Eul2 = [phi1_2, Phi_2, phi2_2]
	
	return Eul1, Eul2
	
### Euler to rotation matrix 
def eultomat(Eul):
	
	g = np.zeros((3,3))
	
	g[0,0]=np.cos(Eul[0])*np.cos(Eul[2])-np.sin(Eul[0])*np.sin(Eul[2])*np.cos(Eul[1])
	g[0,1]=np.sin(Eul[0])*np.cos(Eul[2])+np.cos(Eul[0])*np.sin(Eul[2])*np.cos(Eul[1])
	g[0,2]=np.sin(Eul[2])*np.sin(Eul[1])

	g[1,0]=(-1)*np.cos(Eul[0])*np.sin(Eul[2])-np.sin(Eul[0])*np.cos(Eul[2])*np.cos(Eul[1])
	g[1,1]=(-1)*np.sin(Eul[0])*np.sin(Eul[2])+np.cos(Eul[0])*np.cos(Eul[2])*np.cos(Eul[1])
	g[1,2]=np.cos(Eul[2])*np.sin(Eul[1])

	g[2,0]=np.sin(Eul[0])*np.sin(Eul[1])
	g[2,1]=(-1)*np.cos(Eul[0])*np.sin(Eul[1])
	g[2,2]=np.cos(Eul[1])
	
	return g 	
	
def angtovec(theta, psi):
	
	v_out = [0,0,0]
	
	v_out[0]=np.sin(theta)*np.cos(psi)
	v_out[1]=np.sin(theta)*np.sin(psi)
	v_out[2]=np.cos(theta)
	
	return v_out 
	
def transpose(g):
	
	gt=np.zeros((3,3))
	
	for ii in range(0,3):
		for jj in range(0,3):
			gt[ii,jj]=g[jj,ii]
	
	return gt 
	
def mattovec(gt, n1_vec):
	
	n2_vec = [0,0,0]
	for ii in range(0,3):
		for jj in range(0,3):
			n2_vec[ii]=n2_vec[ii]+gt[ii,jj]*n1_vec[jj]
	
	return n2_vec

def mattomat(g1, g2):
	
	g3 = np.zeros((3,3))
	
	for ii in range(0,3):
		for jj in range(0,3):
			for kk in range(0,3):
				g3[ii,jj]=g3[ii,jj]+g1[ii,kk]*g2[kk,jj]
	return g3
	
def mattoeul(mat):
	
	xz = mat[2,2]
	
	Eul =[0,0,0]
	
	if xz*xz < 1:
		sf = np.sqrt(1-xz*xz)
	else:
		sf = 0 

		
	if sf > 1.e-6:
		Eul[0] = np.arccos(-mat[2,1]/sf)
		if mat[2,0] < 0:
			Eul[0]=2*np.pi-Eul[0]
		Eul[1]=np.arccos(xz)
		Eul[2]=np.arccos(mat[1,2]/sf)
		if mat[0,2] <0:
			Eul[2] = 2*np.pi-Eul[2]
	else:
		Eul[0] = np.arccos(mat[1,1])
		if mat[0,1]<0:
			Eul[0]=2*np.pi-Eul[0]
		Eul[1]=0
		Eul[2]=0
		
	#PHI = np.arccos(mat[2,2])
	#if mat[2,1] == 0:
		#phi1 = 0 
	
	#else:
		#phi1 = np.arctan(mat[2,0]/mat[2,1]*-1)
	#if mat[1,2] ==0:
		#phi2 = 0 
	#else:
		#phi2 = np.arctan(mat[0,2]/mat[1,2])
	
	#Eul = [phi1, PHI, phi2]
	
	return Eul
	
def mattoaxang(R1):
	misang1 = np.arccos(0.5*(R1[0,0]+R1[1,1]+R1[2,2]-1))
	p1 = (R1[2,1]-R1[1,2])/(2*np.sin(misang1))
	p2 = (R1[0,2]-R1[2,0])/(2*np.sin(misang1))
	p3 = (R1[1,0]-R1[0,1])/(2*np.sin(misang1))
	
	ax = [p1,p2,p3]
	ang = misang1
	ax = ax/np.linalg.norm(ax)
	
	return ax, ang
	
def vectoang(v):
	if v[2] < 0:
		v[0] = -v[0]
		v[1] = -v[1]
		v[2] = -v[2]
	else:
		v = v
		
	
	a = [0,0]
	a[0]=np.arccos(v[2])
	if v[0] !=0:
		a[1]=np.arctan(v[1]/v[0])
	else: 
		a[1]=np.pi/2
	
	if a[1] < 0:
		a[1] = 2*np.pi + a[1]
		
	return a 

# Euler Angle to quaternion 	
def eu2qu(Eul):
	
	P = -1
	
	o = (Eul[0]+Eul[2])/2 
	d = (Eul[0]-Eul[2])/2
	c = np.cos(Eul[1]/2)
	s = np.sin(Eul[1]/2)
	q = [c*np.cos(o), -P*s*np.cos(d), -P*s*np.sin(d), -P*c*np.sin(o)]

	if c*np.cos(o) <0:
		q = [-c*np.cos(o), P*s*np.cos(d), P*s*np.sin(d), P*c*np.sin(o)]
		
	else:
		q = [c*np.cos(o), -P*s*np.cos(d), -P*s*np.sin(d), -P*c*np.sin(o)]

	
	return q  

# Axis angle to quaternion 
def ax2qu(ax, ang):
	q = [np.cos(ang/2), np.sin(ang/2)*ax[0], np.sin(ang/2)*ax[1], np.sin(ang/2)*ax[2]]
	
	return q 	 
	
# Quaternion to axis/angle 
def qu2ax(q):
	
	w = 2*np.arccos(q[0])
	
	if w == 0:
		ax = [0, 0, 1]
		ang = 0 
		
	elif q[0] == 0:
		ax = [q[1], q[2], q[3]]
		ang = np.pi
		
	else:
		s = q[0]/np.sqrt(q[1]*q[1] + q[2]*q[2] + q[3]*q[3])
		ax = [s*q[1], s*q[2], s*q[3]]
		ang = w 
		
	return ax, ang 

# axis angle to matrix 		
def ax2om(ax, ang):
	
	g = np.zeros((3,3))
	
	c = np.cos(ang)
	s = np.sin(ang)
	
	g[0,0] = c + (1-c)*ax[0]**2
	g[0,1] = (1-c)*ax[0]*ax[1]+s*ax[2]
	g[0,2] = (1-c)*ax[0]*ax[2]-s*ax[1]	

	g[1,0] = (1-c)*ax[0]*ax[1]-s*ax[2]
	g[1,1] = c + (1-c)*ax[1]**2
	g[1,2] = (1-c)*ax[1]*ax[2]+s*ax[0]	
	
	g[2,0] = (1-c)*ax[0]*ax[2]+s*ax[1]
	g[2,1] = (1-c)*ax[1]*ax[2]-s*ax[0]
	g[2,2] = c + (1-c)*ax[2]**2

	return g 
