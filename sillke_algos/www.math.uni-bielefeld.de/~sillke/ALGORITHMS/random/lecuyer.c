/***********************************************************************

   uniform [0,1] random number generator
   developed by Pierre Lecuyer based on a clever
   and tested combination of two linear congruential
   sequences

   s1 and s2 are the seeds (positive integers)

   Pierre Lecuyer,
     Random Number Generation,
     In: Handbook on Simulation,
     Jerry Banks, ed. Wiley, New York, 1997

***********************************************************************/

static long s1 = 55555;
static long s2 = 99999;


int lecuyer()
{
        int k;

	/**  s1 = 40014 * s1 % 2147483563  **/
        k  = s1 / 53668;
        s1 = 40014*(s1%53668)-k*12211;
        if (s1 < 0) s1 += 2147483563;

	/**  s2 = 40692 * s2 % 2147483399  **/
        k  = s2 / 52774;
        s2 =40692*(s2%52774)-k*3791;
        if (s2 < 0) s2 += 2147483399;

        /**  combine s1 and s2  **/
        k = (s1 - 2147483563) + s2;
        if (k < 1) k += 2147483562;

        return k;
}

double uni()
{
        const double factor = 1.0/2147483399.0;
        int k;

	/**  s1 = 40014 * s1 % 2147483563  **/
        k  = s1 / 53668;
        s1 = 40014*(s1%53668)-k*12211;
        if (s1 < 0) s1 += 2147483563;

	/**  s2 = 40692 * s2 % 2147483399  **/
        k  = s2 / 52774;
        s2 =40692*(s2%52774)-k*3791;
        if (s2 < 0) s2 += 2147483399;

        /**  combine s1 and s2  **/
        k = (s1 - 2147483563) + s2;
        if (k < 1) k += 2147483562;

        return(((double)(k))*factor);
}

#if 1
#include <stdio.h>

int main()
{
   int i, d=0;
   for (i=0; i<20; i++)
     printf ("%.8x\n", lecuyer());

   for (i=0;i<0x1000000;i++)
   {
      d += lecuyer();
   }
   return d;
}
#endif
