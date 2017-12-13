/***********************************************************************

   x[i] = (2^30 - 2^19) x[i-1] mod (2^61 - 1)

  Reference:

   Pei-Chi Wu,
     Multiplicative, Congruential Random-Number Generators 
     with Multipliers +-2^k1 +- 2^k2 and Modulus 2^p - 1,
     ACM Trans. Math. Software 23 (1997) 255-265

***********************************************************************/

typedef unsigned long long int uint64;
typedef long long int int64;

static uint64 x = 1;

int std61ran (void)
{
   const uint64 M = 0x1fffffffffffffffll;
   x =   (x>>31) + ((x<<30) & M)
       - (x>>42) - ((x<<19) & M);
   if ((int64)x < 0) x += M;
   return (unsigned int)x & 0x7fffffff;
}



#include <stdio.h>

int main ()
{
   int i, d=0;
   for (i=0; i<20; i++) {
      printf("%20d\n", std61ran() );
   }

   for (i=0;i<0x1000000;i++)
   {
      d += std61ran();
   }
   return d;
}
