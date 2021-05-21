import numpy as np 

def sig_pick(ct):
	
	if ct == 0:
		### sigma 3 
		sigma = '3'
		ax = [0.57735027, 0.57735027, 0.57735027]
		ang = 0.87266463

	elif ct == 1:
		### sigma 5
		sigma = '5'
		ax = [0,0,1]
		ang = 0.64332836
		
	elif ct == 2:
		### sigma 7
		sigma = '7'
		ax = [0.57735027, 0.57735027, 0.57735027]
		ang = 0.66689031
		
	elif ct == 3:
		### sigma 9
		sigma = '9' 
		ax = [0.70710678, 0, 0.70710678]
		ang = 0.67963121
		
	elif ct == 4:
		### sigma 11
		sigma = '11'
		ax = [0.70710678, 0, 0.70710678]
		ang = 0.88086767
		
	elif ct == 5:
		### sigma 13a
		sigma = '13a'
		ax = [1,0,0]
		ang = 0.39461894
		
	elif ct == 6:
		### sigma 13b
		sigma = '13b'
		ax = [0.57735027, 0.57735027, 0.57735027]
		ang = 0.485027
		
	elif ct == 7:
		### sigma 15
		sigma = '15'  
		ax = [4.47213595e-01, 1.35999698e-16, 8.94427191e-01]
		ang = 8.40899634e-01
		
	elif ct == 8:
		### sigma 17a
		sigma = '17a' 
		ax = [1,0,0]
		ang = 0.48991392
		
	elif ct == 9:
		### sigma 17b
		sigma = '17b'  
		ax = [0., 0., 1.]
		ang =  0.49008845
		
	elif ct == 10:
		### sigma 19a
		sigma = '19a' 
		ax = [ 0.70710678,  0., 0.70710678]
		ang = 0.46286132
		
	elif ct == 11:
		### sigma 19b
		sigma = '19b' 
		ax = [1,1,1]
		ang = 0.81716316
		
	elif ct == 12:
		### sigma 21a
		sigma = '21a'
		ax = [1,1,1]
		ang = 0.38013271
		
	elif ct == 13:
		### sigma 21b
		sigma = '21b' 
		ax = [2,1,1]
		ang =  np.deg2rad(44.41)
		
	elif ct == 14:
		### sigma 23
		sigma = '23' 
		ax = [0.30151134, 0.30151134, 0.90453403]
		ang = 0.70598568
		
	elif ct == 15:
		### sigma 25a
		sigma = '25a' 
		ax = [0., 0., 1.]
		ang = 0.28379054
		
	elif ct == 16:
		### sigma 25b
		sigma = '25b' 
		ax = [0.6882472,   0.22941573,  0.6882472]
		ang = 0.90198616
		
	elif ct == 17:
		### sigma 27a
		sigma = '27a'
		ax = [0.70710678,  0.,          0.70710678]
		ang = 0.55134951
		
	elif ct == 18:
		### sigma 27b
		sigma = '27b' 
		ax = [4.47213595e-01, 1.82432967e-16, 8.94427191e-01]
		ang = 6.18370154e-01 
		
	elif ct == 19:
		### sigma 29a
		sigma = '29a'
		ax = [0.,          0.,          1.]
		ang = 0.76096355
		
	elif ct == 20:
		### sigma 29b
		sigma = '29b'
		ax = [0.66666667,  0.33333333,  0.66666667]
		ang = 0.80983277
		
	elif ct == 21:
		### sigma 31a
		sigma = '31a' 
		ax = [0.57735027,  0.57735027,  0.57735027]
		ang = 0.31241394
		
	elif ct == 22:
		### sigma 31b 
		sigma = '31b'
		ax = [0.40820676,  0.40820676,  0.81653811]
		ang = 0.91109887
		
	elif ct == 23:
		### sigma 33a
		sigma = '33a' 
		ax = [0.70710678,  0.,          0.70710678]
		ang = 0.34993852
		
	elif ct == 24:
		### sigma 33b
		sigma = '33b' 
		ax = [0.30151134,  0.30151134,  0.90453403]
		ang = 0.5857325
		
	elif ct == 25:
		### sigma 33c
		sigma = '33c' 
		ax = [0.70710678,  0.,          0.70710678]
		ang = 1.02956973    
	
	else:
		print 'error picking sigma value'	
	
	return ax, ang, sigma 
