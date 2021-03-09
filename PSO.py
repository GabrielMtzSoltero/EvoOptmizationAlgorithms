# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:21:49 2019

@author: GabrielAsus
"""

import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import math
import copy
import time
class particlePSO(object):
    def __init__(self,dimention,lower=None,upper=None):
        self.solution=[]    
        self.velocity=[]
        self.dimention=dimention
        self.lower=lower
        self.upper=upper
        for i in range(self.dimention):
            if(lower!=None and upper!=None):
                self.solution=np.append(self.solution,(random.uniform(lower[i],upper[i])))  
                self.velocity=np.append(self.velocity,random.random())
            else:
                self.solution=np.apppend(self.solution,float(random.random()))
                self.velocity=np.append(self.velocity,random.random())
        self.pBestSolution=self.solution
        self.value=sys.float_info.max
        self.pBestValue=sys.float_info.max
        #print(self.solution)
        
        
  
class PSO(object):
    def __init__(self,dimention,populationSize,lower,upper,function,maxIter,breakCriteria,wInertia=1,c1=2,c2=2,imagen=1):
        self.particles=[particlePSO(dimention,lower,upper) for i in range(populationSize)]
        self.maxIter=maxIter
        self.lower=lower
        self.upper=upper
        self.populationSize=populationSize
        self.function=function
        self.breakCriteria=breakCriteria
        self.gBest=particlePSO(dimention,lower,upper)
        self.wInertia=wInertia
        self.c1=c1
        self.c2=c2
        plt.ion()
        self.fig= plt.figure()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.imagen=imagen
        
    def run(self):
        counter=0
        random.seed(9001)
        while counter<self.maxIter:
            for idx in range(self.populationSize):
                
                self.particles[idx].value=self.function(self.particles[idx].solution)
                #print('actual ',self.particles[idx].value,'< mejor local ',self.particles[idx].pBestValue,'coordenadas',self.particles[idx].solution)
                if self.particles[idx].value<self.particles[idx].pBestValue:
                    self.particles[idx].pBestValue=self.particles[idx].value
                    self.particles[idx].pBestSolution=self.particles[idx].solution
                    
                    
                    
            for idx in range(self.populationSize):
                #print('actual ',self.particles[idx].value,'< mejor global ',self.gBest.value)
                if self.particles[idx].value<self.gBest.value:
                    self.gBest=copy.deepcopy(self.particles[idx])
                    idxBest=idx
            
            if self.gBest.value<self.breakCriteria:
                print(self.gBest.solution)
                return self.gBest.solution,self.gBest.value
            
            for idx in range(self.populationSize):
                self.particles[idx].velocity=self.wInertia*self.particles[idx].velocity+random.random()*self.c1*(self.particles[idx].pBestSolution-self.particles[idx].solution)+random.random()*self.c2*(self.gBest.solution-self.particles[idx].solution)
                self.particles[idx].solution=self.particles[idx].solution+self.particles[idx].velocity

            
            
            
            counter+=1
            self.plotear(counter,idxBest)
        print(self.gBest.solution)    
        return [self.gBest.solution],self.gBest.value
    
    def plotear(self,counter,idxBest):       
        time.sleep(.1)
        X0 = np.arange(-10, 10, 0.25)
        X1 = np.arange(-10, 10, 0.25)
        X0, X1 = np.meshgrid(X0, X1)
        ax = plt.axes(projection='3d')
        Z = X0**2+2*X1**2-0.3*np.cos(3*math.pi*X0)-0.4*np.cos(4*math.pi*X1)+0.7
        ax.plot_wireframe(X0, X1, Z,rstride=5, cstride=5,cmap='viridis')
        X=[b.solution[0] for b in self.particles]
        Y=[b.solution[1] for b in self.particles]
        Z=[b.value for b in self.particles]
      
        ax.scatter(X,Y,Z, marker='o',color='r')       
        
        ax.set_xlim3d(-10, 10)
        ax.set_xlabel('x0')
        ax.set_ylim3d(-10, 10)
        ax.set_ylabel('x1')
        ax.set_zlabel('valor')
        ax.set_zlim3d(-1, 300)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
              
                
                
        