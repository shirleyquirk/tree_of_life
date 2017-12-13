#define R 127
#define S 30
#define MASK 127
#define IMPLICID_BITS 2
static unsigned int rands[128];
static unsigned int p = 0;

/***********************************************************************
 
  uniform unsigned int random generator rand_dia.

  Persi Diaconis's (Harvard Univ.) personal favorite is a multiplicative
  "lagged Fibonacci" generator that starts with 55 odd numbers and than 
  uses the formular
  
    x(n) = x(n-24) * x(n-55)  mod (2**32)

  to generate a sequence of random numbers. 
  (Diaconis, "The Unreasonable Effectiveness of Number Theory", AAAS'94 talk)
  This "lagged Fibonacci" generators was considered by Marsaglia.
  He defines F(R,S,OP) as the recurence: x(n) = x(n-R) OP x(n-S).
  Parameters he considers: F(17,5,*), F(31,13,*), F(55,24,*), F(127,30,*).

  To analyze F(R,S,*) with R>S use the transformation (Knuth TAOCP2 3.2.2 Ex31): 
    x(n) = (-1)**s(n) * 3**z(n).
  Then we have the recurences for z and s
    z(n) = z(n-R) + z(n-S)  mod (2**32)
    s(n) = s(n-R) + s(n-S)  mod 2
  We see that we should avoid setting all x(n) be +1 or -1 modulo 8.
  The maximal period for n bit words is (2**R - 1) * 2**(n-3) for n>=3.
  For a test you can use F(3,1,*) and n=4 (the last hex-digit).
  The lowest hex-digit of b0 has period 56 if calculated with 2 implicid bits.

  -= one implicid bit version =-
  As we know that all values are odd, lets calculate with an implicid last bit
    x(n) = x(n-R) * x(n-S)  mod (2**33)
  on 32-bit machines instead. Let x(n) = 2 y(n) + 1 than we have
    
    y(n) = 2 * y(n-R) * y(n-S) + y(n-R) + y(n-S) mod (2**32)

  -= two implicid bits version =-
  If we calculate with 3**z values only, the bit pattern ending with
  the three bits 0X1. Therefore we can drop two bits and calculate
  with two implicid bits.
  
  Ref: - Barry A. Cipra,
	 AAAS'94: Random Numbers, Art and Math,
	 SIAM News, Aug./Sept. 1994, p 24 and 18.

       - G. Marsaglia,
	 A Current View of Random Number Generators,
	 Computer Science and Statistics, 1985, 3-10

       - D. E. Knuth,
	 The Art of Computer Programming, Vol2: Semi-numerical Algorithms,
	 3rd. Edition, Addison-Wesley, Reading, 1997 (not 2nd Edition)
	 Sec. 3.2:   Generating uniform random variables
	 Sec. 3.2.2: Other methods
	   equation (7') and exercise 3.2.2 Ex 31

  Implementation: Torsten Sillke, 1995 (one implicid bit version)
  Implementation: Torsten Sillke, 1998 (two implicid bits version)
  email: Torsten.Sillke@uni-bielefeld.de
 
***********************************************************************/

void rand_dia_init (unsigned int seed)
{
   int i;
   /* set the position back */
   p = 0;  
   /* init the random buffer */
   rands[0] = seed | 1;
   for (i=1;i<R;i++)
     rands[i] = 69069 * rands[i-1];
   for (i=0;i<R;i++) {
     rands[i] += rands[i]>>16;
#if IMPLICID_BITS==0
     rands[i] |= 1;
#endif
   }
}

unsigned int rand_dia (void)
{
   /* fib(n) = fib(n-R) * fib(n-S); with all fib() odd. */
   unsigned int pos = --p;
   unsigned int br = rands[(pos+R) & MASK];
   unsigned int bs = rands[(pos+S) & MASK];
#if IMPLICID_BITS==0
   /* std. version with no implicid bit  */
   /* period lenght: (2**R + 1) * 2**29. */
   unsigned int b0  = br*bs;
#endif
#if IMPLICID_BITS==1
   /* one implicid bit version           */
   /* period lenght: (2**R + 1) * 2**30. */
   unsigned int b0  = br + bs + 2*br*bs;
#endif
#if IMPLICID_BITS==2
   /* two implicid bits version          */
   /* period lenght: (2**R + 1) * 2**31. */
   unsigned int b0, sr, ss;
   sr = br & 1; br ^= sr;
   ss = bs & 1; bs ^= ss;
   b0 = 4*br*bs;
   if (sr) br *= 3;
   if (ss) bs *= 3;
   b0 += br + bs + sr + ss;
#endif
   rands[pos & MASK] = b0;
   return b0 + (b0>>16);    /* low bit improvement */
}

#if 1
#include <stdio.h>

int main()
{
   int i, d=0;
   rand_dia_init(0);
   for (i=0; i<20; i++)
     printf ("%.8x\n", rand_dia());
   
   for (i=0;i<0x1000000;i++)
   {
      d += rand_dia();
   }
   return d;
}
#endif
