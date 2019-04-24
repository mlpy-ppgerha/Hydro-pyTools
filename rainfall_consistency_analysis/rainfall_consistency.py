# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 09:20:27 2019

@author: carol
"""

### Rainfall Consistency analysis

# Cumulative Double Curve
'''Verification of the homogeneity of the series
Procedure:
1. Several stations are chosen from a homogeneous region; 
2. Accumulate the annual (or monthly) totals of each station; 
3. The average of the totals in each year (or month) is calculated in all the stations and accumulates
this average;
4. The accumulated values of the average of the stations against the totals
accumulated from the post being analyzed.'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importing daily rainfall packed ('standard hidroweb format': month/year)
posto_principal_m = pd.read_csv('02651004.csv') #import the main station
posto_sec1_m = pd.read_csv('02651015.csv')      # import the secundary stations
posto_sec2_m = pd.read_csv('02651023.csv')
posto_sec3_m = pd.read_csv('02651028.csv')
posto_sec4_m = pd.read_csv('02651020.csv')

# Exclude the rows with duplicated date (raw and consisted by ANA data)
def exclude_duplicates(x):
    x = x.sort_values('NivelConsistencia')
    x = x.drop_duplicates(subset= 'Data', keep = 'last')
    
    return x

posto_principal_m = exclude_duplicates(posto_principal_m)
posto_sec1_m = exclude_duplicates(posto_sec1_m)
posto_sec2_m = exclude_duplicates(posto_sec2_m)
posto_sec3_m = exclude_duplicates(posto_sec3_m)
posto_sec4_m = exclude_duplicates(posto_sec4_m)

# Transforming date 'Data' into datetime and sort values by date
def date_transform(x):
    x['Data'] = pd.to_datetime(x.Data, dayfirst = True)
    x = x.sort_values('Data')
    x = x.reset_index(drop = True)
    
    return x

posto_principal_m = date_transform(posto_principal_m)
posto_sec1_m = date_transform(posto_sec1_m)
posto_sec2_m = date_transform(posto_sec2_m)
posto_sec3_m = date_transform(posto_sec3_m)
posto_sec4_m = date_transform(posto_sec4_m)

# Filling the series with NaN
def fill_nan(x):
    helper = pd.DataFrame({'Data': pd.date_range(x.Data.min(), x.Data.max(), freq = 'M')})
    hlp_aux = []
    for i in range(len(helper)):
        aux = helper.iloc[i,0]
        hlp = aux.replace(day=1)
        hlp_aux.append(hlp)
    hlp_aux = pd.DataFrame(hlp_aux)
    hlp_aux.columns = ['Data']
    return hlp_aux

# Apply the correction
helperp = fill_nan(posto_principal_m) 
helper1 = fill_nan(posto_sec1_m) 
helper2 = fill_nan(posto_sec2_m) 
helper3 = fill_nan(posto_sec3_m) 
helper4 = fill_nan(posto_sec4_m) 

# Create a new_df with the correct date and filling the missing data with NaN
posto_principal_m= posto_principal_m.merge(helperp, how='outer').sort_values('Data')
posto_sec1_m= posto_sec1_m.merge(helper1, how='outer').sort_values('Data')
posto_sec2_m= posto_sec2_m.merge(helper2, how='outer').sort_values('Data')
posto_sec3_m= posto_sec3_m.merge(helper3, how='outer').sort_values('Data')
posto_sec4_m= posto_sec4_m.merge(helper4, how='outer').sort_values('Data')

del helperp, helper1, helper2, helper3, helper4 #del variables

# Select a common period between the data for the Consistency Analysis

''' need enhancement - automate'''

posto_principal_m = posto_principal_m.iloc[363:643, :]
posto_sec1_m = posto_sec1_m.iloc[239:519, :]
posto_sec2_m = posto_sec2_m.iloc[5:285, :]
posto_sec3_m = posto_sec3_m
posto_sec4_m = posto_sec4_m.iloc[6:286, :]

# Calculate the cumulative monthly rainfall

def monthly_total(x):
    '''Calculate the total accumulate monthly rainfall in one month (mm)'''
    monthly_rainfall = pd.Series()
    for i in range(len(x)):
        month = x.iloc[i,13:44]
        if month.isnull().sum() > 5:
            total_month = pd.Series(np.nan)
            monthly_rainfall = monthly_rainfall.append(total_month)
        else:
            total_month= pd.Series(month.sum())
            monthly_rainfall = monthly_rainfall.append(total_month)
    return monthly_rainfall

posto_principal_mensal = monthly_total(posto_principal_m)
posto_sec1_mensal = monthly_total(posto_sec1_m)
posto_sec2_mensal = monthly_total(posto_sec2_m)
posto_sec3_mensal = monthly_total(posto_sec3_m)
posto_sec4_mensal = monthly_total(posto_sec4_m)

data = pd.concat([posto_principal_mensal, posto_sec1_mensal, posto_sec2_mensal, posto_sec3_mensal, posto_sec4_mensal], axis = 1)

data = data.dropna(axis = 0) # exclude rows with NaN

posto_principal_mensal = data.iloc[:,0]
posto_sec1_mensal = data.iloc[:,1]
posto_sec2_mensal = data.iloc[:,2]
posto_sec3_mensal = data.iloc[:,3]
posto_sec4_mensal = data.iloc[:,4]

####### Make Double Cumulative Curve
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
     

accu_posto_principal_m = cumulative(posto_principal_mensal).reshape(-1,1)

# Accumulate the regional mean stations

mean_stations = data.mean(axis = 1)
accu_mean = cumulative(mean_stations).reshape(-1, 1)

# Plot the curve

plt.figure()
plt.scatter(accu_mean, accu_posto_principal_m)

# Fitting the Simple Linear Regression model

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(accu_mean, accu_posto_principal_m)
regressor.score(accu_mean, accu_posto_principal_m) # get the R²


