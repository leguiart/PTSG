# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 09:17:49 2016

@author: stan
"""
from genetic_ops import GeneticOperators
from population import Population
from fitness_sharing import FitnessSharing
from niche_clearing import NicheClearing
from selection import Selection
import warnings
class GeneticAlgorithm:
    def __init__(self,environment,parameters):
        self.parameters = parameters
        self.environment = environment
        self.population = Population(environment,parameters)
        self.environment.decode(self.population)
        self.environment.evaluate(self.population)
        self.scale_fitness(self.population)
        
    def evolve(self):
        for i in range(0,self.parameters['n.generations']):
            mating_pool = GeneticOperators.select(self.population)       
            new_pop = GeneticOperators.crossover(mating_pool)
            GeneticOperators.mutate_in_place(new_pop)
            self.environment.decode(new_pop)
            self.environment.evaluate(new_pop)
            self.scale_fitness(new_pop)

            if('elitism' in self.parameters and \
            self.parameters['elitism']):        
                if(self.population.parameters['type']== \
                'nsga-ii'):
                    union = Population(self.population.environment,\
                    self.population.parameters,\
                    self.population.individuals+new_pop.individuals)
                    new_pop = Selection.pareto_crowded(union)
                else:
                    new_pop =\
                    Population(self.population.environment,\
                    self.population.parameters,\
                    sorted(self.population.individuals+new_pop.individuals,\
                    key=lambda x:x.fitness,reverse=True)\
                    [:self.population.size])
                
            self.population = new_pop
            
            self.report(i,self.parameters['n.generations'])
            
        self.report()


    def scale_fitness(self,population):
            if('fitness.scaling' in self.parameters and \
            self.parameters['fitness.scaling']):
                FitnessSharing.beta_scaling(population)
            if('fitness.sharing' in self.parameters and \
            self.parameters['fitness.sharing']):
                FitnessSharing.scale_fitness(population)
            if('niche.clearing' in self.parameters and \
            self.parameters['niche.clearing']):
                NicheClearing.scale_fitness(population)
                
    def report(self,generation=0,total=0):
        step = max(1,int(total/10))
        progress = int(generation/step) if step != 0 else 100
        if(generation==total):
            print('\r'*80+'Done'+' '*76)
            self.plot()
        elif(generation%step==0):
            print('\r'*80+"Progress: {num:02d}%".format(\
            num=progress*10)+\
            " ["+chr(187)*int(progress*5)+chr(183)*(10*5-int(progress*5))+\
            "]",end="")
            self.plot()
            
    def plot(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if(hasattr(self.environment,'show')):
                self.environment.show(self.population,clear=True)
    
                
            
        