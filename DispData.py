
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

print results[0]["column"]


# In[ ]:
import scipy as S

data = results[1]
x = data[:,0]
y = data[:,1]
z = data[:,2]

colnum = results[0]["column"].index("eve__3")-1

colors = S.vstack([data[:,colnum],S.zeros(data.shape[0]),S.zeros(data.shape[0])]).T
colors -= colors.min()
colors*=S.power(colors.max(),-1.0)



import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(x,z,s=15.0,c=colors)

plt.show()
