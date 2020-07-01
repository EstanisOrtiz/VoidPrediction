import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os.path 
from scipy.spatial import distance

# Custom modules
from modules import voiddetect as vd 
from modules import select_voidboundaries as sel 


print """==========
Gathering inputs ...
=========="""

#z = int(raw_input('How many files would you like to add?: '))
## Gather inputs 
inputs = ['3_010']#['1_001','1_002','1_003','1_004','1_005','1_006','1_007','1_008','1_009','1_010',
	#'2_001','2_002','2_003','2_004','2_005','2_006','2_007','2_008','2_009',
	#'3_001','3_002','3_003','3_004','3_005','3_006','3_007','3_008','3_009','3_010',
	#'4_001','4_002','4_003','4_004','4_005','4_006','4_007','4_008','4_009',
	#'5_001','5_002','5_003','5_004','5_005','5_006','5_007','5_008','5_009','5_010','5_011',
	#'6_001','6_002','6_003','6_004','6_005','6_006','6_007','6_008','6_009','6_010']	

for name in inputs:
	print name 
	#name = '1_001'
	#name = raw_input("Enter input: ")
	lattice = 'bcc'
	#lattice = raw_input("\n\nCrystal Structure\nIndicate crystal structure.\nType one of the options fcc/bcc/hcp as shown: ")
	
	### get current directory
	pa_current = os.environ['PWD']
	# os.chdir(os.path.dirname(path_current))
	pa_parent = os.path.dirname(pa_current)
	
	#define paths for convenience
	pa_pic = pa_current+'/pyinputs/'+name+'.jpg'
	pa_txt = pa_current+'/pyinputs/'+name+'.txt'
	
	### Read data from text file
	gbdata = np.genfromtxt(pa_txt)
	width = np.amax(gbdata[:, 17])
	height = np.amax(gbdata[:, 18])
	#define maximum void area as a multiple of average grain size (last number is factor of multiplication)
	maxarea = width*height/np.amax(gbdata[:,20])*2.5
	
	### run voiddetect module and return centers and radii of detected voids
	centers, radii, vheight = vd.findvoid(pa_pic, name, maxarea)
	
	
	### Starting points
	staptsx = gbdata[:, 15]
	staptsy = gbdata[:, 16]
	#### Ending points
	endptsx = gbdata[:, 17]
	endptsy = gbdata[:, 18]
	#mis_angle = gbdata[:,6]
	#Find dimensions for picture
	width = np.amax(gbdata[:, 17])
	height = np.amax(gbdata[:, 18])
	
	ratio = height/vheight
	
	centers = np.asarray(centers)*ratio*1.0
	radii = np.asarray(radii)*ratio
	
	#os.system('mkdir '+pa_current+'/outputs/'+name)
	
	#try:
		#np.save(pa_current+'/outputs/'+name+'/centers', centers)
		#print 'saved void information succesfully'
	#except:
		#print 'Unable to save void information'
		
	min_dist = np.zeros((len(centers)))
	for i in range(0, len(centers)):
		temp_dist = np.zeros((len(centers)))
		for j in range(0,len(centers)):
			temp_dist[j] = distance.euclidean(centers[i], centers[j])
		
		min_dist[i] = np.partition(temp_dist, 1)[1]
		#print temp_dist
		
	print centers, min_dist
	
	try:
		np.save(pa_current+'/outputs/'+name+'/min_dist', min_dist)
		print 'saved minimum distance succesfully'
	except:
		print 'Unable to save minimum distance'
		
		
		
	
	
	#### Select boundaries in void vicinity
	## Comment/Uncomment as needed
	selected = sel.selgb(gbdata, centers, radii)
	
	#### Save file of selected boundaries 
	## Comment/Uncomment as needed 
	os.system('mkdir '+pa_current+'/outputs/'+name)
	
	try:
		np.savetxt(pa_current+'/outputs/'+name+'/selected.txt', selected)
		print 'Successfully saved list of selected boundaries.'
	except:
		print 'Unsuccessful. Does the directory exist?'
	## End boundary selection 
	
	
	#### Plot background picture
	## Comment/Uncomment as needed 
	fig, ax = plt.subplots(1)
	im = plt.imread(pa_pic)
	implot = plt.imshow(im, origin='lower', extent=[0, width, 0, height], aspect='equal')
	###Plot points
	IniPlot = zip(staptsx, staptsy, endptsx, endptsy)
	for tuple in IniPlot:
		plt.plot([tuple[0], tuple[2]], [tuple[1], tuple[3]],'#000000')
		
	for tuple in zip(centers, radii):
		circ = Circle(tuple[0], tuple[1], color='#FFFF00', linewidth=3, fill=False)
		ax.add_patch(circ)
		
	for row in selected:
		plt.plot([staptsx[row], endptsx[row]], [staptsy[row], endptsy[row]], color='#FF0000', linewidth= 2)
	### Save file (Comment/Uncomment as needed)
	#plt.savefig(pa_current+'/outputs/detectpics/'+name+'.png')# , bbox_inches='tight')
	#fig.clf()
	### Show plot (Comment/Uncomment as needed)
	plt.show()
	## End plot background picture
	
print 'All done.'
