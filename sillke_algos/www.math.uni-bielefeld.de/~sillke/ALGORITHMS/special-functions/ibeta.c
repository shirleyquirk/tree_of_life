#include <math.h>

/***********************************************************************

  Algoritm: incomplete beta ratio

  Reference:
    Posten, Storrs;
    Algorithms for the Beta Distribution Function,
    Compstat 1986, 309-319

***********************************************************************/

double betar(double a, double b, double x)
{
  /** Incomplete Betafunction          **/
  /** beta(a,b,0) = 0; beta(a,b,1) = 1 **/
  double s, h, p1, p2, q1, q2, so, cz, cz1, cn, cn1, dz, dz1, dn, dn1;
  int k;
  if (a/(a+b) < x) return 1.0-beta(b,a,1.0-x);
  if (1.0e-30 > x) return 0.0;

  cz = a*(a+b); cz1 = a+a+b-1;  dz = b-1;         dz1 = b-1;
  cn = a*(a+1); cn1 = 4*a-2;    dn = (a+1)*(a+2); dn1 = 4*a+2;

  /** Continued fraction expansion **/
  p1 = q2 = 0.0; p2 = q1 = 1.0; s = 0.0;
  for (k=1;k<=999;k++)
  {
    so = s;
    h = cz / cn * x;  /** C(k) **/
    p2 = p1 - h*p2; q2 = q1 - h*q2;
    h = dz / dn * x;  /** D(k) **/
    p1 = h*p1 + p2; q1 = h*q1 + q2;
    s =  p1 / q1;
    if (fabs(s-so) <  1.0e-15*fabs(s)) break;
    /** NEXT C(k), D(k) **/
    cz += cz1 += 2; dz += dz1 -= 2;
    cn += cn1 += 8; dn += dn1 += 8;
  }
  so = lgamma(a+b) - lgamma(a+1.0) - lgamma(b);
  so = exp( so + a * log(x) + b*log(1.0-x) - log(1.0+s) );
  if (so > 1.0) so = 1.0;
  return so;
}
