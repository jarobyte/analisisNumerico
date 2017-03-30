#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 14:11:25 2017

@author: juan
"""

#This program implements the clamped cubic spline with zero first derivative at the 
#endpoints

import numpy as np

lowerFirstDerivative = 0.0
upperFirstDerivative = 0.0


def deltaGrid(grid):
    deltas = ()
    for i in range(1, len(grid)):
        deltas += (grid[i] - grid[i - 1], )
    return deltas

def vectorLinearRelation(functionValues, deltas):
    b = np.array(range(len(deltas) - 1))
    for j in range(len(b)):
        b[j] = 6 * (((functionValues[j + 2] - functionValues[j + 1])/(deltas[j + 1])) 
        - ((functionValues[j + 1] - functionValues[j])/(deltas[j])))
    return b

def vector(functionValues, deltas):
    a = np.array([functionValues[1] - functionValues[0] - lowerFirstDerivative * deltas[0]])
    c = np.array([upperFirstDerivative * deltas[-1] + functionValues[-2] - functionValues[-1]])
    b = vectorLinearRelation(functionValues, deltas)
    return np.concatenate((a, b, c))

def matrixLinearRelation(rowLength, j, deltas):
    a = np.array([deltas[j + 1], 2 * (deltas[j] + deltas[j + 1]), deltas[j]])
    b = np.array([0])
    c = a
    for i  in range(j):
        c = np.concatenate((b, c))
    for i in range(rowLength - (j + 2)):
        c = np.concatenate((c, b))
    return c

def matrix(deltas):
    firstRow = np.array([(((deltas[0]) ** 2) / 3), (((deltas[0]) ** 2) / 6)])
    lastRow = np.array([(((deltas[-1]) ** 2) / 6), (((deltas[-1]) ** 2) / 3)])
    zero = np.array([0])
    for i in range(len(deltas) - 1):
        firstRow = np.concatenate((firstRow, zero))
    for i in range(len(deltas) - 1):
        lastRow = np.concatenate((zero, lastRow))
    matrix = firstRow
    for i in range(len(deltas) - 1):
        matrix = np.vstack((matrix, matrixLinearRelation(len(deltas), i, deltas)))
    matrix = np.vstack((matrix, lastRow))
    return matrix

def secondDerivatives(grid, functionValues):
    deltas = deltaGrid(grid)
    y = vector(functionValues, deltas)
    matriz = matrix(deltas)
    sigmas = np.linalg.solve(matriz, y)
    return sigmas

def cubicPolynomialCoefficients(lowerLimit, upperLimit,
                               lowerLimitValue, upperLimitValue, 
                               lowerDerivative, upperDerivative):
     A = np.matrix([[1, lowerLimit, lowerLimit ** 2, lowerLimit ** 3], 
                                   [1, upperLimit, upperLimit ** 2, upperLimit ** 3], 
                                   [0, 0, 2, 6 * (lowerLimit ** 1)], 
                                   [0, 0, 2, 6 * (upperLimit ** 1)]])
     y = np.array([lowerLimitValue, upperLimitValue, lowerDerivative, upperDerivative])
     x = np.linalg.solve(A, y)
     return x

def closestIntervalIndex(x, grid):
    for i in range(len(grid) - 1):
        if grid[i] <= x and x <= grid[i + 1]:
            return i
    if x < grid[0]:
        return 0
    return len(grid)-2

def polynomialFromCoefficients(x, coeficients):
    value = 0.0
    for i in range(len(coeficients)):
        value += coeficients[i] * (x ** i)
    return value

def spline(x, sample, functionValues):
    closest = closestIntervalIndex(x, sample)
    derivatives = secondDerivatives(sample, functionValues)
    x_j = sample[closest]
    x_j_1 = sample[closest + 1]
    f_x_j = functionValues[closest]
    f_x_j_1 = functionValues[closest + 1]
    f_2_x_j = derivatives[closest]
    f_2_x_j_1 = derivatives[closest + 1]
    coefficients = cubicPolynomialCoefficients(x_j, x_j_1, 
                                             f_x_j, f_x_j_1, 
                                             f_2_x_j, f_2_x_j_1
                                             )
    spline = polynomialFromCoefficients(x, coefficients)
    return spline
