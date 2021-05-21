import numpy as np
import cv2

# Custom modules
from modules import checkCircle as check
from modules import intersection_dic as ipd
from modules import void_parameter as vdpr

# Blank image size
height=500
width=500
img= 255 * np.ones(shape=[height, width, 3], dtype=np.uint8)
# Define size of the void
void_center=(250,250)
void_radi=100
# Define gb coordinates
gb_start=[(105,195),(215,175),(300,200),(166,266),(113,333),(310,311),(390,205)]
#gb_start=

gb_end=[(200,180),(300,120),(350,180),(176,266),(197,315),(344,324), (372,220)]
#gb_end=

dic={}

# Void drawing
cv2.circle(img, void_center, 3, (255, 0, 0), -1)
cv2.circle(img, void_center, void_radi, (0, 0, 255), 3)

# Run void parameter
drawing=[height, width]
"""
distance=[]
i=0
for gb_s, gb_e in zip(gb_start,gb_end):
    distance[i] = check.checkDist(gb_s[0], gb_s[1], gb_e[0], gb_e[1], void_center[0], void_center[1], void_radi)
    i=i+1
"""
pred_lines=[]
r=0
for gb_s, gb_e in zip(gb_start,gb_end):
    x1,y1,x2,y2=gb_s[0],gb_s[1],gb_e[0],gb_e[1]
    cv2.line(img,gb_s,gb_e,(255,0,0),2)
    x_m = (gb_s[0] + gb_e[0]) / 2
    y_m = (gb_s[1] + gb_e[1]) / 2
    mid_gb = (int(x_m), int(y_m))
    d = check.checkDist(x1, y1, x2, y2, void_center[0], void_center[1], void_radi)
    #cv2.putText(img, str(r), mid_gb, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.circle(img, mid_gb, 3, (0, 0, 0), -1)
    dic[r]=[gb_s, gb_e]
    r = r + 1

#inter_section_dic =ipd.intersection_dic_test(gb_start,gb_end,void_center,void_radi)
ipd_dic, pred_lines_dic,same_inter_dic=ipd.intersection_dic(dic,void_center,void_radi,1,1) # Increase tol for test sample
near_pts=ipd.near_point(dic,void_center,void_radi)
print(near_pts)

for clave, valor in ipd_dic.items():
    p1=(int(valor[0][0][0]),int(valor[0][0][1]))
    p2=(int(valor[0][1][0]),int(valor[0][1][1]))
    dist=round(valor[1], 4)

    cv2.circle(img, p2, 3, (0, 255, 255), -1)
    cv2.line(img, p1, p2, (0, 255, 0), 2)

    if clave==1:
        dd=np.sqrt(((p2[0] - void_center[0]) ** 2) + ((p2[1] - void_center[1]) ** 2))
        cv2.putText(img, str(round(dd,3)), p2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    elif clave==6:
        dd=np.sqrt(((p2[0] - void_center[0]) ** 2) + ((p2[1] - void_center[1]) ** 2))
        cv2.putText(img, str(round(dd,3)), p2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

for cc, vv in near_pts.items():
    if cc not in ipd_dic.keys():
        pp2=tuple(vv[0])
        ddd=np.sqrt(((pp2[0] - void_center[0]) ** 2) + ((pp2[1] - void_center[1]) ** 2))
        cv2.putText(img, str(round(ddd, 3)), pp2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        print(cc)


for cl1, val1 in pred_lines_dic.items():
    for val2 in val1:
        pt2_v=(int(val2[1][0]),int(val2[1][1]))
        pt1_v = (int(val2[0][0]), int(val2[0][1]))
    #cv2.line(img, pt1_v, pt2_v, (0, 255, 0), 1)

print(ipd_dic)

cv2.imshow('Void Parameter Tester', img)
cv2.waitKey(0)
