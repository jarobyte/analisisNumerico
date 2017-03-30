#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 14:29:12 2017

@author: juan
"""

#this script implements the natural cubic spline in a computationally efficient way

import clampedCubicSpline as spline
import numericalIntegral as nI
import matplotlib.pyplot as plt

#sample = (-1, 0, 1, 2)
#functionValues = (1, 0, 1, 4)
sample =         (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
functionValues = (1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1)


# Careful choice to determine the polynomial coefficients
x = nI.evaluationPoint(sample, 0.5)



derivatives = spline.secondDerivatives(sample, functionValues)

coeficientsList = []

for y in x:
    closest = spline.closestIntervalIndex(y, sample)
    x_j = sample[closest]
    x_j_1 = sample[closest + 1]
    f_x_j = functionValues[closest]
    f_x_j_1 = functionValues[closest + 1]
    f_2_x_j = derivatives[closest]
    f_2_x_j_1 = derivatives[closest + 1]
    coefficients = spline.cubicPolynomialCoefficients(x_j, x_j_1,f_x_j, f_x_j_1, f_2_x_j, f_2_x_j_1)
    coeficientsList.append(coefficients)

def spln(x):
    closestIntervalIndex = spline.closestIntervalIndex(x, sample)
    coeficients = coeficientsList[closestIntervalIndex]
    return spline.polynomialFromCoefficients(x, coeficients)



l = -1
u = 11

interpolationPoints = 20000
interpolation = nI.grid(l,u, interpolationPoints)
interpolationValues = nI.evaluateFunction(interpolation, spln)
                                          
fig = plt.subplot()
fig.scatter(interpolation, interpolationValues, alpha = 0.1)
fig.scatter(sample, functionValues, color = "r")

plt.show()