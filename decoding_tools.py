# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 10:25:43 2016

@author: stan
"""

class DecodingTools:
    @staticmethod
    def decode_integer(chromosome,position,size):
        mask = ((1<<size)-1)<<position
        return (chromosome&mask)>>position
    @staticmethod
    def decode_real_list(chromosome,n,position,size,interval=None):
        return [\
        DecodingTools.decode_real(chromosome,position+size*i,size,interval)\
        if(interval !=None) else \
        DecodingTools.decode_normalized_real(chromosome,position+size*i,size)\
        for i in range(0,n)]
        
    @staticmethod
    def decode_real(chromosome,position,size,interval):
        return (interval[1]-interval[0])* \
        DecodingTools.decode_normalized_real(chromosome,position,size) \
        +interval[0]
        
    @staticmethod
    def decode_normalized_real(chromosome,position,size):
        x = DecodingTools.decode_integer(chromosome,position,size)
        return x/((1<<(size))-1)