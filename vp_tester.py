import numpy as np
import cv2

# Custom modules
from modules import checkCircle as check
from modules import intersection_dic as ipd
from modules import void_parameter as vdpr

# Blank image size
height=500
width=500
img = 255 * np.ones(shape=[height, width, 3], dtype=np.uint8)
img2=255 * np.ones(shape=[height, width, 3], dtype=np.uint8)
# Define size of the void
void_center=(250,250)
void_radi=100
# Define gb coordinates
gb_start=[(105,195),(215,175),(300,200),(166,266),(113,333),(310,311),(390,205)]
#gb_start=

gb_end=[(200,180),(300,120),(350,180),(176,266),(197,315),(344,324), (350,240)]
#gb_end=

dic={}
len_org={} # original length inside the circle
len_rec={} # reconstructed lentgh
prx_par={} # proximity parameter dic

# Void drawing
cv2.circle(img, void_center, 3, (0, 0, 255), -1)
cv2.circle(img, void_center, void_radi, (0, 0, 255), 3)

cv2.circle(img2, void_center, 3, (0, 0, 255), -1)
cv2.circle(img2, void_center, void_radi, (0, 0, 255), 3)

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
    # Draw gb
    x1,y1,x2,y2=gb_s[0],gb_s[1],gb_e[0],gb_e[1]
    cv2.line(img,gb_s,gb_e,(255,0,0),2)
    cv2.line(img2, gb_s, gb_e, (0, 0, 0), 2)

    # Draw mid points and create dictionary of gb:[(x1,y1) (x2,y2)]
    x_m = (gb_s[0] + gb_e[0]) / 2
    y_m = (gb_s[1] + gb_e[1]) / 2
    mid_gb = (int(x_m), int(y_m))
    d = check.checkDist(x1, y1, x2, y2, void_center[0], void_center[1], void_radi)
    cv2.putText(img, str(r), mid_gb, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1) # gb id
    cv2.circle(img, mid_gb, 3, (0, 0, 0), -1)
    dic[r]=[gb_s, gb_e]


    # Check if start and/or end point are inside of the circle
    prox, p3s=check.inside_len(gb_s,gb_e,void_center, void_radi)

    len_org[r]=check.distance(p3s[0],p3s[1])

    for p3 in p3s:
        if p3[0]>0 and p3[1]>0:
            p3d=tuple(np.array(p3,int))
            cv2.circle(img2, p3d, 3, (0, 0, 0), -1)

    cv2.line(img2, tuple(np.array(p3s[0],int)), tuple(np.array(p3s[1],int)), (255, 0, 0), 2)

    #cv2.putText(img2, str(round(prox,2)), p3s[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    r = r + 1
    #leng=((x2-x1)**2 + (y2-y1)**2)**0.5
    #cv2.putText(img2, str(round(leng,2)), (int(x_m), int(y_m)+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)



# inter_section_dic =ipd.intersection_dic_test(gb_start,gb_end,void_center,void_radi)
#print(dic)
ipd_dic, pred_lines_dic,same_inter_dic=ipd.intersection_dic(dic,void_center,void_radi,1,1) # Increase tol for test sample
near_pts=ipd.near_point(dic,void_center,void_radi)
print(ipd_dic)

for clave, valor in ipd_dic.items():
    p1=(int(valor[0][0][0]),int(valor[0][0][1]))
    p2=(int(valor[0][1][0]),int(valor[0][1][1]))
    dist=round(valor[1], 4)

    cv2.circle(img, p2, 3, (0, 255, 255), -1)
    cv2.line(img, p1, p2, (0, 255, 0), 2)


    cv2.circle(img2, p2, 3, (0, 255, 255), -1)
    cv2.line(img2, p1, p2, (0, 255, 0), 2)

    len_rec[clave]=dist

for cc, vv in near_pts.items():
    if cc not in ipd_dic.keys():
        pp2=tuple(np.array(vv[0],int))
        ddd = np.sqrt(((pp2[0] - void_center[0]) ** 2) + ((pp2[1] - void_center[1]) ** 2))
        #cv2.putText(img, str(round(ddd, 3)), pp2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


for cl1, val1 in pred_lines_dic.items():
    for val2 in val1:
        pt2_v=(int(val2[1][0]),int(val2[1][1]))
        pt1_v = (int(val2[0][0]), int(val2[0][1]))
    #cv2.line(img, pt1_v, pt2_v, (0, 255, 0), 1)


# Proximity parameter
for gbb, gb_point in dic.items():

    len=len_org.get(gbb)
    if gbb in len_rec.keys():
        rec=len_rec.get(gbb)
    else:
        rec=0

    print('-',gbb,'-')
    print(len)
    print(rec)
    print(len+rec)

    par=(len+rec)/(2*void_radi)
    prx_par[gbb]=par
    gb1, gb2=gb_point

    xm = (gb1[0] + gb2[0])/2
    ym = (gb1[1] + gb2[1])/2
    midgb = (int(xm), int(ym)+13)

    cv2.putText(img2, str(round(par, 3)),midgb, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


cv2.imshow('Void Parameter Tester', img)
cv2.imshow('Proximity Parameter', img2)
cv2.waitKey(0)
