#include <stdio.h> 
#include <math.h> 

/*--------------------------------------------------------------------------*/


/***********************************************************************
  Erfc Approximation:

  erfc(z) = t * exp(-z*z) * exp(A0 + A1*t + A2*t^2 + A3*t^3 ...)
   with t = 1/(1 + z/2);

  Error: 1.2e-7 maximal relative error for z>=0

  Numerical Recepies, Chap. 6 Special Functions

***********************************************************************/


double Erfc (double z)
{
   const double a0 = -1.26551223;
   const double a1 =  1.00002368;
   const double a2 =  0.37409196;
   const double a3 =  0.09678418;
   const double a4 = -0.18628806;
   const double a5 =  0.27886807;
   const double a6 = -1.13520398;
   const double a7 =  1.48851587;
   const double a8 = -0.82215223;
   const double a9 =  0.17087277;
   const double  t = 2./(2. + z);
   return t*exp(-z*z+a0+t*(a1+t*(a2+t*(a3+t*(a4+t*(a5+t*(a6+t*(a7+t*(a8+t*a9))))))))); 
}

double Phi (double z)
{
   return 0.5 * erfc( -0.70710678118654752440*z );
}

/*--------------------------------------------------------------------------*/

double Phi_cf15(const double x) 
{ 
        /* Cumulative density function of a N(0,1)   */
        /* return PHI(x) := P(X<=x), for X ~ N(0,1); */

        double x2, t; 

        if (fabs(x)<=4.5)   // -4.5 < x < 4.5 
        { 
                x2 = x*x; 
                t  = 0.5 + x /( 0.2506628275E1 
			 + x2/( 0.2393653683E1
			 + x2/(-0.250662828E2
			 + x2/(-0.1432100488
			 + x2/( 0.3095465448E2
			 + x2/( 0.2336751681E1
			 + x2/(-0.6390521829E2
			 + x2/(-0.9856539925E-1
			 + x2/( 0.6976745875E2
			 + x2/( 0.2339886995E1
			 + x2/(-0.1035124219E3
			 + x2/(-0.8721329536E-1
			 + x2/( 0.1093844274E3
			 + x2/( 0.2336524657E1
			 - 0.7036241192E-2*x2)))))))))))))); 
        } 
        else 
        { 
                /* Note that the procedure gives 0 (resp. 1)  */
                /* for x<- 4.5 (resp. x> 4.5)                 */
                if (x>0.0) t=1.0; else t=0.0; 
        } 
        return(t); 
} 

/*--------------------------------------------------------------------------*/

static double PHI_inverseApprox(const double p)
{
   /* valid for 0 < p <= 0.5  */
   /* abs error <= 5.0e-4     */
   const double C0=2.515517; 
   const double C1=0.802853; 
   const double C2=0.010328; 
   const double D1=1.432788; 
   const double D2=0.189269; 
   const double D3=0.001308; 
   const double t = sqrt(-2*log(p));
   return (C0 + t*(C1 + t*C2))/(1. + t*(D1 + t*(D2 + t*D3))) - t; 
}

double PHI_inverse(const double p) 
{ 
   /* Inverse cdf of a N(0,1)            */
   /* PHI(x) := P(X<=x), for X ~ N(0,1); */
   /* then return PHI^(-1)(x);           */
   /* abs error <= 5.0e-4                */

   double zz = 0;
   if (p < 0.5)
      zz = PHI_inverseApprox(p);
   if (p > 0.5)
      zz = - PHI_inverseApprox(1 - p);
   return zz;
} 


/*--------------------------------------------------------------------------*/

/*---------------------------------------------------------------------------*/
/* NORMSDIST                                                                 */
/* Approximation of normal density function, solves for area under the       */
/* standard normal curve from -infinity to x.                                */
/* Duplicates MS Excel NORMSDIST() function, and agrees to within 1.0e-10    */
/* The maximal relative error is 1.35e-7.                                    */
/*---------------------------------------------------------------------------*/

double normsdist(const double x)
{
   const double invsqrt2pi = 0.3989422804014327;
   const double b1 =  0.31938153;
   const double b2 = -0.356563782;
   const double b3 =  1.781477937;
   const double b4 = -1.821255978;
   const double b5 =  1.330274429;
   const double p  =  0.2316419;
   const double ax = fabs(x);
   const double t  = 1.0 / (1.0 + p * ax);
   double area;
   area = invsqrt2pi * exp(-0.5 * x*x)
                  * t*(b1 + t*(b2 + t*(b3 + t*(b4 + t*b5))));
   if (x > 0.0) area = 1.0 - area;
   return area;
}

#if 0
//---------------------------------------------------------------------------
// INVNORMSDIST
// Inverse normal density function, solves for number of standard deviations
// x corresponding to area (probability) y.  Duplicates MS Excel NORMSINV().
//---------------------------------------------------------------------------
double invnormsdist(const double y)  // 0 < y < 1;
{
register double x, tst, incr;
if (y < 1.0e-20) return -5.0;
if (y >= 1.0) return 5.0;
x = 0.0;
incr = y - 0.5;
while (fabs(incr) > 0.0000001) {
  if (fabs(incr) < 0.0001 && (x <= -5.0 || x >= 5.0)) break;
  x += incr;
  tst = normsdist(x);
  if ((tst > y && incr > 0.) || (tst < y && incr < 0.)) incr *= -0.5;
  }
return x;
}
#endif

/*--------------------------------------------------------------------------*/

int main() 
{ 
     double p, z;

     for (p=0; p<=6.0; p+=1./128)
     {
        double x = normsdist(p);
        double y = Phi(p);
        printf("%20.15lf %20.15lf %20.15lf %20.15lf %10.6lf\n", p, x, y, x-y, 1.e9*(x/y-1));

     }

#if 0
     for (p=0; p<=5.0; p+=0.0625)
     {
        double x = erfc(p);
        double y = Erfc(p);
        printf("%20.15lf %20.15lf %20.15lf %20.15lf\n", p, x, y, x-y);

     }
#endif
        p=0.3; printf("%5.4lf  %20.15lf \n", p, PHI_inverse(p));
        p=0.4; printf("%5.4lf  %20.15lf \n", p, PHI_inverse(p));
        p=0.5; printf("%5.4lf  %20.15lf \n", p, PHI_inverse(p));
        p=0.6; printf("%5.4lf  %20.15lf \n", p, PHI_inverse(p));
        p=0.7; printf("%5.4lf  %20.15lf \n", p, PHI_inverse(p));
        p=0.8; printf("%5.4lf  %20.15lf \n", p, PHI_inverse(p));
        p=0.9; printf("%5.4lf  %20.15lf \n", p, PHI_inverse(p));
        p=0.99; printf("%5.4lf  %20.15lf \n", p, PHI_inverse(p));
        p=0.999; printf("%5.4lf  %20.15lf \n", p, PHI_inverse(p));
        p=0.9999; printf("%5.4lf  %20.15lf \n", p, PHI_inverse(p));

#if 0
     for (z= -1; z<=6.0; z+=0.0625)
     {
        p=Phi(z); printf("%12.9lf  %20.8lf %12.8lf\n", p, PHI_inverse(p), PHI_inverse(p)-z);
     }
#endif
        return 0;
} 
