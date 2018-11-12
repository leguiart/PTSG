#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 18:06:07 2018

@author: leguiart
"""
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib as mp
import numpy as np

A = np.matrix([
   [0.5,0.5],
   [0.25,0.25],
   [0.25,0.75],
   [0.75,0.25],
   [0.75,0.75]])
   

c = np.matrix([
   [0.002],
   [0.005],
   [0.005],
   [0.005],
   [0.005],
   ])
   
#math.exp(-(vprima - v)/(c_enfriamiento*Tinit))
def function(x):
    #print(np.kron(x,np.ones((5,1))))
    d = (np.kron(x,np.ones((5,1)))-A)
    return np.sum(np.exp(-np.multiply(-d,d)/(0.07*11.7745))+c)



f = np.vectorize(lambda x,y: function(np.array([x,y])))
f2 = lambda x,y: function(np.array([x,y]))

x = np.linspace(0,5,100)

y = np.linspace(0,5,100)

X,Y = np.meshgrid(x,y)
print(np.array([X,Y]))

Z = f(X,Y)


fig = mp.pyplot.figure()
ax = Axes3D(fig)
ax.plot_surface(X,Y,Z,rstride=5,cstride=5,cmap=cm.jet)