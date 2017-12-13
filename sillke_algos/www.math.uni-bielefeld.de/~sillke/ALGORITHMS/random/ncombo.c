#define mod_  0xfffffffb
static unsigned int x_1=1, x_2=2;
static unsigned int y_1=1, y_2=2, y_3=3;

/***********************************************************************

  uniform unsigned int random generator ncombo.

  Implementation: Torsten Sillke, 1991
  email: Torsten.Sillke@uni-bielefeld.de

***********************************************************************/

unsigned int ncombo ()
{
   /* Init x1, x2     not all 0; 2*x3 + 1 = (2*x2+1)(2*x1+1) mod 2^33 */
   /* Init y1, y2, y3 not all 0;       y4 = y1 - y3 mod (2^32 - 5)    */
   /* period(x) = 3 * 2^30;    period(y) = (2^32 - 5)^3 - 1           */
   /* period(ncombo) = lcm(period(x),period(y)) ~ 3*2^125 ~ 1.276e38  */
   /* George Marsaglia [1984]                                         */
   /* A Current View of Random Number Generators                      */
   /* Computer Science and Statistics                                 */
   /* Proceedings of the 16th Symposium on the Interface  pp3-10      */
   unsigned int x_new, y_new;

   /* x series:  x_new = 2 x1 x2 + x1 + x2 */
   x_new = 2*(x_1*x_2) + x_1 + x_2; x_1=x_2; x_2=x_new;

   /* y series:  y_new = y1 - y3 mod (2^32 - 5) */
   if (y_3>y_1) y_1 += mod_; y_new=y_1-y_3; y_1=y_2; y_2=y_3; y_3=y_new;

   return x_new-y_new;
}


#if 1
#include <stdio.h>

int main ()
{
   int i, d=0;
   for (i=0; i<20; i++) {
      printf("%20u\n", ncombo() );
   }

   for (i=0;i<0x1000000;i++)
   {
      d += ncombo();
   }
   return d;
}
#endif
