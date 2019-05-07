# -*- coding: utf-8 -*-
'''
Created on Tue Apr 30 22:01:07 2019

@author: Carolina Natel de Moura

Checking Linear Regression Assumptions for residuals
3) Normality of the residuals
4) Homoscedasticity of the residuals
5) Independence of the residuals

To check Linear Regression Assumptions for predictors, go to 
checking_regression_assumptions.pyin this repo

P.S.: In case you find any error ou you have any doubt, please contact: carolina.natel@gmail.com
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importing monthly rainfall
main = pd.read_csv('02651004_monthly.csv', index_col=False) #import the main station
sec1 = pd.read_csv('02651015_monthly.csv', index_col=False) #import the secondary stations
sec2 = pd.read_csv('02651023_monthly.csv', index_col=False)
sec3 = pd.read_csv('02651028_monthly.csv', index_col=False)
sec4 = pd.read_csv('02651020_monthly.csv', index_col=False)

# Select a common period between main station and secondary stations
def intersect_bydate(a, b, c=None, d=None, e=None):
    df = pd.DataFrame()
    df_final = pd.DataFrame()
    helper_b = b.set_index('Data', inplace = False)
    if c is not None and d is not None  and e is not None:
        helper_c = c.set_index('Data', inplace = False)
        helper_d = d.set_index('Data', inplace = False)
        helper_e = e.set_index('Data', inplace = False)
        for i in range(len(a)):
            aux_a = a.iloc[i,:]
            aux = aux_a[0]
            if helper_b.index.contains(aux) and helper_c.index.contains(aux) and helper_d.index.contains(aux) and helper_e.index.contains(aux):
                idx_b = helper_b.index.get_loc(aux)
                idx_c = helper_c.index.get_loc(aux)
                idx_d = helper_d.index.get_loc(aux)
                idx_e = helper_e.index.get_loc(aux)
                value_a = pd.DataFrame(a.iloc[i,:]).T.reset_index(drop = True)
                value_b = pd.DataFrame(b.iloc[idx_b,1:2]).T.reset_index(drop = True)
                value_c = pd.DataFrame(c.iloc[idx_c,1:2]).T.reset_index(drop = True)
                value_d = pd.DataFrame(d.iloc[idx_d,1:2]).T.reset_index(drop = True)
                value_e = pd.DataFrame(e.iloc[idx_e,1:2]).T.reset_index(drop = True)
                df = pd.concat([value_a, value_b, value_c, value_d, value_e], axis = 1)
                df_final = df_final.append(df).sort_values('Data')  
    elif c is not None and d is not None and e is None:
        helper_c = c.set_index('Data', inplace = False)
        helper_d = d.set_index('Data', inplace = False)
        for i in range(len(a)):
            aux_a = a.iloc[i,:]
            aux = aux_a[0]
            if helper_b.index.contains(aux) and helper_c.index.contains(aux) and helper_d.index.contains(aux):
                idx_b = helper_b.index.get_loc(aux)
                idx_c = helper_c.index.get_loc(aux)
                idx_d = helper_d.index.get_loc(aux)
                value_a = pd.DataFrame(a.iloc[i,:]).T.reset_index(drop = True)
                value_b = pd.DataFrame(b.iloc[idx_b,1:2]).T.reset_index(drop = True)
                value_c = pd.DataFrame(c.iloc[idx_c,1:2]).T.reset_index(drop = True)
                value_d = pd.DataFrame(d.iloc[idx_d,1:2]).T.reset_index(drop = True)
                df = pd.concat([value_a, value_b, value_c, value_d], axis = 1)
                df_final = df_final.append(df).sort_values('Data')
    elif c is not None and d is None and e is None:
        helper_c = c.set_index('Data', inplace = False)
        for i in range(len(a)):
            aux_a = a.iloc[i,:]
            aux = aux_a[0]
            if helper_b.index.contains(aux) and helper_c.index.contains(aux):
                idx_b = helper_b.index.get_loc(aux)
                idx_c = helper_c.index.get_loc(aux)
                value_a = pd.DataFrame(a.iloc[i,:]).T.reset_index(drop = True)
                value_b = pd.DataFrame(b.iloc[idx_b,1:2]).T.reset_index(drop = True)
                value_c = pd.DataFrame(c.iloc[idx_c,1:2]).T.reset_index(drop = True)
                df = pd.concat([value_a, value_b, value_c], axis = 1)
                df_final = df_final.append(df).sort_values('Data')
    elif c is None and d is None and e is None:
        for i in range(len(a)):
            aux_a = a.iloc[i,:]
            aux = aux_a[0]
            if helper_b.index.contains(aux):
                idx_b = helper_b.index.get_loc(aux)
                value_a = pd.DataFrame(a.iloc[i,:]).T.reset_index(drop = True)
                value_b = pd.DataFrame(b.iloc[idx_b,1:2]).T.reset_index(drop = True)
                df = pd.concat([value_a, value_b], axis = 1)
                df_final = df_final.append(df).sort_values('Data')
    return df_final

main_sec = intersect_bydate(main, sec1, sec2, sec3, sec4).dropna(axis = 0).reset_index(drop = True)
main_sec = main_sec.iloc[:,1:].astype(float)
main_sec.columns = ['main', 'sec1', 'sec2', 'sec3', 'sec4']

main_m = main_sec.iloc[:,0]
sec1_m = main_sec.iloc[:,1]
sec2_m = main_sec.iloc[:,2]
sec3_m = main_sec.iloc[:,3]
sec4_m = main_sec.iloc[:,4]

del main, sec1, sec2, sec3, sec4

# Make Double Cumulative Curve
# Accumulate values by station
def cumulative(x): 
    cum = [] 
    aux = []
    total = []
    for i in range(len(x)):
        stored = total
        aux = x.iloc[i]
        if len(cum) == 0:
            total = aux
        else:
            total = stored + aux
        cum.append(total)
    return np.asarray(cum)
     
accu_main_m = cumulative(main_m).reshape(-1,1)

# Accumulate the regional mean stations
mean_stations = main_sec.mean(axis = 1)
accu_mean = cumulative(mean_stations).reshape(-1, 1)

# Plot the curve
plt.style.use('seaborn-whitegrid')
fig = plt.figure()
plt.title("Double-Mass Curve (Monthly)")
ax = plt.axes()
plt.scatter(accu_mean, accu_main_m, marker = '.', color = 'black')
plt.xlabel('Regional accu rainfall (mm)')
plt.ylabel('Accu rainfall at main station (mm)')

fig.savefig('PortoVitoria_doubleMass.png')