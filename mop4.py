# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 08:15:41 2016

@author: stan
"""
from environment import Environment
from multiobjective import MultiObjective
from decoding_tools import DecodingTools as dt
import numpy as np
import matplotlib.pyplot as plt
class MOP4(Environment,MultiObjective):
    
    def __init__(self,precision=15,n=3,interactive=False):
        self.n = n
        self.precision = precision
        self.interactive = interactive
        if(interactive):
            plt.ion()
    
    def evaluate(self,population):
        for individual in population.individuals:
            individual.objectives = \
            np.array([MOP4.f1(individual.phenotype),\
            MOP4.f2(individual.phenotype)])
        
    def decode(self,population):
        for individual in population.individuals:
            ch = individual.genotype.chromosome
            individual.phenotype = \
            np.array([\
            dt.decode_real(ch,0,self.precision,(-5,5)),\
            dt.decode_real(ch,self.precision,self.precision,(-5,5)),
            dt.decode_real(ch,2*self.precision,self.precision,(-5,5))])
            
    def get_chromosome_length(self):
        return self.precision*self.n
        
    def get_number_of_objectives(self):
        return 2
        
    def get_optimization_type(self):
        return np.array([-1,-1])
        
    @staticmethod
    def f1(x):
        n = len(x)
        return sum(-10*np.exp(-0.2*np.sqrt(x[:n-1]**2+x[1:n]**2)))
        
    def f2(x):
        #return sum(np.abs(x)**0.8 + 5*np.sin(x)**3)
        return sum(np.abs(x)**0.8 + 5*np.sin(x**3))
        
    def show(self,population,colors='blue',clear = True):

        if(clear):
            plt.clf()
        
        objectives =[x.objectives for x in population.individuals]
        X = [x.item(0) for x in objectives]
        Y = [x.item(1) for x in objectives]
        
        
        plt.scatter(X,Y,color=colors)
        plt.grid()
        if(self.interactive):
            plt.pause(0.05)
        else:
            plt.show()
        
        
        
    