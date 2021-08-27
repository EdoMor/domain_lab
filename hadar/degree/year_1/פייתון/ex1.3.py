r=float(input('ball radius:'))
a=(4/3)**0.5*r
import math
vb=(4/3)*math.pi*r**3
vc=a**3
d=vb-vc
print('difference:', d)

##ball radius:2.5
##difference: 41.39358573355295
