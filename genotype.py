# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 09:17:49 2016

@author: stan
"""
from struct import unpack
from os import urandom
from functools import reduce
from math import ceil

class Genotype:
    def __init__(self,n,chromosome=None):
        self.n = n
        if(chromosome != None):
            self.chromosome = chromosome
        else:          
            if(self.n==64):
                chromosome = unpack("!Q",urandom(8))[0]
            elif(self.n<64):
                chromosome = unpack("!Q",urandom(8))[0] & \
                ((1<<self.n)-1)
            else:
                m = ceil(self.n/64)
                rand = [0]+[unpack("!Q",urandom(8))[0] for i in range(0,m)]
                chromosome = reduce(lambda x,y:(x<<64)|y,rand) &\
                ((1<<self.n)-1)
            self.chromosome = chromosome
    
    def __str__(self):
        return ("{0:0"+str(self.n)+"b}").format(self.chromosome)
            
