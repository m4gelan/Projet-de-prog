#include <math.h>
#include <stdio.h>
// On choisit la nomenclature suivante : "y" pour la durée de simulation (années),"T" pour la période, "f" pour la fréquence, "n" pour la norme, "ord" pour l'ordonnée à l'origine, "e" pour l'exentricité, "B" pour l'obliquité ou inclinaison (nutation), "L" pour la précession , "phi" pour la latitude.

struct Parameter {
    double min;
    double max;
    int T;
    double f;
    double n;
    double ord;
};

double freq_c(int T){
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


int d_calculator(double value_Op, int T, double f, double n, double ord){
	int d = 0;
	int temp = 0;
	for (int i = 0; i < T; i++) {
		double func = cos(f*i)*n + ord;
		if (fabs(func - value_Op) < 0.000001){
			temp = i;
			if (d < temp){
				d = temp;
			}
		}	
	}
	return d;
}

void p_func(int i, double freq, double norme, double origine, int d_value){
	double p_func = cos((i+d_value)*freq)*norme + origine;
	printf("AN : %d\nValeur : %f\n", i, p_func);
}

int main(int argc, char * argv[]){
	struct Parameter e = {0.0034, 0.0580, 413000, freq_c(e.T), norme_c(e.min, e.max), origine_c(e.min, e.max)};
	struct Parameter B = {0.38222711, 0.42760567, 41000, freq_c(B.T), norme_c(B.min, B.max), origine_c(B.min, B.max)};
	struct Parameter L = {0.0, 6.28319, 25920 , freq_c(L.T), norme_c(L.min, L.max), origine_c(L.min, L.max)};
	
	double y = 20;
	//double e_values = [y];
	double e_Op = 0.0167;
	double B_Op = 0.40927971;
	double L_Op = 1.76278;
	
	int d_e = d_calculator(e_Op, e.T, e.f, e.n, e.ord);
	int d_B = d_calculator(B_Op, B.T, B.f, B.n, B.ord);
	for (int i = 0; i < y; i++) {
		printf("\nExentricite \n");
		p_func(i, e.f, e.n, e.ord, d_e);
		//e_values[i] = ;  
		printf("\nObliquite \n");
		p_func(i, B.f, B.n, B.ord, d_B);
		printf("\nPrecession \n");
		printf("AN : %d\nValeur : %f\n", i, L_Op + i*L.f);
		}
	return 0;
}
