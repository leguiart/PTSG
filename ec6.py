# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 19:46:35 2016

@author: stan
"""
from environment import Environment
from multiobjective import MultiObjective
from decoding_tools import DecodingTools as dt
import numpy as np
import matplotlib.pyplot as plt
class EC6(Environment,MultiObjective):
    
    def __init__(self,precision=15,n=10,interactive=False):
        self.n = n
        self.precision = precision
        self.interactive = interactive
        if(interactive):
            plt.ion()
    
    def evaluate(self,population):
        for individual in population.individuals:
            individual.objectives = \
            np.array([self.f1(individual.phenotype),\
            self.f2(individual.phenotype)])
        
    def decode(self,population):
        for individual in population.individuals:
            ch = individual.genotype.chromosome
            individual.phenotype = \
            np.array(dt.decode_real_list(ch,10,0,self.precision))
            
    def get_chromosome_length(self):
        return self.precision*self.n
        
    def get_number_of_objectives(self):
        return 2
        
    def get_optimization_type(self):
        return np.array([-1, -1])
        
    def f1(self,x):
        return 1-np.exp(-4*x[0])*(np.sin(6*np.pi*x[0])**6)
        
    def g(self,x):
        return 1 + 9*(np.sum(x[1:])/(self.n-1))**0.25
        
    def f2(self,x):
        g = self.g(x)
        f = self.f1(x)
        return g*(1 -(f/g)**2)
        
    def show(self,population=None,colors='blue',clear = True):
        
        if(clear):
            plt.clf()
            
        objectives =[x.objectives for x in population.individuals]
        X = [x.item(0) for x in objectives]
        Y = [x.item(1) for x in objectives]
        plt.scatter(X,Y,color=colors)
        
        X = np.linspace(0,1,100)
        Y= 1 - X**2
        plt.plot(X,Y,'red')
        
        plt.grid()
        if(self.interactive):
            plt.pause(0.05)
        else:
            plt.show()