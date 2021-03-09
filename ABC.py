# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 18:24:04 2019

@author: GabrielAsus
"""

import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import math

            
            
class Bee(object):
    def __init__(self,dimention,function,lower,upper):
        
        self.solution=[]        
        self.function=function
        self.dimention=dimention
        self.lower=lower
        self.upper=upper
        for i in range(self.dimention):
            self.solution.append(int(self.lower[i])+random.random()*(int(self.upper[i])-int(self.lower[i])))  
        self.getValue()
        #self.getFitness()
    def reStart(self):        
        self.solution=[]
        for i in range(self.dimention):
            self.solution.append(int(self.lower[i])+random.random()*(int(self.upper[i])-int(self.lower[i])))  
        self.getValue()
        self.getAptitud()
    def getValue(self):
        self.value=self.function(self.solution)
        self.getAptitud()           
    def getAptitud(self):
        if self.value>=0 :
            self.aptitud=1/(1+self.value)
        else:
            self.aptitud=1+abs(self.value)
            
class ArtifitialBC(object):
    
    def __init__(self,
                 dimention,
                 lower,
                 upper,
                 function,
                 populationSize,
                 maxIter,
                 ):
        #initialize the bees        
        self.bees=[Bee(dimention,function,lower,upper) for i in range(populationSize)]
        self.popF=int(populationSize/2)
        self.popO=int(populationSize/2)
        self.trialCounters=[0 for i in range(self.popF)]
        self.maxIter=maxIter
        self.populationSize=populationSize
        self.dimention=dimention
        self.function=function
        self.lower=lower
        self.upper=upper
        self.stagnationLimit=populationSize*dimention/2
        self.probability=0
        self.ims=[]
        plt.ion()
        self.fig= plt.figure()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
    def run(self):
        counter=0
        while(counter<self.maxIter):
            #employee bees
            for idxB in range(self.popF):
                k=random.randint(0,self.popF-1)
                while(idxB==k):
                    k=random.randint(0,self.popF-1)
                j=random.randint(0,self.dimention-1)
                phi=random.uniform(-1,1)
                vBee=Bee(self.dimention,self.function,self.lower,self.upper)
                                
                vBee.solution[j]=self.bees[idxB].solution[j]+phi*(self.bees[idxB].solution[j]-self.bees[k].solution[j])
                vBee.getValue()
                if(vBee.value<self.bees[idxB].value):   
                    self.bees[idxB].solution=vBee.solution
                    self.trialCounters[idxB]=0
                    self.bees[idxB].getValue()
                else:
                    self.trialCounters[idxB]+=1
            #onlooker bees
            for idxB in range(self.popO,self.populationSize):                
                
                #calculate de probability
                self.calculateProb()
                #seleccionar el indxBF
                selectedBF=self.selectRoulette()
                k=random.randint(0,self.popF-1)
                while(selectedBF==k):
                    k=random.randint(0,self.popF-1)
                s=random.randint(0,self.dimention-1)
                r=random.uniform(-1,1)
                self.bees[idxB].solution[s]=self.bees[selectedBF].solution[s]+r*(self.bees[selectedBF].solution[s]-self.bees[k].solution[s])
                self.bees[idxB].getValue()
                if(self.bees[idxB].value<self.bees[selectedBF].value):
                    self.bees[selectedBF]=self.bees[idxB]
                    self.trialCounters[selectedBF]=0
                else:
                    self.trialCounters[selectedBF]+=1
            #scout bees
            for idxB in range(self.popF):
                if(self.trialCounters[idxB]>self.stagnationLimit):
                    self.bees[idxB].reStart()
                    self.trialCounters[idxB]=0
            #select the best
            maxValue=sys.float_info.max
            idxBest=None
            for idx in range(self.populationSize):                
                if (self.bees[idx].value<maxValue):
                    idxBest=idx;
                    maxValue=self.bees[idx].value
            
            
            self.plotear(counter,idxBest)
            if(self.bees[idxBest].value<.005):
                #self.plotear(counter,idxBest)
                break
            counter+=1
        return self.bees[idxBest].solution,self.bees[idxBest].value
        
                    
    def calculateProb(self):
        sumFit=0
        for idxP in range(int(self.popF)):
            sumFit=self.bees[idxP].aptitud+sumFit
        for idxP in range(int(self.popF)):
            self.bees[idxP].probability=self.bees[idxP].aptitud/sumFit
                
    def selectRoulette(self):
        r=random.uniform(0,1)
        suma=0
        for idxR in range(int(self.popF)):
            if(suma+self.bees[idxR].probability>=r):
                return idxR
            else:
                suma=suma+self.bees[idxR].probability
        return idxR
    def plotear(self,counter,idxBest):       
        self.fig.clear()
        x1 = np.arange(-100, 100, 0.25)
        x2 = np.arange(-100, 100, 0.25)
        x1, x2 = np.meshgrid(x1, x2)

        #Z = ((x1**2+x2-11)**2)+(x1+x2**2-7)**2
        Z = x1**2+2*x2**2-0.3*np.cos(3*math.pi*x1)-0.4*np.cos(4*math.pi*x2)+0.7


        levels=[0,1,10,15,20,30,40,50,70,90,100,150,200,300,400,1500,2500,3500,5000,10000]
        plt.contour(x1,x2,Z,levels,cmap=cm.brg,zorder=-1)

        X=[b.solution[0] for b in self.bees]
        Y=[b.solution[1] for b in self.bees]
        plt.scatter(X,Y, marker='o',color='r')       
        plt.xlim(-100, 100)
        plt.ylim(-100, 100)
       # plt.savefig('ABC'+str(counter)+'.png')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        