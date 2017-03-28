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

import scipy.interpolate as INTERP

mesh_x = S.loadtxt("mesh_x.txt")
mesh_y = S.loadtxt("mesh_y.txt")

the_splines = list()
for i in range(mesh_x.shape[0]):
    the_splines.append(ParametricSpline(mesh_x[i],mesh_y[i]))

SAMPLE_NUMBER = 100

ts = S.linspace(0.0,1.0,SAMPLE_NUMBER)

old_xy = S.vstack([aspline(ts) for aspline in the_splines])
new_xy = S.vstack([S.hstack([i*S.ones((SAMPLE_NUMBER,1)), ts.reshape(-1,1)]) for i in range(len(the_splines))])

new_xs = INTERP.griddata(old_xy, new_xy[:,0], (x, z), method='linear')
new_ys = INTERP.griddata(old_xy, new_xy[:,1], (x, z), method='linear')
new_ys = 1.0 -new_ys

b_box_x = S.array([0.5, 7.5])
b_box_y = S.array([0.35, 0.6])

#disp_genes = ["kni__3","D__3","hbP__3","bcdP__3","KrP__3","gt__3","eve__3","odd__3","rho__3","sna__3"]
disp_genes = ["eve__3"]

for one_gene_name in disp_genes:

    colnum = results[0]["column"].index(one_gene_name)-1

    colors = S.vstack([d[:,colnum],S.zeros(d.shape[0]),S.zeros(d.shape[0])]).T
    colors -= colors.min()
    colors*=S.power(colors.max(),-1.0)

    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(2,1,1)
    ax.set_title(one_gene_name)
    ax.scatter(new_xs,new_ys,s=45.0,c=colors,alpha=0.75)
    ax.set_ylabel("D/V axis \n(linear in this figure, \nlater radial)")

    ax.axhline(b_box_y[0],c="b")
    ax.axhline(b_box_y[1],c="b")
    ax.axvline(b_box_x[0],c="b")
    ax.axvline(b_box_x[1],c="b")

    for i in range(1,8):
        ax.axvline(float(i),c="g")

    xy_selector = S.logical_and(S.logical_and(new_xs >= b_box_x[0], new_xs <= b_box_x[1]), S.logical_and(new_ys >= b_box_y[0], new_ys <= b_box_y[1]))


    selected_data_xs = new_xs[xy_selector]
    selected_data_ys = new_ys[xy_selector]
    selected_data = d[xy_selector,:]

    x_sort = selected_data_xs.argsort()
    selected_data_xs = selected_data_xs[x_sort]
    selected_data_ys = selected_data_ys[x_sort]
    selected_data = selected_data[x_sort]

    val_spline_y = selected_data[:,colnum]

    a_spline = INTERP.UnivariateSpline(selected_data_xs,val_spline_y,ext=3,s=3)
    spline_xs = S.linspace(0.0,8.0,100)

    ax2 = fig.add_subplot(2,1,2,sharex=ax)
    ax2.scatter(selected_data_xs,val_spline_y)
    ax2.plot(spline_xs, a_spline(spline_xs),c="r")

    ax2.set_xlabel("Natural A/P axis.")

    fig.tight_layout()

plt.show()
