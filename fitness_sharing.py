# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 08:31:05 2016

@author: stan
"""
import numpy as np
class FitnessSharing:


    @staticmethod
    def scale_fitness(population):
        sharing_domain = population.parameters['sharing.domain']
        theta_share = population.parameters['theta.share']
        environment = population.environment
        theta_share = (theta_share/100)* \
        (environment.get_chromosome_length() if \
        sharing_domain=='genotype' else 1)
        alpha = population.parameters['alpha.share']
        distance = FitnessSharing.count if sharing_domain=='genotype' \
        else population.environment.compute_distance
        individuals = population.individuals       
        distances = np.zeros((population.size,population.size))
        for i in range(0,population.size):
            for j in range(i,population.size):
                distances[i,j] = \
                distance(individuals[i],individuals[j])
                distances[j,i] = distances[i,j]
        sharing = np.vectorize(FitnessSharing.sharing_function) 
        scaled_fitness = \
        [population.individuals[i].fitness/ \
        sum(sharing(distances[i],theta_share,alpha)) \
        for i in range(0, population.size)]
        for i in range(0,population.size):
            population.individuals[i].fitness = scaled_fitness[i]
        
    @staticmethod
    def count(individual1,individual2):
        diff = individual1.genotype.chromosome^individual2.genotype.chromosome
        c = 0
        while(diff !=0 ):
            diff = diff&(diff-1)
            c = c + 1
        return c
        
    @staticmethod
    def sharing_function(distance,theta_share,alpha):
        return 1 - (distance/theta_share)**alpha if \
        distance < theta_share else 0
       
    @staticmethod
    def beta_scaling(population):
        beta = population.parameters['beta.fitness.scaling']
        for i in range(0,population.size):
            fitness = population.individuals[i].fitness
            population.individuals[i].fitness = fitness**beta
            
        