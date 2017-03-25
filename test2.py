
# coding: utf-8

# In[1]:

import sys


# In[2]:

sys.path.append("./src/")


# In[3]:

from pypointcloud import *


# In[4]:

results = None
with open("./D_mel_wt__atlas_r2.vpc") as infile:
    results = read_vpc(infile)


# In[6]:




# In[ ]:
import scipy as S

data = results[1]
x = data[:,0]
y = data[:,1]
z = data[:,2]

x_selector = S.logical_and(x > -10000.0, x < 100020.0)

print x.min(), x.max()
print y.min(), y.max()
print z.min(), z.max()

x = x[x_selector]
y = y[x_selector]
z = z[x_selector]

d = data[x_selector]

colnum = results[0]["column"].index("eve__4")-1

colors = S.vstack([d[:,colnum],S.zeros(d.shape[0]),S.zeros(d.shape[0])]).T
colors -= colors.min()
colors*=S.power(colors.max(),-1.0)
print colors.shape

import matplotlib.pyplot as plt
fig = plt.figure()
plt.scatter(x,z,s=15.0,c=colors)
fig.show()
