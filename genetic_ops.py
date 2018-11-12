# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 10:49:31 2016

@author: stan
"""
from random import randint
from genotype import Genotype
from numpy import random
from population import Population
from individual import Individual
from selection import Selection
from permutation_cross import PermutationCrossover
import numpy as np
class GeneticOperators: 
    
    selections={"tournament.selection":Selection.tournament,
                "roulettewheel.selection":Selection.roulettewheel,
                "ranking.selection":Selection.ranking,
                "pareto.tournament":Selection.pareto_tournament}  
                
    permutations={"permutation.ox":PermutationCrossover.ox_crossover,
                  "permutation.ox1":PermutationCrossover.ox1_crossover,
                  "permutation.ox2":PermutationCrossover.ox2_crossover,
                  "permutation.pmx":PermutationCrossover.pmx_crossover,
                  "permutation.pmx.grefenstette":
                      PermutationCrossover.pmx_grefenstette_crossover,
                  "permutation.pos":PermutationCrossover.pos_crossover,
                  "permutation.cx":PermutationCrossover.cx_crossover}
    
    keys = list(permutations.keys())
    @staticmethod
    def crossover(population):
        #assumes individuals are shuffled
        new_pop = []
        for i in range(0,population.size>>1):
            individual1 = population.individuals[i]
            individual2 = population.individuals[population.size-i-1]
            if(random.uniform() < population.parameters['p.crossover']):
                type = population.parameters['crossover.type'] \
                if (population.parameters['crossover.type'] \
                != 'permutation.all.operators') else \
                np.random.choice(GeneticOperators.keys)
                children = GeneticOperators.permutation_crossover_individuals(\
                individual1,individual2,type) \
                if(population.parameters['type']=='permutation') else \
                GeneticOperators.crossover_individuals(\
                individual1,individual2)
            else:
                children = [\
                Individual(individual1.genotype,\
                np.array(individual1.phenotype)),\
                Individual(individual2.genotype,\
                np.array(individual2.phenotype))]
            new_pop = new_pop + children
        return \
        Population(population.environment, population.parameters,new_pop)
    
    @staticmethod
    def crossover_individuals(individual1,individual2,type = 'single'):
        genotype1 = individual1.genotype
        genotype2 = individual2.genotype
        crossp = randint(1,genotype1.n-1)
        mask1 = ((1<<(genotype1.n-crossp))-1)<< crossp
        mask2 = (1<<crossp)-1
        ch1 = mask1&genotype1.chromosome|mask2&genotype2.chromosome
        ch2 = mask1&genotype2.chromosome|mask2&genotype1.chromosome
        child1 = Genotype(genotype1.n,ch1)
        child2 = Genotype(genotype1.n,ch2)
        return [Individual(child1),Individual(child2)]
        
    @staticmethod
    def permutation_crossover_individuals(individual1,individual2,type):
        return GeneticOperators.permutations[type](individual1,individual2)
        
    @staticmethod
    def mutate_in_place(population):
        if(population.parameters['type']=='permutation'):
            length = len(population.individuals[0].phenotype)
            mutations = random.binomial(length*population.size,\
            population.parameters['p.mutation'])
            to_mutate = [(randint(0,population.size-1),randint(0,length-1),\
            randint(0,length-1)) for i in range(0,mutations)]
            for ind,a,b in to_mutate:
                temp = population.individuals[ind].phenotype[a]
                population.individuals[ind].phenotype[a] = \
                population.individuals[ind].phenotype[b]
                population.individuals[ind].phenotype[b] = temp
        else:
            length = population.environment.get_chromosome_length();
            mutations = random.binomial(length*population.size,\
            population.parameters['p.mutation'])
            to_mutate = [(randint(0,population.size-1),randint(0,length-1)) \
            for i in range(0,mutations)]
            for ind,pos in to_mutate:
                population.individuals[ind].genotype.chromosome = \
                population.individuals[ind].genotype.chromosome^(1<<pos)
            
    @staticmethod
    def select(population):
        selection_method = \
        GeneticOperators.selections[population.parameters['selection.type']]
        return selection_method(population)
            
                
                
            
            
            
            
        
        
