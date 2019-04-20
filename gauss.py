'''
    Homework 2 CMPE242, derivative and low pass filter by convolution

    Author: Tomasz Chadzynski
    Version: v0.2
    Date: 4/17/19

    This task implements kernels used in discrete convolution.
    Kernel 1 computes a first derivative of the signal using the central difference approach.
    Kernel 2 Applies low pass filter to the signal. The filtering is implemented by applying gaussian smoothing technique.

     MODULE: Implementing gaussian distribution and helper functions

'''

import math as _m


def mean(x):
    s = 0.0

    for n in x:
        s += n

    return s/len(x)


def std_dev(x, u):
    p_sum = 0
    for n in x:
        p_sum += (n - u)*(n - u)

    return _m.sqrt(p_sum/(len(x)-1));


def g(x, u, s ):
    A = 1/(_m.sqrt(2*_m.pi)*s)
    E = -((x-u)**2)/(2*s*s)

    G = A * _m.exp(E)

    return G


def test_gauss(sigma=1, u=0):
    y = []
    rng = range(int(-5*sigma), int(5*sigma))
    for x in rng:
        y+= [g(x, u=u, s=sigma)]

    return (y,rng)

