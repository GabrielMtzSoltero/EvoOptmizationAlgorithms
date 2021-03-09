# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 14:36:52 2019

@author: GabrielAsus
"""

import DE as de
import benchfunctions as bn
import numpy as np
def sphere(x):
    return x[0]**2+x[1]**2
    return np.sum(x*x)


lower=[-10,-10,-10]
upper=[10,10,10]
breakCriteria=.00005
algoritmo=de.algorithmDE(dimention=2,
                 lower=lower,
                 upper=upper,
                 function=sphere,
                 populationSize=30,
                 maxIter=200,
                 breakCriteria=breakCriteria,
                 F=.5,
                 C=.5,
                 seed=9001)
solucion,fitness,=algoritmo.run()
print('terminó algoritmo')
print(solucion)
print(fitness)
