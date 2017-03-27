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


x_min = x.min()
x_max = x.max()
z_min = z.min()
z_max = z.max()



import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button

from EditableSpline import *

N_SPLINES = 9
points_per_spline = 5


x_pos = S.linspace(x_min,x_max,N_SPLINES)

cutsplines = list()
for i in range(N_SPLINES):
    cutsplines.append(S.vstack([S.ones(points_per_spline)*x_pos[i],S.linspace(z_min,z_max,points_per_spline)]).T)

editable_spline_list = list()







fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(x,z,s=15.0,c=colors)

multi = MultiSpline(ax,cutsplines)
multi.connect()
multi.update_line()

plt.show()

mesh_x = S.array([i.data[:,0] for i in multi.splines])
mesh_y = S.array([i.data[:,1] for i in multi.splines])

S.savetxt("mesh_x.txt",mesh_x)
S.savetxt("mesh_y.txt",mesh_y)

S.savetxt("all_mesh.txt",S.array(multi.datas))
