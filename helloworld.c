#include <math.h>
#include <stdio.h>

typedef struct{
    double x;
    double y;
} point_t;

int main()
{
    printf("Hello World\n");
    point_t a;
    point_t b;
    point_t* c=&a;
    point_t* d=&b;
    
    a.x=5.;
    a.y=4.;
    
    b.x=7.;
    b.y=-3.;
    
    printf("a.x,a.y=%f,%f\n",a.x,a.y);
    
    printf("c->x,c->y=%f,%f\n",c->x,c->y);
    printf("c->x*c->y=%f\n",c->x*c->y);
    return 0;
}
