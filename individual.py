# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:22:10 2016

@author: stan
"""
class Individual:
    def __init__(self,genotype=None,phenotype=None):
        self.genotype = genotype
        self.phenotype = phenotype
        
    def __str__(self):
        return  \
        (('genotype: '+ str(self.genotype)) \
        if self.genotype is not None else '') + \
        (('phenotype: '+ str(self.phenotype)) \
        if self.phenotype is not None else '') + \
        (('fitness: ' + str(self.fitness)) \
        if hasattr(self,'fitness') else '') + \
        (('objectives: '+str(self.objectives))
        if hasattr(self,'objectives') else '')
        