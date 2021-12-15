
// On choisit la nomenclature suivante : "y" pour la durée de simulation (années),"T" pour la période, "f" pour la fréquence, "n" pour la norme, "ord" pour l'ordonnée à l'origine, "e" pour l'exentricité, "B" pour l'obliquité ou inclinaison (nutation), "L" pour la précession , "phi" pour la latitude.
#define PY_SSIZE_T_CLEAN
#include <Python.h>
static double rayon_init = 500;
#include <math.h>
#include <stdio.h>
struct Parameter {
    double min;
    double max;
    int T;
    double f;
    double n;
    double ord;
};

double freq_c(int T){
  double M_PI = 3.14159265358979323846264338327950288419716939937510582097494459230;
	double f = (2*M_PI)/T;
	return f;
}

double norme_c(double min, double max){
	double n = (max-min)/2;
	return n;
}

double origine_c(double min, double max){
	double ord = (max+min)/2;
	return ord;
}


double p_func(int i, double freq, double norme, double origine, int d_value){
	double p_func = cos((i+d_value)*freq)*norme + origine;
	return p_func;
}

int d_calculator(double value_Op, int T, double f, double n, double ord){
	double epsilon = 0.1;
	int temp = 0;
	for (int i = 0; i < T; i++) {
		double func = p_func(i, f, n, ord, 0);
		if (fabs(func - value_Op) < epsilon){
			epsilon = fabs(func - value_Op);
			temp = i;

		}
	}
	return temp;
}



static PyObject * simulation(PyObject * self, PyObject * args){
  //rentre par l'utilisateur
	double excentricite;
	double obliquite;
	double precession;
	int annees;
  //structure ses morts
  struct Parameter e = {0.0034, 0.0580, 413, freq_c(e.T), norme_c(e.min, e.max), origine_c(e.min, e.max)};
	struct Parameter B = {0.38222711, 0.42760567, 41000, freq_c(B.T), norme_c(B.min, B.max), origine_c(B.min, B.max)};
	struct Parameter L = {0.0, 6.28319, 25920 , freq_c(L.T), norme_c(L.min, L.max), origine_c(L.min, L.max)};
 // calculateur
 int d_e = d_calculator(excentricite, e.T, e.f, e.n, e.ord);
 int d_B = d_calculator(obliquite, B.T, B.f, B.n, B.ord);

		if (! PyArg_ParseTuple(args, "dddi", &excentricite, &obliquite, &precession, &annees)) return NULL;
	PyObject * ex_list = PyList_New(annees);
	for (int i =0;i<annees;i++){
		PyObject *val = PyFloat_FromDouble(p_func(i, e.f, e.n, e.ord, d_e));
		PyList_SetItem(ex_list, i, val);
	}
  PyObject * ob_list = PyList_New(annees);
  for (int i =0;i<annees;i++){
		PyObject *val = PyFloat_FromDouble(p_func(i, B.f, B.n, B.ord, d_B));
		PyList_SetItem(ob_list, i, val);
	}
  PyObject * pr_list = PyList_New(annees);
  for (int i =0;i<annees;i++){
    PyObject *val = PyFloat_FromDouble(precession + i*L.f);
    PyList_SetItem(pr_list, i, val);
  }
  PyObject * list = PyList_New(annees);
	PyList_SetItem(list, 0, ex_list);
  PyList_SetItem(list, 1, ob_list);
  PyList_SetItem(list, 2, pr_list);
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
PyInit_final(void){
	PyObject * module = PyModule_Create(&moduleDefinition);
	PyModule_AddObject(module,"rayon_init",PyFloat_FromDouble(rayon_init));

		return module;
}
