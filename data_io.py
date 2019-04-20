'''
    Homework 2 CMPE242, derivative and low pass filter by convolution

    Author: Tomasz Chadzynski
    Version: v0.2
    Date: 4/17/19

    This task implements kernels used in discrete convolution.
    Kernel 1 computes a first derivative of the signal using the central difference approach.
    Kernel 2 Applies low pass filter to the signal. The filtering is implemented by applying gaussian smoothing technique.

     MODULE: Implementation of file I/O and plotting

'''

import re
import math
import matplotlib.pyplot as plt


def read_raw_data(filename):
    rf = open(filename)
    rf_str = rf.read()
    rf.close()

    rf_str = re.sub('\s+', ' ', rf_str).strip()
    rf_array = rf_str.split(' ')

    rf_data = [float(x) for x in rf_array]

    return rf_data


def plot_raw(data, title='ADC raw data', markersize=1, custom_range = None):
    if custom_range == None:
        rng = range(len(data))
    else:
        rng = custom_range
    plt.style.use('grayscale')
    plt.plot(rng, data, '.', markersize=markersize, label="RAW")
    plt.xlabel('Sample index')
    plt.ylabel('ADC output')
    plt.title(title)
    plt.legend()
    plt.show()

def plot_pwr_spectrum(data, title='Power spectrum', no_dc=False, markersize=1):
    x = range(len(data))
    if no_dc == True:
        begin = 1
        title_part = ' without DC component' 
    else:
        title_part = ' with DC component' 
        begin = 0

    plt.style.use('grayscale')
    plt.plot(x[begin:], data[begin:], '.', markersize=markersize, label="raw")
    plt.xlabel('Frequency index')
    plt.ylabel('Power')
    plt.title(title + title_part)
    plt.show()

def plot_pwr_spectrum_log(data, title='Power spectrum', markersize=1):
    x = range(len(data))
    px = [math.log(i,2) for i in x[1:int(len(x)/2)+1]]
    py = data[1:int(len(data)/2)+1]

    len(px)
    len(py)

    plt.style.use('grayscale')
    plt.plot(px, py, '.', markersize=markersize, label="raw")
    plt.xlabel('Frequency index [log2]')
    plt.ylabel('Power')
    plt.title(title)
    plt.show()

def print_signal_properties(pwr, signal_spec=0.9, title=''):
    print(title)
    print('DC %d' % pwr[0])
    print('HI_FREQ idx %d' % (len(pwr)/2-1))
    print("P HI_FREQ %d" % pwr[int(len(pwr)/2-1)])

    #compute power index
    m = int((len(pwr)/2)-1)
    m0 = int(m * signal_spec);

    print("-----------------------")
    print('signal spec %f' % signal_spec)
    print("Highest FREQ idx: %d" % m)
    print("Signal FREQ idx: %d" % m0)

    del_m0 = 0
    del_m = 0

    #for i in range(0, m0+1):
    for i in range(0, m0+1):
        del_m0 += pwr[i]

    for i in range(0, m+1):
        del_m += pwr[i]

    n = del_m0/del_m

    print("n idx: %f" % n)


def gen_sin(s_period = 128, num_periods = 8):
    total_sampl = s_period * num_periods;
    X = []

    for i in range(total_sampl):
        val = math.sin(2*math.pi*i/s_period)
        X += [val]

    return X




