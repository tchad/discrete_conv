/*****************************************************************
* Program is for CMPE class use, see Dr. Harry Li's lecture notes for details *
* Reference: Digital Signal Processing, by A.V. Oppenhaim;                                * 
* fft.c for calculting 4 points input, but you can easily expand this to 2^x inputs; *
* : x0.1;             Date: Sept. 2009;                                                               * 
* Note: cross compiled for arm-linux-gcc, be sure to modify make file
to link math lib when compiling, by adding -lm 
This code then was tested on ARM11 board. Feb 2015.  
******************************************************************/
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <stdint.h>

#define ARR_SZ 131072
#define SET_POW 17

typedef struct sComplex
{	double a;        //Real Part
	double b;        //Imaginary Part
} Complex;

uint32_t bitrev(uint32_t i, uint32_t bitnum)
{
    uint32_t ret = 0;

    for( uint32_t b = 0; b < bitnum; b++) {
        if(i & (0x1u << b)) {
            ret |= (0x1u << (bitnum - 1 - b));
        }
    }

    return ret;
}

void FFT(Complex *X, uint32_t M)
{
	uint32_t N = pow(2, M);

	for (uint32_t k = 0; k < M; k++)
	{
		uint32_t LE = pow(2, M - k);
		uint32_t LE1 = LE / 2;

        Complex U = {
            .a = 1.0, 
            .b = 0.0
        };

        Complex W = {
		    .a = cos(M_PI / (double)LE1),
		    .b = -sin(M_PI/ (double)LE1)
        };

		for (uint32_t j = 0; j < LE1; j++)
		{
			for (uint32_t i = j; i < N; i = i + LE)
			{
                Complex tmp1, tmp2;
				uint32_t IP = i + LE1;

				tmp1.a = X[i].a + X[IP].a;
				tmp1.b = X[i].b + X[IP].b;

				tmp2.a = X[i].a - X[IP].a;
				tmp2.b = X[i].b - X[IP].b;

				X[IP].a = (tmp2.a * U.a) - (tmp2.b * U.b);
				X[IP].b = (tmp2.a * U.b) + (tmp2.b * U.a);

				X[i] = tmp1;
			}

            Complex tmp = {
			    .a = (U.a * W.a) - (U.b * W.b),
                .b = (U.a * W.b) + (U.b * W.a)
            };
			U = tmp;
		}
	}

    //Apply scaling
	for(uint32_t i=0; i<N; i++) {
        X[i].a /= N;
        X[i].b /= N;
	}

    //Sort using bit reversal
    //TODO: Add in place sorting with proper indexing pattern
    Complex *tmp_arr = malloc(sizeof(Complex) * N);
    for( uint32_t i=0; i< N; i++) {
        tmp_arr[i] = X[i];
    }

    for( uint32_t i=0; i< N; i++) {
        uint32_t i_rev = bitrev(i, M);
        X[i] = tmp_arr[i_rev];
    }
    
    free(tmp_arr);
}

int main(int argc, char **argv)
{
    /*
     * ARGS:
     * string - path to source file
     * string - path to destination file
     * int = log2(array size) - must be integer (array size = 2^N)
     */

	uint32_t i;
    uint32_t arr_pow;
    uint32_t arr_sz;
    Complex *X;

	FILE *f = fopen(argv[1], "r");
    arr_pow = atoi(argv[3]);
    arr_sz = pow(2,arr_pow);
    X = malloc(sizeof(Complex)*arr_sz);
    

    //Read data from input file
	for(i=0; i<arr_sz; i++) {
		int tmp;
		fscanf(f, "%d\n", &(tmp));
		X[i].a = tmp;
        X[i].b = 0;
	}

	fclose(f);

	/*
	printf ("*********Before*********\n");
	for (i = 1; i < ARR_SZ; i++)
		printf ("X[%d]:real == %f  imaginary == %f\n", i, X[i].a, X[i].b);
	*/

    //Perform FFT
	FFT(X, arr_pow);

	/*
	printf ("\n\n**********After*********\n");
	for (i = 1; i < ARR_SZ; i++)
		printf ("X[%d]:real == %f  imaginary == %f\n", i, X[i].a, X[i].b);
		*/

    //Save complex freq representation back to file
	f = fopen(argv[2], "w");
	for (i = 0; i < arr_sz; i++)
		fprintf (f,"%d:%f:%f\n", i, X[i].a, X[i].b);

	fclose(f);
    free(X);

	return 0;
}

