# coding: utf-8

import sys
sys.path.append("./src/")

from pypointcloud import *
from spline_tools import ParametricSpline

import scipy as S

results = None
with open("./D_mel_wt__atlas_r2.vpc") as infile:
    results = read_vpc(infile)

d = results[1]
x = d[:,0]
y = d[:,1]
z = d[:,2]


ap_line = None


x_min = x.min()
x_max = x.max()
z_min = z.min()
z_max = z.max()



import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button


N_SPLINES = 9
points_per_spline = 5

from scipy.interpolate import griddata

mesh_x = S.loadtxt("mesh_x.txt")
mesh_y = S.loadtxt("mesh_y.txt")

the_splines = list()
for i in range(mesh_x.shape[0]):
    the_splines.append(ParametricSpline(mesh_x[i],mesh_y[i]))

SAMPLE_NUMBER = 100

ts = S.linspace(0.0,1.0,SAMPLE_NUMBER)

old_xy = S.vstack([aspline(ts) for aspline in the_splines])
new_xy = S.vstack([S.hstack([i*S.ones((SAMPLE_NUMBER,1)), ts.reshape(-1,1)]) for i in range(len(the_splines))])

new_xs = griddata(old_xy, new_xy[:,0], (x, z), method='linear')
new_ys = griddata(old_xy, new_xy[:,1], (x, z), method='linear')

disp_genes = ["eve__1","eve__2","eve__3","bcdP__3","eve__4"]

for one_gene_name in disp_genes:

    colnum = results[0]["column"].index(one_gene_name)-1

    colors = S.vstack([d[:,colnum],S.zeros(d.shape[0]),S.zeros(d.shape[0])]).T
    colors -= colors.min()
    colors*=S.power(colors.max(),-1.0)

    fig = plt.figure(figsize=(4,2))
    ax = fig.add_subplot(1,1,1)
    ax.set_title(one_gene_name)
    ax.scatter(new_xs,new_ys,s=15.0,c=colors)
    fig.tight_layout()

plt.show()
