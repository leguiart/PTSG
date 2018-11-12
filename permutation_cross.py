# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 00:30:32 2016

@author: stan
"""
from numpy import random
from individual import Individual
import numpy as np
class PermutationCrossover:
    
    #Partially-mapped crossover
    @staticmethod
    def pmx_crossover(individual1,individual2):
        n,i,f,i_central,i_sides= PermutationCrossover.mapping_sections(\
        individual1,individual2)
        child1,child2 = PermutationCrossover.child_templates(n)
        map_1_2,map_2_1 = PermutationCrossover.find_mappings(\
        i_central,individual1,individual2)
        
        child1[i_central]= individual2.phenotype[i_central]
        child2[i_central]= individual1.phenotype[i_central] 

        sides = list(filter(lambda x: x not in i_central,\
        range(0,n)))        
        
        child1[sides] = [i if i not in map_2_1.keys() else\
        PermutationCrossover.alternative(i,map_2_1) \
        for i in individual1.phenotype[sides]]
        child2[sides] = [i if i not in map_1_2.keys() else\
        PermutationCrossover.alternative(i,map_1_2) \
        for i in individual2.phenotype[sides]]
        return [Individual(phenotype=child1),Individual(phenotype=child2)]
        
    @staticmethod
    def cx_crossover(individual1,individual2):
        n = len(individual1.phenotype)
        child1= individual2.phenotype.copy()
        child2= individual1.phenotype.copy()
        city_pos = 0
        map_1 = {individual1.phenotype[i]:i for i in range(0,n)}
        while(True):
            city_pos = PermutationCrossover.apply_mapping(\
            child1,child2,individual1,individual2,city_pos,map_1)
            if(map_1[individual2.phenotype[city_pos]] is 0):
                PermutationCrossover.apply_mapping(\
                child1,child2,individual1,individual2,city_pos,map_1)
                break
        return  [Individual(phenotype=child1),Individual(phenotype=child2)]
        
    @staticmethod
    def apply_mapping(child1,child2,individual1,individual2,city_pos,map_1):
        child1[city_pos] = individual1.phenotype[city_pos]
        child2[city_pos] = individual2.phenotype[city_pos]
        return map_1[individual2.phenotype[city_pos]]
        
    #Order crossover        
    @staticmethod
    def ox_crossover(individual1,individual2):
        n,i,f,i_central,i_sides= PermutationCrossover.mapping_sections(\
        individual1,individual2)
        
        p1_central = set(individual1.phenotype[i_central])
        p2_central = set(individual2.phenotype[i_central])
        centrals = p1_central.union(p2_central)
        
        rest_1 = list(filter(lambda x:x[1] not in centrals, \
        enumerate(individual1.phenotype)))
        rest_2 = list(filter(lambda x:x[1] not in centrals, \
        enumerate(individual2.phenotype)))
        
        rest_1 = np.array([x[1] for x in \
        list(filter(lambda x:x[0]>=f,rest_1))+\
        (list(filter(lambda x:x[0]<i,rest_1)))])

        rest_2 = np.array([x[1] for x in \
        list(filter(lambda x:x[0]>=f,rest_2))+\
        (list(filter(lambda x:x[0]<i,rest_2)))])
        
        head_1 = np.array(list(filter(lambda x:x not in p2_central,\
        individual1.phenotype[i_central])))
        
        head_2 = np.array(list(filter(lambda x:x not in p1_central,\
        individual2.phenotype[i_central])))
        
        child1 = PermutationCrossover.build_child(\
        head_1,individual2.phenotype[i_central],rest_1)
        
        child2= PermutationCrossover.build_child(\
        head_2,individual1.phenotype[i_central],rest_2)
         
        return [Individual(phenotype=child1),Individual(phenotype=child2)]
        
    @staticmethod
    def build_child(head,middle,rest):
        if head.size>0 and rest.size>0:
            return np.concatenate((head,middle,rest))
        elif head.size>0 and rest.size==0:
            return np.concatenate((head,middle))
        elif head.size==0 and rest.size>0:
            return np.concatenate((middle,rest))
        else:
            return middle
        
        
    @staticmethod
    def ox1_crossover(individual1,individual2):
        n,i,f,i_central,i_sides= PermutationCrossover.mapping_sections(\
        individual1,individual2)
        child1,child2 = PermutationCrossover.child_templates(n) 

        p1_central = set(individual1.phenotype[i_central])
        p2_central = set(individual2.phenotype[i_central])

        child1[i_central]= individual1.phenotype[i_central]
        child2[i_central]= individual2.phenotype[i_central]        
        child1[i_sides[:n-(f-i)-1]] = list(filter(lambda x:x not in p1_central,\
        individual2.phenotype[i_sides]))
        child2[i_sides[:n-(f-i)-1]] = list(filter(lambda x:x not in p2_central,\
        individual1.phenotype[i_sides])) 
        return [Individual(phenotype=child1),Individual(phenotype=child2)]
        
    @staticmethod
    def ox2_crossover(individual1,individual2):
        n,poss = PermutationCrossover.random_crossover_points(\
        individual1,individual2)

        child1 = np.copy(individual1.phenotype)
        child2 = np.copy(individual2.phenotype)
        
        p_1 = individual1.phenotype[poss]
        p_2 = individual2.phenotype[poss]

        pos_1 = [i[0] for i in enumerate(individual1.phenotype) \
        if i[1] in set(p_2)]
        pos_2 = [i[0] for i in enumerate(individual2.phenotype) \
        if i[1] in set(p_1)]
        child1[pos_1]= p_2    
        child2[pos_2]= p_1
        return [Individual(phenotype=child1),Individual(phenotype=child2)]

    @staticmethod
    def random_crossover_points(individual1,individual2):
        n = len(individual1.phenotype)
        #sorted unique indices 
        poss = np.unique(np.random.choice(list(range(0,n)),\
        np.random.randint(1,n)))        
        return (n,poss)
        
    @staticmethod
    def pos_crossover(individual1,individual2):
        n,poss = PermutationCrossover.random_crossover_points(\
        individual1,individual2)
        child1,child2 = PermutationCrossover.child_templates(n)
        
        child1[poss]=individual2.phenotype[poss]
        child2[poss]=individual1.phenotype[poss]

        
        poss_set = set(poss)        
        p1_sel = set(individual1.phenotype[poss])
        p2_sel = set(individual2.phenotype[poss])
        pos_res = list(filter(lambda x:x not in poss_set,range(0,n)))

        rest_1 = list(filter(lambda x:x not in p2_sel,individual1.phenotype))
            
        rest_2 = list(filter(lambda x:x not in p1_sel,individual2.phenotype))

        child1[pos_res] = rest_1
        child2[pos_res] = rest_2
        return [Individual(phenotype=child1),Individual(phenotype=child2)]
        
    @staticmethod
    def pmx_grefenstette_crossover(individual1,individual2):
        n,i,f,i_central,i_sides= PermutationCrossover.mapping_sections(\
        individual1,individual2)
        child1_central = individual2.phenotype[i_central]
        child2_central = individual1.phenotype[i_central]
        p1_central = set(child1_central)
        p2_central = set(child2_central)
        child1_rest = np.array(list(filter(lambda x:x not in p1_central,\
        individual1.phenotype)))
        child2_rest = np.array(list(filter(lambda x:x not in p2_central,\
        individual1.phenotype)))
        pos_1 = np.where(individual1.phenotype==child1_central[0])[0][0]
        pos_2 = np.where(individual2.phenotype==child2_central[0])[0][0]
        child1 = PermutationCrossover.build_child(child1_rest[:pos_1],\
        child1_central,child1_rest[pos_1:])
        child2 = PermutationCrossover.build_child(child2_rest[:pos_2],\
        child2_central,child2_rest[pos_2:])
        return [Individual(phenotype=child1),Individual(phenotype=child2)]
        
    @staticmethod
    def mapping_sections(individual1,individual2):
        n = len(individual1.phenotype)
        i,f = np.sort(random.randint(0,n,2))
        i_central = list(range(i,f+1))
        i_sides = [i%n for i in range(f+1,n+f+1)]
        return (n,i,f,i_central,i_sides)
        
    @staticmethod
    def find_mappings(i_central,individual1,individual2):
        map_1_2 = {individual1.phenotype[i]:individual2.phenotype[i] \
        for i in i_central}
        map_2_1 = {individual2.phenotype[i]:individual1.phenotype[i] \
        for i in i_central}
        return (map_1_2,map_2_1)
        
    @staticmethod
    def alternative(city,map):
        while(city in map.keys()):
            city = map[city]
        return city
        
        
    @staticmethod
    def child_templates(n):
        return ( np.array([0]*n), np.array([0]*n))
        
        