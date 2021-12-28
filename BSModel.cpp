#include "BSModel.h"

double normalCDF(double value)
{
	double M_SQRT1_2 = pow(0.5, 0.5);
	return 0.5 * erfc(-value * M_SQRT1_2);
}


void BSModel::func() {
	*d1 = (log(*m_S0 / *m_K) + (*m_r +( pow(*m_sigma, 2) / 2)) * *m_T) / (*m_sigma * pow(*m_T, 0.5));
	*d2 = *d1 - *m_sigma * pow(*m_T, 0.5);
}

BSModel::BSModel(double S0, double K, double T, double r, double sigma){
	m_S0 = new double(S0);
	m_K = new double(K);
	m_T = new double(T);
	m_r = new double(r);
	m_sigma = new double(sigma);
	d1 = new double(0);
	d2 = new double(0);
	func();
}

BSModel::BSModel(const BSModel &m) {
	m_K = new double(*m.m_K);
	m_S0 = new double(*m.m_S0);
	m_T = new double(*m.m_T);
	m_sigma = new double(*m.m_sigma);
	m_r = new double(*m.m_r);
	d1 = new double(*m.d1);
	d2 = new double(*m.d2);
}

BSModel::~BSModel() {
	if (m_K != NULL) {
		delete m_K;
		m_K = NULL;
	}
	if (m_S0 != NULL) {
		delete m_S0;
		m_S0 = NULL;
	}
	if (m_T != NULL) {
		delete m_T;
		m_T = NULL;
	}
	if (m_sigma != NULL) {
		delete m_sigma;
		m_sigma = NULL;
	}
	if (m_r != NULL) {
		delete m_r;
		m_r = NULL;
	}
	if (d1 != NULL) {
		delete d1;
		d1 = NULL;
	}
	if (d2 != NULL) {
		delete d2;
		d2 = NULL;
	}
}

double BSModel::call() const {
	double c = *m_S0 * normalCDF(*d1) - *m_K * exp(-(*m_r) * (*m_T)) * normalCDF(*d2);
	return c;
}

double BSModel::put() const {
	double p = *m_K * exp(-(*m_r) * (*m_T)) * normalCDF(-(*d2)) - ((*m_S0) * normalCDF(-(*d1)) );
	return p;
}