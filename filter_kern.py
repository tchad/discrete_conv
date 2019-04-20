'''
    Homework 2 CMPE242, derivative and low pass filter by convolution

    Author: Tomasz Chadzynski
    Version: v0.2
    Date: 4/17/19

    This task implements kernels used in discrete convolution.
    Kernel 1 computes a first derivative of the signal using the central difference approach.
    Kernel 2 Applies low pass filter to the signal. The filtering is implemented by applying gaussian smoothing technique.

     MODULE: various filtering kernels

'''

from gauss import g

def gen_kern_centr_diff():
    return [-0.5, 0.0, 0.5]

def gen_kern_gaussian_2nd_derivative(s=1 , u=0):
    kern = [
            g(-2,u,s)/4.0,
            0,
            -2.0*g(0,u,s)/4.0,
            0,
            g(2,u,s)/4.0
           ]

    return kern

def gen_kern_gaussian_smoothing_lpf_1D(s=1 , u=0):
    kern = [
            g(-2,u,s),
            g(-1,u,s),
            g(0,u,s),
            g(1,u,s),
            g(2,u,s)
           ]

    scale = sum(kern)
    kern  = [x/scale for x in kern]

    return kern

