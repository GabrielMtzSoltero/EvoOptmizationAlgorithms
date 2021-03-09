# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 18:01:49 2019

@author: GabrielAsus
"""
import ABC as abc
import math
lower=[-6,-6]
def function1(x):
    
    return x[0]**2+2*x[1]**2-0.3*math.cos(3*math.pi*x[0])-0.4*math.cos(4*math.pi*x[1])+0.7
    #return ((x[0]**2+x[1]-11)**2)+(x[0]+x[1]**2-7)**2  

algoritmo=abc.ArtifitialBC(dimention=2,
                 lower=[-100,-100],
                 upper=[100,100],
                 function=function1,
                 populationSize=30,
                 maxIter=200)
solution,fitness=algoritmo.run()
print(solution)
print(fitness)
