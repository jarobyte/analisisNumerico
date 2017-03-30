#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 15:48:46 2017

@author: juan
"""
#1

#def f(x):
#    return x ** 3 - 3
#
#def f_1(x):
#    return 3 * x ** 2
#
#x = 1.5
#
#for i in range(40):
#   x = x - (f(x) / f_1(x))
#   print(x)
#   
#print("the cubic root of 4 is: " + str(x))
#print(x ** 3)

#3


import math
import numpy as np

def f(x):
    return np.array([x[0] ** 2 + x[1] ** 2 + x[2] ** 2, 
                     x[0]*x[1]*x[2], 
                     x[0] - x[1] - math.sin(x[2])])

def jacobian(x):   
    return np.array([[2*x[0], 2*x[1], 2*x[2]], 
                     [x[1]*x[2], x[0]*x[2], x[0]*x[1]], 
                     [1, -1, -math.cos(x[2])]])

x = np.array([0.1, 0.2, 0.3])

def inverseJacobian(x):
    return np.linalg.inv(jacobian(x))

def mul(x, y):
    return np.dot(x, y)
z = x
for i in range(10):
    m = inverseJacobian(z)
    print(mul(m, jacobian(z)))
    print()
    y = f(z)
    z = z - mul(m, y)
    print(f(z))
    print("*****")
    