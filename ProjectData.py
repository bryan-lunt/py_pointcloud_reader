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

import scipy.interpolate as INTERP

import scipy.optimize as OPT



import spline_tools as st


myspline,other = st.all_spline_stuff(ap_line[:,0],ap_line[:,1])

def distance(x,x_0,y_0):
    y = myspline(x)
    dist = S.real(S.power(S.power(x_0-x,2.0)+S.power(y_0-y,2.0),0.5))
    return dist

new_xs = S.zeros_like(x)
new_zs = S.zeros_like(z)

for i in range(new_xs.size):
    foo = OPT.minimize(distance,x[i],args=(x[i],z[i]))
    new_xs[i] = foo.x
    new_zs[i] = foo.fun*S.sign(z[i]-myspline(x[i]))


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#ax.scatter(new_xs,new_zs,s=15.0,c=colors)
ax.scatter(new_xs,z,s=15.0,c=colors)

xs = S.linspace(ap_line[0,0],ap_line[-1,0],200)
ys = S.zeros_like(xs)

ax.plot(xs,ys,color="g")

plt.show()
