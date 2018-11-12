# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 10:29:57 2016

@author: stan
"""
from abc import ABCMeta, abstractmethod
class MultiObjective:
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_number_of_objectives(self):
        pass
    
    @abstractmethod
    def get_optimization_type(self):
        pass