# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 12:59:11 2019

@author: GabrielAsus
"""
import math
def bohachevsky(x):    
    return x[0]**2+2*x[1]**2-0.3*math.cos(3*math.pi*x[0])-0.4*math.cos(4*math.pi*x[1])+0.7
    
def himmelblau(x):
    return ((x[0]**2+x[1]-11)**2)+(x[0]+x[1]**2-7)**2

def sphere(x):
    return x[0]**2+x[1]**2
    
    