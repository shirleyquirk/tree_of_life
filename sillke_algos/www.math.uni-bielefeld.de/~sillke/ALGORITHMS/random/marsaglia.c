From - Mon Jan 18 13:46:45 1999
From: zaykin@statgen.ncsu.edu (Dmitri Zaykin)
Newsgroups: sci.math.num-analysis,sci.stat.math,sci.math
Subject: Re: Random numbers for C: Improvements.
Supersedes: <790f18msk.fsf@poole.statgen.ncsu.edu>
Date: 18 Jan 1999 00:16:24 GMT
Organization: Statistical Genetics

dwnoon@compuserve.com (David W. Noon) writes:
> The only other language I know of that has sufficiently powerful macro
> facilities to force inlining like C but with better syntax, is 
> portable across many platforms, and produces efficient object code is 
> PL/I. If anybody besides me can use such code, I will produce it 
> too/instead.

Another option is to re-write macros as C++ member functions. If all
the code is in the body of the class or "inline" keyword is explicitly
given, the compiler will attempt to inline the functions.

Below is my version of it and an example of usage. I've put "//"
comments in places where I thought changes to the C code are
necessary. There are additional advantages over C-macros. (1) No
global variables are introduced. (2) It is easy to run several
"independent" random sequences by creating several variables of Rnd
type and seeding them differently (something that would not be
straightforward to do in C).

Dmitri

#include <limits.h> // ULONG_MAX and UCHAR_MAX defined there

class Rnd {
    Rnd() {}
    typedef unsigned long Unlo;
    Unlo z, w, jsr, jcong, t[UCHAR_MAX+1], x, y;
    unsigned char c;
    Unlo znew() { return (z = 36969UL*(z & 65535UL)+(z >> 16)); } // +UL
    Unlo wnew() { return (w = 18000UL*(w & 65535UL)+(w >> 16)); } // +UL
 public:
    Rnd (Unlo i1, Unlo i2, Unlo i3, Unlo i4) 
            : z(i1), w(i2), jsr(i3), jcong(i4), x(0), y(0), c(0) {
        for(int i=0; i<UCHAR_MAX+1; i++) t[i] = Kiss();
    }
    Unlo Mwc() { return (znew() << 16) + wnew(); }
    Unlo Shr3 () { // was: jsr=(jsr=(jsr=jsr^(jsr<<17))^(jsr>>13))^(jsr<<5)
        jsr=jsr^(jsr<<17);
        jsr=jsr^(jsr>>13); 
        return (jsr=jsr^(jsr<<5));
    }
    Unlo Cong() { return (jcong = 69069UL*jcong + 1234567UL); } // +UL
    Unlo Kiss() { return (Mwc() ^ Cong()) + Shr3(); }
    Unlo Swb () { // was: t[c+237]=(x=t[c+15])-(y=t[c]+(x<y)),t[++c]
        x = t[(c+15) & 0xFF];
        t[(c+237) & 0xFF] = x - (y = t[(c+1) & 0xFF] + (x < y));
        return t[++c];
    }
    Unlo Lfib4() { // was: t[c]=t[c]+t[c+58]+t[c+119]+t[c+178],t[++c]
        t[c]=t[c]+t[(c+58) & 0xFF]+t[(c+119) & 0xFF]+t[(c+179) & 0xFF];
        return t[++c];
    }
    double Uni() { return Kiss() * 2.328306e-10; }
    double Vni() { return long(Kiss()) * 4.656613e-10; }
    double operator () () { return Uni(); }
    Unlo operator () (Unlo n) {
        return n == 1 ? 0 : Kiss() / (ULONG_MAX/n + 1);
    }
    double operator () (double Min, double Max) { return Min+Uni()*(Max-Min); }
};

// example of usage

#include <time.h>
#include <iostream.h>

int main() 
{
    unsigned i, seed=time(0);
    Rnd rn (seed, 2*seed, 3*seed, 4*seed);

    for(i=0; i<5; i++) cout << rn(5) << endl;      // [0, 1, 2, 3, 4]
    for(i=0; i<5; i++) cout << rn() << endl;       // (0, ..., 1)
    for(i=0; i<5; i++) cout << rn.Vni() << endl;   // (-1, ..., 1)
    for(i=0; i<5; i++) cout << rn(10, 20) << endl; // (10, ..., 20)
    for(i=0; i<5; i++) cout << rn.Lfib4() << endl; // trying Lfib4
    for(i=0; i<5; i++) cout << rn.Swb() << endl;   // trying Swb
}

-----------------------------------------------------------------------------
From - Thu Jan 21 15:28:34 1999
From: zaykin@statgen.ncsu.edu (Dmitri Zaykin)
Newsgroups: sci.stat.math,sci.math,sci.math.num-analysis
Subject: Re: Random numbers for C: Improvements.
Date: 21 Jan 1999 04:40:53 GMT
Organization: Statistical Genetics

To check if C-macros for these random number generators do indeed
always produce faster, and maybe "less bloated" code than inlined C++
member functions, I did a little experiment with timing/code size
using the GNU compiler (egcs-1.1.1 g++/gcc) on Solaris 2.5.1. With
this compiler, it is clearly not the case.

(1) Executable size (conclusion: C++ code smaller)

inlined member functions   C-macros              C-macros
g++ -Winline -O2 -s        g++ -Winline -O2 -s   gcc -Winline -O2 -s
8908                       9820                  9532


(2) Timing in 10 experiments (conclusion: C++ code faster)

inlined member functions   C-macros              C-macros
g++ -Winline -O2 -s        g++ -Winline -O2 -s   gcc -Winline -O2 -s
11330000                   15030000              14500000
11330000                   15040000              14470000
11340000                   15030000              14490000
11340000                   15040000              14520000
11340000                   15030000              14500000
11320000                   15030000              14490000
11340000                   15040000              14480000
11340000                   15030000              14510000
11340000                   15030000              14500000
11340000                   15030000              14500000

//-----------------------------------------------------
// C++ code:

#include <stdio.h>
#include <time.h>
#include <limits.h>

class Rnd {
    Rnd() {}
    typedef unsigned long Unlo;
    typedef unsigned char Uc;
    Unlo z, w, jsr, jcong, t[UCHAR_MAX+1], x, y, a, b;
    unsigned char c;
    Unlo znew() { return (z = 36969UL*(z & 65535UL)+(z >> 16)); }
    Unlo wnew() { return (w = 18000UL*(w & 65535UL)+(w >> 16)); }
 public:
    Rnd (Unlo i1, Unlo i2, Unlo i3, Unlo i4, Unlo i5, Unlo i6) 
            : z(i1), w(i2), jsr(i3), jcong(i4), x(0), y(0), 
              a(i5), b(i6), c(0) {
        for(int i=0; i<UCHAR_MAX+1; i++) t[i] = Kiss();
    }
    Unlo Mwc() { return (znew() << 16) + wnew(); }
    Unlo Shr3 () {
        jsr=jsr^(jsr<<17);
        jsr=jsr^(jsr>>13); 
        return (jsr=jsr^(jsr<<5));
    }
    Unlo Cong() { return (jcong = 69069UL*jcong + 1234567UL); }
    Unlo Kiss() { return (Mwc() ^ Cong()) + Shr3(); }
    Unlo Swb () {
        x = t[(Uc)(c+15)];
        t[(Uc)(c+237)] = x - (y = t[(Uc)(c+1)] + (x < y));
        return t[++c];
    }
    Unlo Lfib4() {
        t[c]=t[c]+t[(Uc)(c+58)]+t[(Uc)(c+119)]+t[(Uc)(c+179)];
        return t[++c];
    }
    Unlo Fib() { b=a+b; return (a=b-a); }
    double Uni() { return Kiss() * 2.328306e-10; }
    double Vni() { return long(Kiss()) * 4.656613e-10; }
    double operator () () { return Uni(); }
    Unlo operator () (Unlo n) {
        return n == 1 ? 0 : Kiss() / (ULONG_MAX/n + 1);
    }
    double operator () (double Min, double Max) { return Min+Uni()*(Max-Min); }
};

int main()
{
    unsigned long i, xx=0, seed=time(0);
    long spent;
    Rnd rn (seed, 2*seed, 3*seed, 4*seed, 5*seed, 6*seed);

    spent=clock();
    for(i=0; i<77777777; i++) xx += (rn.Kiss() + rn.Swb());
    printf ("%ld \t", clock()-spent);

    printf("\n");
}

/*****************************************************************/
/* C-macros */

#include <stdio.h>
#include <time.h>
#include <limits.h>

#define znew   (z=36969UL*(z&65535UL)+(z>>16))
#define wnew   (w=18000UL*(w&65535UL)+(w>>16))
#define MWC    ((znew<<16)+wnew )
#define SHR3  (jsr^=(jsr<<17), jsr^=(jsr>>13), jsr^=(jsr<<5))
#define CONG  (jcong=69069UL*jcong+1234567UL)
#define FIB   ((b=a+b),(a=b-a))
#define KISS  ((MWC^CONG)+SHR3)
#define UC    (unsigned char)
#define LFIB4 (c++,t[c]=t[c]+t[UC(c+58)]+t[UC(c+119)]+t[UC(c+178)])
#define SWB   (x = t[UC(c+15)], t[UC(c+237)] = x-(y=t[UC(c+1)]+(x<y)), t[++c])
#define UNI   (KISS*2.328306e-10)
#define VNI   ((long) KISS)*4.656613e-10
typedef unsigned long Un;
static Un z=362436069UL, w=521288629UL, jsr=123456789UL, jcong=380116160UL;
static Un a=224466889UL, b=7584631UL, t[256];
static Un x=0,y=0; static unsigned char c=0;
void settable(Un i1,Un i2,Un i3,Un i4,Un i5, Un i6)
{ int i; z=i1;w=i2,jsr=i3; jcong=i4; a=i5; b=i6;
 for(i=0;i<256;i=i+1)  t[i]=KISS;
}

int main()
{
    unsigned long i, xx=0, seed=time(0);
    long spent;
    
    settable (seed, 2*seed, 3*seed, 4*seed, 5*seed, 6*seed);

    spent=clock();
    for(i=0; i<77777777; i++) xx += (KISS + SWB);
    printf ("%ld \t", clock()-spent);

    printf("\n");
    return 0;
}
