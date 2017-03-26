# coding: utf-8

import sys
sys.path.append("./src/")

from pypointcloud import *

import scipy as S

results = None
with open("./D_mel_wt__atlas_r2.vpc") as infile:
    results = read_vpc(infile)

d = results[1]
x = d[:,0]
y = d[:,1]
z = d[:,2]


colnum = results[0]["column"].index("eve__4")-1

colors = S.vstack([d[:,colnum],S.zeros(d.shape[0]),S.zeros(d.shape[0])]).T
colors -= colors.min()
colors*=S.power(colors.max(),-1.0)

ap_line = None

try:
    ap_line = S.loadtxt("spline_points.txt")
except:
    ap_line = S.array([[-213.1,13.5],
                    [-90.67,5.46],
                    [-52.56,1.54],
                    [-15.34,0.622],
                    [12.9,0.622],
                    [44.75,1.54],
                    [78.38,3.39],
                    [118.3,7.54],
                    [187.8,16.3]])





import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button

from EditableSpline import *











fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(x,z,s=15.0,c=colors)

main_spline = EditableSpline(ax,ap_line)
main_spline.connect()
main_spline.update_line()

plt.show()

S.savetxt("spline_points.txt",main_spline.data)
