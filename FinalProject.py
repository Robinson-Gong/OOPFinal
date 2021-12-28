# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 17:01:54 2021

@author: Yiyu Gong
"""

import os
os.chdir(os.path.split(os.path.realpath(__file__))[0])
import pandas as pd
import numpy as np
import akshare as ak
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from scipy import optimize

if not os.path.isfile("logfile.csv"):
    df = pd.DataFrame(columns=['Time','Stock_name', 'currentPrice','Time to maturity','Libor_T', "T days'volatility based on NGarch with 5 year_historical data"])
    df.to_csv('logfile.csv',index=False)
else:
    df = pd.read_csv('logfile.csv')

stock,T = input().split()
T = float(T)

time0 = time.strftime("%Y%m%d", time.localtime())
time1 = (datetime.now() - relativedelta(years=5)).strftime("%Y%m%d")

df1 = ak.stock_us_hist(symbol= stock , start_date= time1, end_date= time0)

if T < 7/365:
    hist_df = ak.rate_interbank(market="伦敦银行同业拆借市场", symbol="Libor美元", indicator="隔夜",need_page="1")
elif T < 1/12:
    hist_df = ak.rate_interbank(market="伦敦银行同业拆借市场", symbol="Libor美元", indicator="1周",need_page="1")
elif T < 1/6:
    hist_df = ak.rate_interbank(market="伦敦银行同业拆借市场", symbol="Libor美元", indicator="1月",need_page="1")
elif T < 1/4:
    hist_df = ak.rate_interbank(market="伦敦银行同业拆借市场", symbol="Libor美元", indicator="2月",need_page="1")
elif T < 2/3:
    hist_df = ak.rate_interbank(market="伦敦银行同业拆借市场", symbol="Libor美元", indicator="3月",need_page="1")
else:
    hist_df = ak.rate_interbank(market="伦敦银行同业拆借市场", symbol="Libor美元", indicator="8月",need_page="1")

df1['return'] = np.log(1+df1['收盘'].pct_change(int(252*T)))

df1 = df1.dropna()
df1 = df1.reset_index(drop = True)

def getNegativeLoglikelihood3(params,r):
    omega,alpha,beta,theta = params
    sigma2 = np.ones(len(r))
    sigma2[0] = np.var(r)
    for i in range(1,len(r)):
        s = omega + alpha * (r[i - 1] - theta*sigma2[i-1]**0.5)**2 + beta * sigma2[i - 1]
        sigma2[i] = (s>0)*s+(s<0)*100
    LogLikeLihood =  (np.log(2*np.pi) + np.log(sigma2) + r**2/sigma2).sum()/2
    return LogLikeLihood 

params_MLE2 = optimize.fmin(getNegativeLoglikelihood3,np.array([0.0000015,0.05,0.8,1.25]),  \
                                       args=(df1['return'],), ftol = 0.00001)

omega,alpha,beta,theta = params_MLE2
df1['sigma2'] = np.var(df1['return'])
for i in range(1,df1.shape[0]):
    df1.loc[i,'sigma2'] =  omega + alpha * (df1.loc[i - 1,'return'] - theta*df1.loc[i-1,'sigma2']**0.5)**2 + beta * df1.loc[i - 1,'sigma2']

df = df.append(pd.DataFrame({'Time':[time0],'Stock_name':[stock],'currentPrice':[df1.iloc[-1,2]],'Time to maturity':[T],'Libor_T':[hist_df.iloc[0,1]*0.01],"T days'volatility based on NGarch with 5 year_historical data":[pow(df1.iloc[-1,-1],0.5)]}),ignore_index=True)

df.to_csv('logfile.csv',index=False)