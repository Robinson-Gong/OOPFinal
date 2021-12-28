#pragma once
#include <iostream>
#include "BSModel.h"



int main() {
	double S0 ;
	double K ;
	double T ;
	double r;
	double sigma;
	cout << "input current derivative price" << endl;
	cin >> S0;
	cout << "input option's Strike price" << endl;
	cin >> K;
	cout << "input the time to maturity" << endl;
	cin >> T;
	cout << "input the risk-free interest rate" << endl;
	cin >> r;
	cout << "input the volatility of the derivative" << endl;
	cin >> sigma;
	BSModel b = BSModel(S0, K, T, r, sigma);
	cout <<"call option price equal "<< b.call() << endl;
	cout <<"put option d1 equal " << *b.d1 << endl;
	system("pause");
	return 0;
}
