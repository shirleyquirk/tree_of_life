cp_coefs=[[0,  1.10177994, -9.12488794, 31.65096789, -53.56758182, 52.39764154, -30.68624919, 10.69988939, -2.05311671,  0.1693529 ],
[0, 2.53262608, -9.29224367, 31.29683222, -54.85782455, 54.23485481, -31.68717966, 10.97960069, -2.09334234,  0.1717265 ],
[0,  3.1142652,  -9.24014357, 31.05593582, -54.29775047, 53.39726145, -31.13060499, 10.79497664, -2.06279961,  0.16970231],
[0,  3.55860697, -9.19094005, 30.87611178, -53.95849362, 52.98371489, -30.89674269, 10.7280363,  -2.05319676,  0.16914954],
[0,  3.93465299, -9.16423824, 30.78221519, -53.78889228, 52.78150997, -30.79194166, 10.70153434, -2.04995398,  0.16899786],
[0,  4.26685546, -9.14927397, 30.73063651, -53.69794999, 52.67188438, -30.73963465, 10.69015391, -2.04888215,  0.16897031],
[0,  4.56769065, -9.14040046, 30.70048633, -53.64574663, 52.60715686, -30.71141412, 10.68517718, -2.04863979,  0.16898431],
[0,  4.84462486, -9.13487522, 30.68193808, -53.61414117, 52.56630459, -30.69535434, 10.68315835, -2.04873177,  0.16901164],
[0,  5.10256151, -9.13129754, 30.67006216, -53.59421713, 52.53911576, -30.68589259, 10.68258249, -2.04895633,  0.16904186],
[0,  5.34492882, -9.12890832, 30.66221984, -53.58127072, 52.52021802, -30.68021161, 10.68272934, -2.04922595,  0.16907102],
[0,  5.57423545, -9.12727375, 30.65691748, -53.57267006, 52.5065965, -30.67678952, 10.68323647, -2.04950158,  0.16909774]]

import itertools,math
import sys
if sys.version_info[0]==3:
    from vec2d import Vec2D

def cp(c,i):
    if c<0:
        return -sum([coef*(-c)**(idx/2) for idx,coef in enumerate(cp_coefs[i])])
    else:
        return sum([coef*c**(idx/2) for idx,coef in enumerate(cp_coefs[i])])

def integ_cp(c,i):
    return sum([coef/(idx/2+1)*c**(idx/2+1) for idx,coef in enumerate(cp_coefs[i])])

if sys.version_info[0]==2:
    def zip_longest(l1,l2):
        return itertools.izip_longest(l1,l2)
else:
    def zip_longest(l1,l2):
        return itertools.zip_longest(l1,l2)
class Poly(list):
    def __mul__(self,other):
        if type(other) not in (Poly,list,tuple):
            other=[other]
        ret=Poly([0]*(len(self)+len(other)-1))
        for idx,s in enumerate(self):
            for jdx,o in enumerate(other):
                ret[idx+jdx]+=s*o
        return ret
    def __rmul__(self,other):
        return self.__mul__(other)
    def __add__(self,other):
        if type(other) not in (Poly,list,tuple):
            other=[other]
        return Poly([sum([j if j else 0 for j in i]) for i in zip_longest(self,other)])
    def __radd__(self,other):
        return self.__add__(other)
    def __pow__(self,other):
        if type(other) != int:
            if type(other)==float and int(other)==other:
                other=int(other)
            else: 
                raise ValueError("Can Only Raise to Integer Powers, not ",other,type(other))
        ret=Poly([1])
        for o in range(other):
            ret=ret*self
        return ret
    def integrate(self):
        return Poly([0,0]+[coef/(idx/2+1) for idx,coef in enumerate(self)])
    def deriv(self):#fuck, have to deal with negative half powers
        assert(self[1]==0)
        return Poly([coef*(idx/2-1) for idx,coef in enumerate(self[2:])])
    def _(self,s):
        if s<0:
            return -sum([coef*(-s)**(idx/2) for idx,coef in enumerate(self)])
        else:
            return sum([coef*s**(idx/2) for idx,coef in enumerate(self)])
    def as_f_of(self,other):
        if type(other) != Poly:
            if type(other) in (tuple,list):
                other=Poly(other)
            else:
                other=Poly([other])
        ret=Poly([0])
        for idx,s in enumerate(self):
            if (idx//2)!=idx/2:
                if s!=0:#half power coefficients must be zero
                    raise ValueError("Half Power Coefficients Must be Zero",other)
            else:
                ret=ret+s*(other**(idx//2))
        return ret
def whole_poly(l):
    ret=Poly()
    for i in zip(l,[0]*len(l)):
        ret.extend(i)
    return ret
def theta(t0,c0,c,i):
    if c0<0:
        if c<0:
            return t0-integ_cp(-c0,i)+integ_cp(-c,i)
        else:
            return t0-integ_cp(-c0,i)+integ_cp(c,i)
    else:
        return t0+integ_cp(c,i)-integ(c0,i)

def theta_s(t0,c0,c1,s,i):
    pi=Poly(cp_coefs[i]).integrate()
    c=Poly([c0,0,c1-c0])
    c.fog(pi)##wont work.
def poly_theta(t0,c0,i):
    pi=(Poly(cp_coefs[i])).integrate()
    #c>0,c0>0: t0+pi-pi._(c0) 
    #c0<0,c<0: pi._(c0) - pi._(c) 
    #c0<0,c>0: pi._(c0) + pi._(c)
    return t0-pi._(c0)+pi
def cos(poly,order):
    #o=0: (1)
    #o=1: (1,0,0,0,-1/2)
    #o=2: (1,0,0,0,-1/2,0,0,0,1/24)
    if order==0:
        return Poly([0])
    ret=Poly([0]*(4*order-3))
    for i in range(order):
        ret[4*i]=((-1)**i/math.factorial(2*i))
        #print(i,math.factorial(2*i),ret[4*i])
    #print(ret)
    return ret.as_f_of(poly)
def sin(poly,order):
    #o=0: (0,0,1)
    #o=1: (0,0,1,0,0,0,-1/6)
    #o=2: (0,0,1,0,0,0,-1/6,0,0,0,1/120)
    if order==0:
        return Poly([0])
    ret=Poly([0]*(4*order-1))
    for i in range(order):
        ret[4*i+2]=(-1)**i/math.factorial(2*i+1)
    #print(ret)
    return ret.as_f_of(poly)
def _int(p,c0,c1,s):
    ret=0
    c=c0+(c1-c0)*s
    for idx,coef in enumerate(p):
        ret+=coef*abs(c)**(idx/2+1)/((c1-c0)*(idx/2+1))
    return ret*(-1 if c>0 else 1)
    
def xy(t0,c0,c1,s,i):
    #x=integral(cos(theta)ds), not dc) but integrate by parts:
    #integral(a+bs)^n=(a+bs)^(n+1)/(b(n+1))
    pi=(Poly(cp_coefs[i])).integrate()
    #pi[0]+=t0
    theta=t0-pi._(c0)+(-1 if c0<0 else 1)*pi
    while theta._(abs(c0+(c1-c0)*s))>math.pi:
        theta[0]-=2*math.pi
    while theta._(abs(c0+(c1-c0)*s))<-math.pi:
        theta[0]+=2*math.pi
    xpoly=cos(theta,3)#gives good cos from -pi to pi
    ypoly=sin(theta,3)
    x=0
    y=0
    for idx,coef in enumerate(xpoly):
        x+=coef*(-1 if c0<0 else 1)*abs(c0+(c1-c0)*s)**(idx/2+1)/((c1-c0)*(idx/2+1))-(-1 if c0<0 else 1)*coef*abs(c0)**(idx/2+1)/((c1-c0)*(idx/2+1))
    for idx,coef in enumerate(ypoly):
        y+=coef*(-1 if c0<0 else 1)*abs(c0+(c1-c0)*s)**(idx/2+1)/((c1-c0)*(idx/2+1))-(-1 if c0<0 else 1)*coef*abs(c0)**(idx/2+1)/((c1-c0)*(idx/2+1))
    return (x,y)
