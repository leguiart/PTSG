# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:46:33 2016

@author: stan
"""
from abc import ABCMeta, abstractmethod
class Environment:
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def evaluate(self,population):
        pass
        
    @abstractmethod
    def get_gene_template(self):
        pass
    
    @abstractmethod
    def compute_distance(self,individual1,individual2):
        pass
    
    @abstractmethod
    def compute_normalized_distance(self,individual1,individual2):
        pass
        
    @abstractmethod
    def decode(self,population):
        pass
        
    @abstractmethod
    def get_chromosome_length(self):
        pass
    