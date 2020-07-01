import numpy as np 

def selgb(gbdata, centers, radii):
	### Starting points
	sx = gbdata[:, 15]
	sy = gbdata[:, 16]
	### Ending points
	ex = gbdata[:, 17]
	ey = gbdata[:, 18]
	#Points = zip(staptsx, staptsy, endptsx, endptsy)
	#Points = (1, 2, 3, 4)

	i = 0
	selected = []
	while i < len(gbdata):
		#for tuple in zip(centers[:,0], centers[:,1], radii):
		for tuple in zip(centers[:][0], centers[:][1], radii):
			stapt = (sx[i]-tuple[0])**2+(sy[i]-tuple[1])**2
			endpt = (ex[i]-tuple[0])**2+(ey[i]-tuple[1])**2
			rsqu = tuple[2]**2
			if (stapt <= rsqu or endpt <= rsqu) and gbdata[i,13] >= 5.0:
				selected.append(i)
			else:
				continue
		i = i + 1

	return selected
