# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 19:56:11 2019

@author: GARIMA
"""

print("list of integers")

a = [int(x) for x in input().split()]
print(a)

print("The distinct numbers are:",list(set(a)))