#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:26:02 2017

@author: juan
"""

#This script implements the quadratic spline with inicial zero first derivative

import naturalCubicSpline as spln
import matplotlib.pyplot as plt
import numericalIntegral as nI
import math
z = (0.0, )
#sample =         (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
#functionValues = (1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def f(x):
    return math.exp(-(x ** 2))
#    return x ** 2

sample = nI.grid(-5, 5, 10)
functionValues = nI.evaluateFunction(sample, f)

for i in range(1, len(sample)):
    z += (-z[i - 1] + 2 * ((functionValues[i] - functionValues[i - 1]) / (sample[i] - sample[i - 1])), )
    
def spline(x):
    index = spln.closestIntervalIndex(x, sample)
    x_j = sample[index]
    x_j_1 = sample[index + 1]
    z_j = z[index]
    z_j_1 = z[index + 1]
    y_j = functionValues[index]
    constant = y_j
    linearTerm = z_j * (x - x_j)
    quadraticTerm = ((z_j_1 - z_j)/ 2 * (x_j_1 - x_j)) * ((x - x_j) ** 2)
    return constant + linearTerm + quadraticTerm

interpolationPoints = 100
interpolation = nI.grid(-4, 4, interpolationPoints)
interpolationValues = nI.evaluateFunction(interpolation, spline)


fig = plt.subplot()
fig.scatter(sample, functionValues, c = "r")
fig.scatter(interpolation, interpolationValues, alpha = 0.1)
plt.show()