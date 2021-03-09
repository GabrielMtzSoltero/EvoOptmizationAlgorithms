# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:56:41 2019

@author: GabrielAsus
"""

import PSO as pso
import cv2
import math
import numpy as np
import matplotlib.pyplot  as plt
import benchfunctions as bn

def bohachevsky(x):    
    return x[0]**2+2*x[1]**2-0.3*math.cos(3*math.pi*x[0])-0.4*math.cos(4*math.pi*x[1])+0.7

def maxInImage(x,imagen):
    if(x[0]>511):
        x[0]=511
    if(x[1]>511):
        x[1]=511
    if(x[0]<0):
        x[0]=0
    if(x[1]<0):
        x[1]=0
    return imagen[int(x[0])][int(x[1])]



lower=[-10,-10]
upper=[10,10]
breakCriteria=-250

imagen=cv2.imread('imagen.jpg',0)

algoritmo=pso.PSO(dimention=2,
                 lower=lower,
                 upper=upper,
                 function=bohachevsky,
                 populationSize=30,
                 maxIter=100,
                 breakCriteria=breakCriteria,
                 wInertia=.5,
                 c1=2,
                 c2=2,
                 imagen=imagen
                 )
solucion,fitness=algoritmo.run()
print('terminó algoritmo')
print (solucion)
print (fitness)
