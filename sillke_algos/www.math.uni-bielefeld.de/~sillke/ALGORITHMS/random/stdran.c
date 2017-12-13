/***********************************************************************

   The Minimal Portable Random Number Generator
  
   a = 7^5 = 16807   m = 2^31 - 1 = 2147483647 = 0x7fffffff
  
   x[n+1] = a * x[n] (mod m)
  
   Ref: - G. S. Fishman, L. R. Moore;
	  An statistical exhaustive analysis of multiplicative
	  congruential random number generators with modulus 2^31-1,
	  SIAM J. Sci. Statist. Comput., 7 (1986) 24-45. 
	  Erratum, ibid, 7 (1986) 1058
        - Numerical Recipes in C (2nd Ed.) 
          Chap. 7.1, p 278-279 
        - THE OX BOOK, DOORNIK, 1996, p 150 
	  generator: ranuox()
        (The algorithm proposed by Park and Miller (1988) 
	 given in this references is slower than this one.)
  
   It follows a fast and portable implementation with bit manipulation.
   (System Condition:  32Bit integer)
  
   All Multipliers have been tested for the modulo 2^31 - 1.
   The best (small) one is a=48271 (Fishman, Moore, 1986), 
   good distributed and fast to implement.
  
   Torsten Sillke, 1994
   email: Torsten.Sillke@uni-bielefeld.de
   
***********************************************************************/

void std31ranInit (int u);
int  std31ran     (void);

/*--------------------------------------------------------------------*/

#define FACTOR_IBM   16807
#define FACTOR_BEST  48271

static unsigned int x = 1;
static const unsigned int a = FACTOR_BEST;

void std31ranInit (int u)
{
  int v = (u+1) & 0x7fffffff;
  if (v==0) v++;
  if (v+1<0) v--;
  x = v;
}

int std31ran (void)
{
  unsigned zh, zl, z;
  z = x<<1;
  /* the bits are now shifted to the front */
  zl = z & 0xffff;
  zh = z >> 16;
  zl *= a;
  zh *= a;
  zh += zl >> 16;
  zl = (zl & 0xffff) + (zh << 16);
  zh = (zh >> 16) << 1;
  zl += zh;
  if (zh > zl) zl += 2;
  z = zl >> 1;
  x = z;
  return z;
}


#include <stdio.h>

int main ()
{
   int i, d=0;
   for (i=0; i<20; i++) {
      printf("%20d\n", std31ran() );
   }

   for (i=0;i<0x1000000;i++)
   {
      d += std31ran();
   }
   return d;
}

