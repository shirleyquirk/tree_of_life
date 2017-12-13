/**********************************************************************
* Incomplete Gamma Function                                           *
*---------------------------------------------------------------------*
*
*                           x
*                    2      |\
*     erf(x)  =  ---------  | exp(-t*t) dt
*                 sqrt(pi) \|
*                           0
*
*                           oo
*                           |\         a-1
*   Gamma(a)  =             | exp(-t) t    dt
*                          \|
*                           0
*
*                           x
*                           |\         a-1
* gamma(a,x)  =             | exp(-t) t    dt
*                          \|
*                           0
*
*                           oo
*                           |\         a-1
* Gamma(a,x)  =             | exp(-t) t    dt
*                          \|
*                           x
*
* GammaP(a,x) = gamma(a,x) / Gamma(a)
* GammaQ(a,x) = Gamma(a,x) / Gamma(a)
*
* erf(x) = gammap(1/2, x*x)   for x>=0.
* Phi(x) = 1/2 + 1/2*erf(x/sqrt(2)) = 1/2 + 1/2*gammap(1/2, x*x/2)
*
* Let lgamma(x) = log(Gamma(x)).
*
* Reference:
*
* - W. Press, S. Teukolsky, W. Vetterling, B. Flannery:
*   Numerical Recipes in C
*   The Art of Scientific Computing (Second Edition, 1992)
*   Chap. 6.2: Incomplete Gamma Function, Error Function, [...]
*
*   http://nr.harvard.edu/nr/bookc.html (Online Version)
*
***********************************************************************/

#include <math.h>
#define EPS 1.0e-9

double gammap_sr(double a, double x, double ldenum)
{
  const int itmax = 200;
  int n;
  double sum, del, ap;

  if (x <= 0)
     return 0; /* invalid arguments */

  ap = a;
  sum = del = 1/a;
  for (n=1; fabs(del)>fabs(sum)*EPS || n<=itmax; n++) {
     ++ap;
     sum += del *= x/ap;
  }
  return sum * exp(-x+a*log(x)-ldenum);
}

double gammaq_cf(double a, double x, double ldenum)
{
  /* modified Lentz's method */
  const int itmax = 200;
  const double fpmin = 1.0e-80;
  int n;
  double an, b, c, d, del, cf;
  b = x+1-a;
  c = 1/fpmin;
  d = 1/b;
  cf = del = d;
  for (n=1; fabs(del-1) > EPS || n<=itmax; n++) {
     an = -n*(n-a);
     b += 2;
     d = an*d + b;
     if (fabs(d) < fpmin) d = fpmin;
     c = b + an/c;
     if (fabs(c) < fpmin) c = fpmin;
     d = 1/d;
     del = d*c;
     cf *= del;
  }
  return cf * exp(-x+a*log(x)-ldenum);
}

double gammap (double a, double x)
{
  /** Incomplete Gammafunction **/
  if (x < 0 || a <= 0) return 0; /* invalid arguments */

  if (x < a+1)
     return gammap_sr(a,x,lgamma(a));
  else
     return 1-gammaq_cf(a,x,lgamma(a));
}

double gammaq (double a, double x)
{
  /** Incomplete Gammafunction **/
  if (x < 0 || a <= 0) return 0; /* invalid arguments */

  if (x < a+1)
     return 1-gammap_sr(a,x,lgamma(a));
  else
     return gammaq_cf(a,x,lgamma(a));
}


main()
{
   /*** T e s t: erf(x) = gammap(0.5,x*x) ***/
   double x;
   for (x=0.0; x<=4.0; x+=0.001) {
     printf("%5.3lf %12.9lf %12.9lf\n", x, erf(x), gammap(0.5,x*x));
   }
}
