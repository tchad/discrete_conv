'''
    Homework 2 CMPE242, derivative and low pass filter by convolution

    Author: Tomasz Chadzynski
    Version: v0.2
    Date: 4/17/19

    This task implements kernels used in discrete convolution.
    Kernel 1 computes a first derivative of the signal using the central difference approach.
    Kernel 2 Applies low pass filter to the signal. The filtering is implemented by applying gaussian smoothing technique.

     MODULE: Implementing discrete kernel based discrete convolution operator

'''


def convolve_odd_kern(x,k):
    k_len = len(k)
    L = int(k_len/2)
    R = L+1
    
    out = []
    for i in range(L,len(x)-L):
        sub = x[i-L:i+R]
        y = 0
        
        for i in range(len(sub)):
            y += sub[i] * k[i]

        out += [y]

    return out

