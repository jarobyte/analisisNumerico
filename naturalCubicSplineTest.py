#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 12:33:50 2017

@author: juan
"""

import naturalCubicSpline as spline
import numericalIntegral as nI
import matplotlib.pyplot as plt
import math


l = -4
u = 4
samplePoints = 10
interpolationPoints = 200


def f(x):
    return math.exp(-(x ** 2))

sample = nI.grid(l, u, samplePoints)
functionValues = nI.evaluateFunction(sample, f)

#sample = (-1, 0, 1, 2)
#functionValues = (1, 0, 1, 4)

def g(x):
    return spline.naturalCubicSpline(x, sample, functionValues)

interpolation = nI.grid(l,u, interpolationPoints)
interpolationValues = nI.evaluateFunction(interpolation, g)

fig = plt.subplot()
fig.scatter(interpolation, interpolationValues, alpha = 0.1)
fig.scatter(sample, functionValues, color = "r")

plt.show()