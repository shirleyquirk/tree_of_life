
/***********************************************************************
*
* Normal Distribution Function
*   phi(z)  = exp(-z*z/2) / sqrt(2*Pi);
*
* Commulative Normal Distribution Function
*   Phi(z)  = 1/2 + 1/2 * erf( z/sqrt(2) )
*           = 1/2 * erfc( -z/sqrt(2) )
*           = 1/2 + 1/2 * P(1/2, x*x/2)
*
*   with erf() the error function
*   and P() the gamma function percentages
*
* The following functions are defined in this modul:
*
*   Phi()         :: Commulative Normal Distribution Function
*   InvPhi()      :: the inverse of Phi()
*   InvErf()      :: the inverse of erf()
*   InvErfc()     :: the inverse of erfc()
*
* Functions used:
*   The non-ANSII function erf() and erfc() are used.
*
***********************************************************************/

#include<math.h>
#include<limits.h>
#include<errno.h>

static const double Cpi      = 3.1415926535897932384626434;
static const double C2sqrtPi = 1.1283791670955125738961589;
static const double CsqrtPi  = 1.7724538509055160272981675;
static const double Csqrt2   = 1.4142135623730950488016887;
static const double C1sqrt2  = 0.7071067811865475244008444;


double Phi (double z)
{
   return 0.5 * erfc( - C1sqrt2*z );
}

/***********************************************************************

   Inverse of the error function Erf.

   Implementation: Inversion by Newton iteration of erf(x).
      The initial value x0 = 0.
      For |z| <= 0.84 (=erf(1)) at most 4 iterations are necessary.

***********************************************************************/

static double InvErfSmall (const double z)
{
   /* f(x)   = erf(x) - z   */
   /* f'(x)  = c*exp(-x*x)  */
   /* f''(x) = -2 f'(x)     */
   double c = C2sqrtPi;
   double f = -z, f1=c;
   double q = f/f1, x = -q, x0 = 0;

   while (fabs(x-x0) > 1e-12 && fabs(f) > 1e-14 ) {
      /* Newton 2nd order: x <- x - f/f'(1 + f*f''/(2 f'^2)) */
      x0  = x;
      f   = erf(x) - z;
      f1  = c*exp(-x*x);
      q   = f/f1;
      x  -= q*(1-x*q);  /* Newton Step 2nd order */
   }

   return x;
}

/***********************************************************************

 lambert_w2 is that "Dilbert lambda" (inverse x e^x^2) 
 If you don't have W functions, you can probably get away with 

                                     log(log(x)) 
     lambert_w2(x) ~ sqrt(log(x)) - -------------- . 
                                    4 sqrt(log(x)) 

***********************************************************************/

static double lambertW2 (const double z)
{
   /* "Dilbert lambda" (inverse x e^x^2) approximation */
   double logz = log(z);
   double slz  = sqrt(logz);
   return slz - 0.25*log(logz)/slz;
}


/***********************************************************************

   Inverse of the error function Erfc.

   Implementation: Inversion by Newton iteration of erfc(sqrt(log(x))).
      The initial value is computed via lambertW2.
      For z < 0.25 at most 4 iterations are necessary.

***********************************************************************/

static double InvErfcSmall (const double z)
{
   /* f(x)   = erfc(sqrt(log(x))) - z   */
   /* f'(x)  = 1/(c x^2 sqrt(log(x)))   */
   /* f''(x) = -c*x*f'(x)^2*(2*sqrt(log(x))+1/(2*sqrt(log(x))))   */
   double c = CsqrtPi;
   double f = 1, f1i=0;
   double a = lambertW2(1/(c*z));
   double x = erfc(a)/(c * a * z*z), x0 = 0;

   while (fabs(x-x0) > 1e-12*x && fabs(f) > 1e-15*z ) {
      /* Newton 2nd order: x <- x - f/f'(1 + f*f''/(2 f'^2)) */
      double slx;
      x0  = x;
      slx = sqrt(log(x));
      f   = z - erfc(slx);
      f1i = c * x * x * slx;
      x  -= f*f1i*(1 - c*f*x*(slx + 0.25/slx));       /* Newton Step */
   }

   return  sqrt(log(x));
}

/***********************************************************************

   Inverse of the error function Erf.

   Implementation: 
      For small and big values two differnt approximations are used.
      
   Return values:
      If x is +1, InvErf() returns +INFINITY.
      If x is -1, InvErf() returns -INFINITY.
      If x is not in the range [-1, 1],
      InvErf() returns NaN and sets errno to EDOM.

***********************************************************************/

double InvErf (const double z)
{
   double az = fabs(z);
   double x = 0;
   if (az>=1)
   {
      double huge = DBL_MAX;
      double inf  = 2*huge;
      /* Infinity of NaN */
      if (z == 1)
	 return  inf; /* +infinity */
      if (z == -1)
	 return -inf; /* -infinity */
      /* out of range, set errno=EDOM, return NaN */
      errno=EDOM;
      return inf-inf;
   }

   if (az < 0.8125)          /* -13/16 < z < 13/16 */
      x =  InvErfSmall(z);
   else if (z > 0)           /* z >=  13/16 */
      x =  InvErfcSmall(1-z);
   else                      /* z <= -13/16 */
      x = -InvErfcSmall(z+1);
   return x;
}

double InvErfc (const double z)
{
   double x = 0;
   if ( z<=0 || z>=2 )
   {
      double huge = DBL_MAX;
      double inf  = 2*huge;
      /* Infinity of NaN */
      if (z == 0)
	 return  inf; /* +infinity */
      if (z == 2)
	 return -inf; /* -infinity */
      /* out of range, set errno=EDOM, return NaN */
      errno=EDOM;
      return inf-inf;
   }

   if (z <= 0.1875)          /* z <=   3/16 */
      x =  InvErfcSmall(z);
   else if (z < 1.8125)      /* 3/16 < z < 29/16 */
      x =  InvErfSmall(1-z);
   else                      /* z >=  29/16 */
      x = -InvErfcSmall(2-z);
   return x;
}

/***********************************************************************

   Inverse of the cumulative normal distribution

   Implementation: 

***********************************************************************/

double InvPhi (double z)
{
   return -Csqrt2 * InvErfc( 2*z );
}


#if 1
/************* T E S T *******************************************/

#include<stdio.h>

int main()
{
   double p;
   p = 0.5      ; printf("%10.7lf erf  %30.28lf \n", p, erf(p));
   p = 1.0      ; printf("%10.7lf erf  %30.28lf \n", p, erf(p));
   p = 1.5      ; printf("%10.7lf erf  %30.28lf \n", p, erf(p));
   p = 2.0      ; printf("%10.7lf erf  %30.28lf \n", p, erf(p));
   p = 3.0      ; printf("%10.7lf erf  %30.28lf \n", p, erf(p));
   p = 6.0      ; printf("%10.7lf erfc %30.28lg \n", p, erfc(p));
   p = 8.0      ; printf("%10.7lf erfc %30.28lg \n", p, erfc(p));

   p = -0.99    ; printf("%10.7lf %21.18lf \n", p, InvErf(p));
   p = -0.5     ; printf("%10.7lf %21.18lf \n", p, InvErf(p));
   p = 0.0      ; printf("%10.7lf %21.18lf \n", p, InvErf(p));
   p = 0.5      ; printf("%10.7lf %21.18lf \n", p, InvErf(p));
   p = 0.6      ; printf("%10.7lf %21.18lf \n", p, InvErf(p));
   p = 0.7      ; printf("%10.7lf %21.18lf \n", p, InvErf(p));
   p = 0.9      ; printf("%10.7lf %21.18lf \n", p, InvErf(p));
   p = 0.99     ; printf("%10.7lf %21.18lf \n", p, InvErf(p));

   p = erfc(9.9); printf("%10.7lg ierfc %21.18lf \n", p, InvErfc(p));

   p = 1.0      ; printf("%10.7lf %21.18lf \n", p, InvErf(p));
   p = -1.0     ; printf("%10.7lf %21.18lf \n", p, InvErf(p));
   p = 2.0      ; printf("%10.7lf %21.18lf \n", p, InvErf(p));

   p = 0.0      ; printf("%10.7lf %21.18lf \n", p, InvPhi(p));
   p = 1.0      ; printf("%10.7lf %21.18lf \n", p, InvPhi(p));
   p = 0.5      ; printf("%10.7lf %21.18lf \n", p, InvPhi(p));
   p = Phi(1.)  ; printf("%10.7lf %21.18lf \n", p, InvPhi(p));
   p = Phi(2.)  ; printf("%10.7lf %21.18lf \n", p, InvPhi(p));
   p = Phi(3.)  ; printf("%10.7lf %21.18lf \n", p, InvPhi(p));
   p = Phi(-4.) ; printf("%10.7lf %21.18lf \n", p, InvPhi(p));
   p = Phi(-5.) ; printf("%10.7lf %21.18lf \n", p, InvPhi(p));

   return 0;
}
#endif
