# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 13:26:19 2019

@author: GabrielAsus
"""

import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import math
import copy
import time
class particleDE(object):
    def __init__(self,dimention,lower=None,upper=None):
        self.solution=[] 
        self.lower=lower
        self.upper=upper
        for i in range(dimention):
            if(lower!=None and upper!=None):
                self.solution=np.append(self.solution,(random.uniform(lower[i],upper[i])))  
            else:
                self.solution=np.apppend(self.solution,float(random.random()))

        self.value=sys.float_info.max
        
        
class algorithmDE(object):
    def __init__(self,dimention,populationSize,lower,upper,function,maxIter,breakCriteria=None,F=0.7,C=0.5,seed=None):
        self.dimention=dimention
        self.particles=[particleDE(dimention,lower,upper) for i in range(populationSize)]
        self.maxIter=maxIter
        self.lower=lower
        self.upper=upper
        self.populationSize=populationSize
        self.function=function
        self.breakCriteria=breakCriteria
        self.F=F
        self.C=C
        self.seed=seed
        self.mutantV=particleDE(dimention,lower,upper)
        self.trialV=[particleDE(dimention,lower,upper) for i in range(populationSize)]
        self.bestParticle=particleDE(dimention,lower,upper)
        self.bestParticle.value=sys.float_info.max
        self.bestIndx=None
        plt.ion()
        self.fig= plt.figure()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
        
    def run(self):
        counter=0
        if(self.seed!=None):
            random.seed(9001)
        while counter<self.maxIter:
            for idx in range(self.populationSize):
                r1=random.randrange(self.populationSize)                
                r2=random.randrange(self.populationSize)
                while r1==r2:
                    r2=random.randrange(self.populationSize)
                r3=random.randrange(self.populationSize)
                while r3 == r1 or r3==r2:
                    r3=random.randrange(self.populationSize)
                self.mutantV.solution=self.particles[r1].solution+self.F*(self.particles[r2].solution-self.particles[r3].solution)
                J_r=random.randrange(self.dimention)
                for j in range(self.dimention):
                    r_cj=random.random()
                    if r_cj<self.C or j==J_r:
                        self.trialV[idx].solution[j]=copy.deepcopy(self.mutantV.solution[j])
                    else:
                        self.trialV[idx].solution[j]=self.particles[idx].solution[j]
                self.trialV[idx].value    = self.function(self.trialV[idx].solution)
                self.particles[idx].value = self.function(self.particles[idx].solution)
                if self.trialV[idx].value<self.particles[idx].value:
                    self.particles[idx].solution=copy.deepcopy(self.trialV[idx].solution)
                    self.particles[idx].value=copy.deepcopy(self.trialV[idx].value)
                if self.breakCriteria!=None:
                    if self.particles[idx].value<self.breakCriteria:
                        self.bestIndx=idx
                        break;
                        
            if self.bestIndx!=None:
                return self.particles[self.bestIndx].solution,self.particles[self.bestIndx].value
            for idx in range(self.populationSize):
                if self.particles[idx].value<self.bestParticle.value:
                    self.bestParticle=copy.deepcopy(self.particles[idx])                
            counter+=1
            self.plotear(counter,self.bestIndx)
        return self.bestParticle.solution,self.bestParticle.value
    
    def plotear(self,counter,idxBest):       
        
        x1 = np.arange(-200, 200, 0.25)
        x2 = np.arange(-200, 200, 0.25)
        x1, x2 = np.meshgrid(x1, x2)

        Z = x1**2+x2**2
        #aqui estoy pleteando la funcion de himelblau
        #Z = ((x1**2+x2-11)**2)+(x1+x2**2-7)**2
        #Z = x1**2+2*x2**2-0.3*np.cos(3*math.pi*x1)-0.4*np.cos(4*math.pi*x2)+0.7
        
        #fig=plt.figure(counter)  
        
        levels=[0,1,10,15,20,30,40,50,70,90,100,150,200,300,400,1500,2500,3500,5000,10000]
        plt.contour(x1,x2,Z,levels,cmap=cm.brg,zorder=-1)
        
        #print(idxBest)

        X=[b.solution[0] for b in self.particles]
        Y=[b.solution[1] for b in self.particles]
        plt.scatter(X,Y, marker='o',color='r')       
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.fig.clear()
              
                
                    
                        
                
                