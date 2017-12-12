#include <Python.h>
#include <structmember.h>
#include <math.h>
#define FALSE 0
#define TRUE 1

static PyTypeObject Vec2D_Type;

#define Vec2D_check(v) ((v)->ob_type == &Vec2D_Type)



typedef struct {
    PyObject_HEAD
    double x,y,r,t;
    char car,pol;
} Vec2D;

static void Vec2D_dealloc(Vec2D* self){
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *
Vec2D_NEW(char car,char pol,double x,double y,double r,double t){
    Vec2D *self;
    self=PyObject_NEW(Vec2D,&Vec2D_Type);
    if (self !=NULL){
        if (car){
            self->x=x;
            self->y=y;
            self->car=TRUE;
        }else{
            self->x=NAN;
            self->y=NAN;
            self->car=FALSE;
        }
        if (pol){
            self->r=r;
            self->t=t;
            self->pol=TRUE;
        }else{
            self->r=NAN;
            self->t=NAN;
            self->pol=FALSE;
        }
    }
    return (PyObject *)self;
}
        

static PyObject * 
Vec2D_new(PyTypeObject *type, PyObject *args, PyObject *kwds){
    Vec2D *self;
    
    self=(Vec2D *)type->tp_alloc(type,0);
    if (self !=NULL) {
        self->x = NAN;
        self->y = NAN;
        self->r = NAN;
        self->t = NAN;
        self->car = FALSE;
        self->pol = FALSE;
    }
    
    return (PyObject *)self;
}

static int
Vec2D_init(Vec2D *self, PyObject *args, PyObject *kwargs){
    
    //PyObject *x=NULL, *y=NULL, *r=NULL, *t=NULL, *tmp;
    
    static char *kwlist[] = {"x","y","r","t",NULL};
    
    if (!PyArg_ParseTupleAndKeywords(args,kwargs,"|dddd",kwlist,&self->x,&self->y,&self->r,&self->t))
        return -1;
    
    if (!isnan(self->y) && !isnan(self->x))
        self->car=TRUE;
    if (!isnan(self->r) && !isnan(self->t))
        self->pol=TRUE;
    
    return 0;
}

/*
static PyMemberDef Vec2D_members[]={
    {'x',T_DOUBLE, offsetof(Vec2D,x),0,"x coord"},
    {'y',T_DOUBLE, offsetof(Vec2D,y),0,"y coord"),
    {'r',T_DOUBLE, offsetof(Vec2D,r),0,"r coord"),
    {'t',T_DOUBLE, offsetof(Vec2D,t),0,"t coord"),
    {'car',T_BOOL, offsetof(Vec2D,car),0,""),
    {'pol',T_BOOL, offsetof(Vec2D,pol),0,""),
    {NULL} // Sentinel
};
*/
#define degrees(r) ((r)*180.0*M_1_PI)
#define radians(d) ((d)/(180.0)*(M_PI))

static void update_car(Vec2D* self){
    self->x=self->r*cos(self->t);
    self->y=self->r*sin(self->t);
    self->car=TRUE;
}

static void update_pol(Vec2D* self){
    self->r=sqrt(self->x*self->x+self->y*self->y);
    self->t=atan2(self->y,self->x);
    self->pol=TRUE;
}

static PyObject *
Vec2D_add(Vec2D *self,Vec2D *other){
    if (!self->car)
        update_car(self);
    if (!other->car)
        update_car(other);
    double x = self->x+other->x;
    double y = self->y+other->y;
    
    return Vec2D_NEW(TRUE,FALSE,x,y,NAN,NAN);
}

static PyObject*
Vec2D_add_inplace(Vec2D*self,PyObject*args){
    Vec2D* other;
    if (!PyArg_ParseTuple(args,"O",&other))
        return NULL;
    if (!self->car)
        update_car(self);
    if (!other->car)
        update_car(other);
    self->x+=other->x;
    self->y+=other->y;
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
Vec2D_sub(Vec2D *self,Vec2D *other){
    if (!self->car)
        update_car(self);
    if (!other->car)
        update_car(other);
    double x = self->x-other->x;
    double y = self->y-other->y;
    
    return Vec2D_NEW(TRUE,FALSE,x,y,NAN,NAN);
}


static PyObject*
Vec2D_sub_inplace(Vec2D*self,PyObject*args){
    Vec2D* other;
    if (!PyArg_ParseTuple(args,"O",&other))
        return NULL;
    if (!self->car)
        update_car(self);
    if (!self->car)
        update_car(other);
    self->x-=other->x;
    self->y-=other->y;
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
Vec2D_mult(PyObject *a, PyObject *b){
    Vec2D* self;
    double other;
    double x=NAN;
    double y=NAN;
    double r=NAN;
    
    if (Vec2D_check(a)){
        self=(Vec2D*)a;
        other=PyFloat_AsDouble(b);
    }else{
        self=(Vec2D*)b;
        other=PyFloat_AsDouble(a);
    }
    if (self->car){
        x = self->x*other;
        y = self->y*other;
    }
    if (self->pol)
        r = self->r*other;
    return Vec2D_NEW(self->car,self->pol,x,y,r,self->t);
}


static PyObject*
Vec2D_mult_inplace(Vec2D*self,PyObject* args){
    double other;
    if (!PyArg_ParseTuple(args,"f",&other))
        return NULL;
    if (self->car){
        self->x*=other;
        self->y*=other;
    }
    if (self->pol)
        self->r*=other;
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
Vec2D_div(PyObject *a, PyObject *b){
    Vec2D* self;
    double other;
    double x=NAN;
    double y=NAN;
    double r=NAN;
    
    if (Vec2D_check(a)){
        self=(Vec2D*)a;
        other=PyFloat_AsDouble(b);
    }else{
        self=(Vec2D*)b;
        other=PyFloat_AsDouble(a);
    }
    if (self->car){
        x = self->x/other;
        y = self->y/other;
    }
    if (self->pol)
        r = self->r/other;
    return Vec2D_NEW(self->car,self->pol,x,y,r,self->t);
}


static PyObject*
Vec2D_div_inplace(Vec2D*self,PyObject* args){
    
    double other;
    if (!PyArg_ParseTuple(args,"f",&other))
        return NULL;
    if (self->car){
        self->x/=other;
        self->y/=other;
    }
    if (self->pol)
        self->r/=other;
    Py_INCREF(Py_None);
    return Py_None;
}



static PyNumberMethods Vec2D_as_number = {
    Vec2D_add,    // binaryfunc nb_add;         /* __add__ */
    Vec2D_sub,    // binaryfunc nb_subtract;    /* __sub__ */
    Vec2D_mult,   // binaryfunc nb_multiply;    /* __mul__ */
    Vec2D_div,    // binaryfunc nb_divide;      /* __div__ */
    0,            // binaryfunc nb_remainder;   /* __mod__ */
    0,            // binaryfunc nb_divmod;      /* __divmod__ */
    0,            // ternaryfunc nb_power;      /* __pow__ */
    0,            // unaryfunc nb_negative;     /* __neg__ */
    0,            // unaryfunc nb_positive;     /* __pos__ */
    0,            // unaryfunc nb_absolute;     /* __abs__ */
    0,            // inquiry nb_nonzero;        /* __nonzero__ */
    0,            // unaryfunc nb_invert;       /* __invert__ */
    0,            // binaryfunc nb_lshift;      /* __lshift__ */
    0,            // binaryfunc nb_rshift;      /* __rshift__ */
    0,            // binaryfunc nb_and;         /* __and__ */
    0,            // binaryfunc nb_xor;         /* __xor__ */
    0,            // binaryfunc nb_or;          /* __or__ */
    0,            // coercion nb_coerce;        /* __coerce__ */
    0,            // unaryfunc nb_int;          /* __int__ */
    0,            // unaryfunc nb_long;         /* __long__ */
    0,            // unaryfunc nb_float;        /* __float__ */
    0,            // unaryfunc nb_oct;          /* __oct__ */
    0,            // unaryfunc nb_hex;          /* __hex__ */
};

static PyObject*
Vec2D_getcar(Vec2D* self, void*closure){
    if(!self->car)
        update_car(self);
    return PyTuple_Pack(2,PyFloat_FromDouble(self->x),PyFloat_FromDouble(self->y));
}

static int
Vec2D_setcar(Vec2D* self, PyObject* val, void* closure){
    //accepts tuple or int.
    PyObject* x,*y;
    if (val==NULL){
        self->x=NAN;
        self->y=NAN;
        self->car=FALSE;
        return 0;
    }
    if (PyTuple_Check(val)) {
        if (PyTuple_GET_SIZE(val)<2)
            return -1;
        x=PyTuple_GET_ITEM(val,0);//borrowed reference, don't need to decref
        y=PyTuple_GET_ITEM(val,1);
    }else if (PyList_Check(val)) {
        if (PyList_GET_SIZE(val)<2)
            return -1;
        x=PyList_GET_ITEM(val,0);
        y=PyList_GET_ITEM(val,1);
    }else{
        return -1;
    }
    if (!(PyFloat_Check(x)||PyLong_Check(x)))
        return -1;
    if (!(PyFloat_Check(y)||PyLong_Check(y)))
        return -1;
    self->x=PyFloat_AsDouble(x);
    self->y=PyFloat_AsDouble(y);  
    self->car=TRUE;  
    self->pol=FALSE;
    return 0;
}   

static PyObject*
Vec2D_getpol(Vec2D* self, void*closure){
    if(!self->pol)
        update_pol(self);
    return PyTuple_Pack(2,PyFloat_FromDouble(self->r),PyFloat_FromDouble(self->t));
}

static int
Vec2D_setpol(Vec2D* self, PyObject* val, void* closure){
    //accepts tuple or int.
    PyObject* r,*t;
    if (val==NULL){
        self->r=NAN;
        self->t=NAN;
        self->pol=FALSE;
        return 0;
    }
    if (PyTuple_Check(val)) {
        if (PyTuple_GET_SIZE(val)<2)
            return -1;
        r=PyTuple_GET_ITEM(val,0);//borrowed reference, don't need to decref
        t=PyTuple_GET_ITEM(val,1);
    }else if (PyList_Check(val)) {
        if (PyList_GET_SIZE(val)<2)
            return -1;
        r=PyList_GET_ITEM(val,0);
        t=PyList_GET_ITEM(val,1);
    }else{
        return -1;
    }
    if (!(PyFloat_Check(r)||PyLong_Check(r)))
        return -1;
    if (!(PyFloat_Check(t)||PyLong_Check(t)))
        return -1;
    self->r=PyFloat_AsDouble(r);
    self->t=PyFloat_AsDouble(t);
    self->pol=TRUE;    
    self->car=FALSE;
    return 0;
}   


static PyObject*
Vec2D_getx(Vec2D* self,void*closure){
    if (!self->car)
        update_car(self);
    return PyFloat_FromDouble(self->x);
}
static int
Vec2D_setx(Vec2D* self,PyObject* val,void*closure){
//DEPRECATED use setcar
    if (val==NULL){
        self->x=NAN;
        self->car=FALSE;
        return 0;
    }
    if (! (PyLong_Check(val) || PyFloat_Check(val))) {
        PyErr_SetString(PyExc_TypeError,
            "Value must be Int or Float");
        return -1;
    }
    
    self->x=PyFloat_AsDouble(val);
    self->pol=FALSE;
    
    return 0;
}

static PyObject*
Vec2D_gety(Vec2D* self,void*closure){
    if (!self->car)
        update_car(self);
        
    return PyFloat_FromDouble(self->y);
}

static int
Vec2D_sety(Vec2D* self,PyObject* val,void*closure){
    if (val==NULL){
        self->y=NAN;
        self->car=FALSE;
        return 0;
    }
    if (! (PyLong_Check(val) || PyFloat_Check(val))) {
        PyErr_SetString(PyExc_TypeError,
            "Value must be Int or Float");
        return -1;
    }
    
    self->y=PyFloat_AsDouble(val);
    self->pol=FALSE;
    
    return 0;
}

static PyObject*
Vec2D_getr(Vec2D* self,void*closure){
    if (!self->pol)
        update_pol(self);
    return PyFloat_FromDouble(self->r);
}

static int
Vec2D_setr(Vec2D* self,PyObject* val,void*closure){
    if (val==NULL){
        self->r=NAN;
        return 0;
    }
    if (! (PyLong_Check(val) || PyFloat_Check(val))) {
        PyErr_SetString(PyExc_TypeError,
            "Value must be Int or Float");
        return -1;
    }
    
    self->r=PyFloat_AsDouble(val);
    self->car=FALSE;
    return 0;
}

static PyObject*
Vec2D_gett(Vec2D* self,void*closure){
    if (!self->pol)
        update_pol(self);
    return PyFloat_FromDouble(self->t);
}

static int
Vec2D_sett(Vec2D* self,PyObject* val,void*closure){
    if (val==NULL){
        self->t=NAN;
        return 0;
    }
    if (! (PyLong_Check(val) || PyFloat_Check(val))) {
        PyErr_SetString(PyExc_TypeError,
            "Value must be Int or Float");
        return -1;
    }
    
    self->t=PyFloat_AsDouble(val);
    self->car=FALSE;
    
    return 0;
}

static PyObject*
Vec2D_cross(Vec2D* self,PyObject* args){
    Vec2D* other;
    if (!PyArg_ParseTuple(args,"O",&other))
        return NULL;
    //printf("crossing (%f,%f) with (%f,%f)\n",self->x,self->y,other->x,other->y);
    return PyFloat_FromDouble(self->x*other->y-self->y*other->x);
}

static PyObject*
Vec2D_five(Vec2D* self,PyObject* args){
    return PyFloat_FromDouble(5.0);
}

static PyObject*
Vec2D_dot(Vec2D* self,PyObject* args){
    Vec2D* other;
    if (!PyArg_ParseTuple(args,"O",&other))
        return NULL;
    if (!self->car)
        update_car(self);
    if (!other->car)
        update_car(other);
    return PyFloat_FromDouble(self->x * other->x + self->y * other->y);
}

static PyObject*
Vec2D_proj(Vec2D*self,PyObject*args){
    Vec2D*other;
    if(!PyArg_ParseTuple(args,"O",&other))
        return NULL;
    if (!self->car)
        update_car(self);
    if (!other->car)
        update_car(other);
    double S=((self->x)*(other->x)+(self->y)*(other->y))/((other->x)*(other->x)+(other->y)*(other->y));
    if (other->pol) {
        return Vec2D_NEW(TRUE,TRUE,other->x*S,other->y*S,S*other->r,other->t);
    }else{
        return Vec2D_NEW(TRUE,FALSE,other->x*S,other->y*S,NAN,NAN);
    }
}
static PyObject*
Vec2D_rotate(Vec2D* self,PyObject* args){
    
    if (!self->pol)
        update_pol(self);
    double dt;
    if (! PyArg_ParseTuple(args,"d",&dt)){
        printf("failed to parse tuple\n");
        return NULL;
    }
    //printf("t=%f,dt=%f\n",self->t,dt);
    self->t+=dt;
    self->car=FALSE;
    //printf("set t to %f\n",self->t);
    Py_INCREF(Py_None);
    return Py_None;
}



static PyMethodDef Vec2D_methods[]={
/*
    {"x", (PyCFunction)Vec2D_x,METHVARARGS,
        "return x coord"},
    {"y", (PyCFunction)Vec2D_y,METHVARARGS,
        "return y coord"},
    {"r", (PyCFunction)Vec2D_r,METHVARARGS,
        "return r coord"},
    {"t", (PyCFunction)Vec2D_t,METHVARARGS,
        "return t coord"},
*/
    {"cross", (PyCFunction)Vec2D_cross,METH_VARARGS,
        "return cross product"},
    {"dot", (PyCFunction)Vec2D_dot,METH_VARARGS,
        "return dot product"},
    {"rotate", (PyCFunction)Vec2D_rotate,METH_VARARGS,
        "rotate in place"},
    {"add", (PyCFunction)Vec2D_add_inplace,METH_VARARGS,
        "add in place"},
    {"times", (PyCFunction)Vec2D_mult_inplace,METH_VARARGS,
        "multiply in place"},
    {"sub",(PyCFunction)Vec2D_sub_inplace,METH_VARARGS,
        "subtract in place"},
    {"div",(PyCFunction)Vec2D_div_inplace,METH_VARARGS,
        "divide in place"},
    {"five",(PyCFunction)Vec2D_five,METH_VARARGS,
        "five"},
    {"proj",(PyCFunction)Vec2D_proj,METH_VARARGS,
        "vector projection"},
    {NULL,NULL,0,NULL} /*SENTINEL*/
};

/*static Vec2D_getattr(Vec2D *obj, char *name)
{
    return Py.FindMethod(Vec2D_methods, (PyObject *)obj, name);
}
*/

static PyGetSetDef Vec2D_getsetters[]={
    {"x",
        (getter)Vec2D_getx,(setter)Vec2D_setx,
        "x coord", NULL},
    {"y",
        (getter)Vec2D_gety,(setter)Vec2D_sety,
        "y coord", NULL},
    {"r",
        (getter)Vec2D_getr,(setter)Vec2D_setr,
        "r coord",NULL},
    {"t",
        (getter)Vec2D_gett,(setter)Vec2D_sett,
        "t coord",NULL},
    {"car",
        (getter)Vec2D_getcar,(setter)Vec2D_setcar,
        "x,y coords",NULL},
    {"pol",
        (getter)Vec2D_getpol,(setter)Vec2D_setpol,
        "r,t coords",NULL},
    {NULL} /*Sentinel*/
};


static PyObject*
Vec2D_repr(Vec2D* self){
    PyObject*repr;
    PyObject*a,*b,*c,*d,*theta,*degree;
    if (self->car && !self->pol){
        a=PyFloat_FromDouble(self->x);
        b=PyFloat_FromDouble(self->y);
        repr=PyUnicode_FromFormat("Vec2D(x=%R,y=%R)",a,b);
        Py_DECREF(a);
        Py_DECREF(b);
    }else if (self->pol && !self->car){
        a=PyFloat_FromDouble(self->r);
        b=PyFloat_FromDouble(degrees(self->t));
        theta=PyUnicode_FromString("θ");
        degree=PyUnicode_FromString("°");
        repr=PyUnicode_FromFormat("Vec2D(r=%R,%U=%R%U)",a,theta,b,degree);
        Py_DECREF(a);
        Py_DECREF(b);
        Py_DECREF(theta);
        Py_DECREF(degree);
    }else if (self->car && self->pol){
        a=PyFloat_FromDouble(self->x);
        b=PyFloat_FromDouble(self->y);
        c=PyFloat_FromDouble(self->r);
        d=PyFloat_FromDouble(degrees(self->t));
        theta=PyUnicode_FromString("θ");
        degree=PyUnicode_FromString("°");
        repr=PyUnicode_FromFormat("Vec2D(x=%R,y=%R,r=%R,%U=%R%U)",a,b,c,theta,d,degree);
        Py_DECREF(a);
        Py_DECREF(b);
        Py_DECREF(d);
        Py_DECREF(c);
        Py_DECREF(theta);
        Py_DECREF(degree);
    }else{
        Py_INCREF(Py_None);
        return Py_None;
    }
    
    return repr;
}


static PyTypeObject Vec2D_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "vec2d.Vec2D",             /* tp_name */
    sizeof(Vec2D),             /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)Vec2D_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_reserved */
    (reprfunc)Vec2D_repr,      /* tp_repr */
    &Vec2D_as_number,           /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash  */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,   /* tp_flags */
    "Vec2D objects",           /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    Vec2D_methods,             /* tp_methods */
    0,                         /* tp_members */
    Vec2D_getsetters,          /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Vec2D_init,      /* tp_init */
    0,                         /* tp_alloc */
    Vec2D_new,                 /* tp_new */
};

static PyModuleDef vec2dmodule ={
    PyModuleDef_HEAD_INIT,
    "vec2d",
    "Vec2D objects",
    -1,
    NULL,NULL,NULL,NULL,NULL
};

PyMODINIT_FUNC
PyInit_vec2d(void)
{
    PyObject * m;
    
    //vec2d_Vec2DType.tp_new = PyType_GenericNew;
    
    if (PyType_Ready(&Vec2D_Type) < 0)
        return NULL;
        
    m = PyModule_Create(&vec2dmodule);
    if (m==NULL)
        return NULL;
    
    Py_INCREF(&Vec2D_Type);
    PyModule_AddObject(m,"Vec2D",(PyObject *)&Vec2D_Type);
    return m;
};
