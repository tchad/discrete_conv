'''
    Homework 2 CMPE242, derivative and low pass filter by convolution

    Author: Tomasz Chadzynski
    Version: v0.2
    Date: 4/17/19

    This task implements kernels used in discrete convolution.
    Kernel 1 computes a first derivative of the signal using the central difference approach.
    Kernel 2 Applies low pass filter to the signal. The filtering is implemented by applying gaussian smoothing technique.

     MODULE: Main module performing the tests and displaying results

'''

import sys
import data_io as dio
import fft
from conv import convolve_odd_kern
import gauss
import filter_kern as k


if __name__ == "__main__":
    if(len(sys.argv) > 1):
        data_filename = sys.argv[1]
        print('__main__: custom input filename=%s' % data_filename)
    else:
        data_filename = 'data/adc_sampler_pot_133us_100nf.out'
        print('__main__: default input filename=%s' % data_filename)

    if(len(sys.argv) > 2):
        sigma = float(sys.argv[2])
        print('__main__: custom sigma=%f' % sigma)
    else:
        sigma = 10
        print('__main__: default sigma=%s' % sigma)


    #Derivative calculation
    data_gen_sin = dio.gen_sin(128,8)
    kern_derivtive = k.gen_kern_centr_diff();
    data_gen_sin_der = convolve_odd_kern(data_gen_sin, kern_derivtive)

    dio.plot_raw(data_gen_sin, title='sin(x) signal')
    dio.plot_raw(data_gen_sin_der, title='sin(x) derivative cos(x)')

    #Low pass filter
    data_raw = dio.read_raw_data(data_filename)

    gauss_t = gauss.test_gauss(sigma)
    dio.plot_raw(gauss_t[0], title='Gauss function', custom_range=gauss_t[1])
    kernel_lpf = k.gen_kern_gaussian_smoothing_lpf_1D(s=sigma)
    data_lpf = convolve_odd_kern(data_raw, kernel_lpf)

    dio.plot_raw(data_raw, title='Raw potentiometer data')
    dio.plot_raw(data_lpf, title='Low pass filter applied')
    
    data_raw_prep = fft.prep_input(data_raw)
    data_raw_fft = fft.fft(data_raw_prep)
    data_raw_pwr = fft.pwr_spectrum(data_raw_fft)

    data_lpf_prep = fft.prep_input(data_lpf)
    data_lpf_fft = fft.fft(data_lpf_prep)
    data_lpf_pwr = fft.pwr_spectrum(data_lpf_fft)

    dio.print_signal_properties(data_raw_pwr, .5, 'Raw power spectrum')
    dio.plot_pwr_spectrum(data_raw_pwr, title= 'Raw data power spectrum', no_dc=False)

    dio.print_signal_properties(data_lpf_pwr, .5, 'LPF power spectrum')
    dio.plot_pwr_spectrum(data_lpf_pwr, title= 'Filtered data power spectrum', no_dc=False)


    dio.plot_pwr_spectrum(data_raw_pwr, title= 'Raw data power spectrum', no_dc=True)
    dio.plot_pwr_spectrum(data_lpf_pwr, title= 'Filtered data power spectrum', no_dc=True)

    dio.plot_pwr_spectrum_log(data_raw_pwr, title= 'Raw data power spectrum')
    dio.plot_pwr_spectrum_log(data_lpf_pwr, title= 'Filtered data power spectrum')





