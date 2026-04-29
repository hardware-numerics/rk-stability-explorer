#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 03:04:01 2026

@author: gransalis
"""

import numpy as np,numpy.random
import matplotlib.pyplot as plt,matplotlib,scipy.optimize

maxx=2500
maxy=2500
maxrad=60 #max radius of the circle
ncirc=100 # number of circles
np.random.seed(1)

#define centers of circles
xc,yc=np.random.uniform(0,maxx,ncirc),np.random.uniform(0,maxy,ncirc)
rads=np.random.uniform(0,maxrad,ncirc)
#define circle radii

xgrid,ygrid=np.mgrid[0:maxx,0:maxy]
im=xgrid*0+np.inf

for i in range(ncirc):
    im = np.minimum(im, ((xgrid - xc[i])**2 + (ygrid - yc[i])**2)**.5 - rads[i])
# im now stores the minimum radii of the circles which can 
# be placed at a given position without overlap

#plotting 
fig=plt.figure(1)
plt.clf()
plt.imshow(im.T,extent=(0, maxx, 0, maxy))
plt.colorbar()
ax = plt.gca()
for i in range(ncirc):
     ax.add_patch(matplotlib.patches.Circle((xc[i], yc[i]), rads[i],
          facecolor='none', edgecolor='red'))
plt.xlim(0, maxx)
plt.ylim(0, maxy)
plt.draw()