#define PY_SSIZE_T_CLEAN
#include <Python.h>
static double rayon_init = 500;

static double calculateur(double rayon){
	rayon = rayon + 50;
	return rayon;
}
static PyObject * simulation(PyObject * self, PyObject * args){
	double rayon;
		if (! PyArg_ParseTuple(args, "did", &rayon)) return NULL;
	PyObject * list = PyList_New(5);
	for (int i =0;i<5;i++){
		PyObject *val = PyFloat_FromDouble(calculateur(rayon+i));
		PyList_SetItem(list, i, val);
	}
	return list;
}

static PyMethodDef methods[] = {
	{"simulation",simulation, METH_VARARGS, "Simulation de la comete."},
	{NULL, NULL,0,NULL}
	};

static struct PyModuleDef moduleDefinition = {
	PyModuleDef_HEAD_INIT,
	"fromCtoPy",
	"Simulation de la comete.",
	-1,
	methods
  };
PyMODINIT_FUNC
PyInit_fromCtoPy(void){
	PyObject * module = PyModule_Create(&moduleDefinition);
	PyModule_AddObject(module,"rayon_init",PyFloat_FromDouble(rayon_init));

		return module;
}
