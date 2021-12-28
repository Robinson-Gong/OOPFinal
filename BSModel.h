#pragma once
#include <iostream>
#include <string>
#include <array>
#include <math.h>
#include <fstream>
#include <sstream>
#include <vector>
using namespace std;

double normalCDF(double);

class BSModel
{
protected:
	void func();
public:
	BSModel(double, double, double, double, double);
	BSModel(const BSModel& m);
	~BSModel();
	double call() const;
	double put() const;
protected:
	double *m_S0;
	double *m_K;
	double *m_T;
	double *m_sigma;
	double *m_r;
public:
	double *d1;
	double *d2;
};