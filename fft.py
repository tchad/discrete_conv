'''
    Homework 2 CMPE242, derivative and low pass filter by convolution

    Author: Tomasz Chadzynski
    Version: v0.2
    Date: 4/17/19

    This task implements kernels used in discrete convolution.
    Kernel 1 computes a first derivative of the signal using the central difference approach.
    Kernel 2 Applies low pass filter to the signal. The filtering is implemented by applying gaussian smoothing technique.

     MODULE: Module implementing input parsing, fft dft and power spectrum calculations

    Based on the CMPE242 implementation fft.c

'''

import math

class Cplx():
    def __init__(self, _re = 0, _im = 0):
        self.re = _re;
        self.im = _im;

def prep_input(data):
    N = len(data)
    
    #create array of input data with complex type and size power of 2

    #ensure 2^M size, pad additional with zeros
    log2N = math.log2(N)
    if (log2N % 1) != 0:
        print('fft.prep_input: input dataset padding')
        M = int(log2N) + 1
        N = 2**M
    else:
        print('fft.prep_input: input dataset correct size')
        M = log2N

    X = []

    for i in range(0, N):
        if i < len(data):
            tmp = Cplx(data[i],0)
            X += [tmp]
        else:
            X += [Cplx()]

    return X

def fft(X):
    #decimation in frequency FFT

    N = len(X);
    M = int(math.log2(N))

    for k in range(0, M):
        LE = 2**(M - k)
        LE1 = int(LE/2)

        U = Cplx(1.0, 0.0)

        W = Cplx()
        W.re = math.cos(math.pi/LE1)
        W.im = -math.sin(math.pi/LE1)

        for j in range(0, LE1):
            for i in range(j, N, LE):
                IP = i + LE1

                T = Cplx()
                T.re = X[i].re + X[IP].re
                T.im = X[i].im + X[IP].im

                Tmp = Cplx()
                Tmp.re = X[i].re - X[IP].re
                Tmp.im = X[i].im - X[IP].im

                X[IP].re = (Tmp.re * U.re) - (Tmp.im * U.im)
                X[IP].im = (Tmp.re * U.im) + (Tmp.im * U.re)

                X[i].re = T.re
                X[i].im = T.im 

            Tmp = Cplx()
            Tmp.re = (U.re * W.re) - (U.im * W.im)
            Tmp.im = (U.re * W.im) + (U.im * W.re)

            U.re = Tmp.re
            U.im = Tmp.im

    Xs = X
    X = []

    for i in range(len(Xs)):
        i_str = '{:0{w}b}'.format(i, w=M)
        idx_str = i_str[::-1]
        idx = int(idx_str,2)
        X += [Xs[idx]]


    for i in range(len(X)):
        X[i].re /= N
        X[i].im /= N
            
    return X

def pwr_spectrum(cplx_freq):
    pwr= []

    for h in cplx_freq:
        tmp = (h.re**2 + h.im**2)**(1.0/2.0)
        pwr += [tmp]

    return pwr

def dft(X):
    Y = []
    N = len(X)

    for m in range(N):
        if m != 0:
            print(math.log2(m))
        s = Cplx();
        for n in range(N):
            s.re += X[n].re * math.cos((2 * math.pi * m * n)/N)
            s.im += -X[n].re * math.sin((2 * math.pi * m * n)/N)

        s.re /= N
        s.im /= N

        Y += [s]

    return Y

