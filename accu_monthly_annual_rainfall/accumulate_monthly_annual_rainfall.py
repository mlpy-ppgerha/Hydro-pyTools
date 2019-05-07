# -*- coding: utf-8 -*-
"""
Created on Thu May  2 22:07:12 2019

@author: Carolina Natel de Moura

This code accumulates monthly and annual rainfall for hidroweb system data
Download data: <http://www.snirh.gov.br/hidroweb/publico/apresentacao.jsf>

P.S.: In case you find any error ou you have any doubt, please contact: carolina.natel@gmail.com
"""
import pandas as pd
import numpy as np

# Importing daily rainfall packed ('standard hidroweb format': month/year)
main = pd.read_csv('02651004.csv', index_col=False) #import the main station
sec1 = pd.read_csv('02651015.csv', index_col=False) #import the secundary stations
sec2 = pd.read_csv('02651023.csv', index_col=False)
sec3 = pd.read_csv('02651028.csv', index_col=False)
sec4 = pd.read_csv('02651020.csv', index_col=False)

# Exclude the rows with duplicated date (raw and consisted by ANA data)
def exclude_duplicates(x):
    x = x.sort_values('NivelConsistencia')
    x = x.drop_duplicates(subset= 'Data', keep = 'last')
    
    return x

main = exclude_duplicates(main)
sec1 = exclude_duplicates(sec1)
sec2 = exclude_duplicates(sec2)
sec3 = exclude_duplicates(sec3)
sec4 = exclude_duplicates(sec4)

# Transforming date 'Data' into datetime and sort values by date
def date_transform(x):
    x['Data'] = pd.to_datetime(x.Data, dayfirst = True)
    x = x.sort_values('Data')
    x = x.reset_index(drop = True)
    
    return x

main = date_transform(main)
sec1 = date_transform(sec1)
sec2 = date_transform(sec2)
sec3 = date_transform(sec3)
sec4 = date_transform(sec4)

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
helperp = fill_nan(main) 
helper1 = fill_nan(sec1) 
helper2 = fill_nan(sec2) 
helper3 = fill_nan(sec3) 
helper4 = fill_nan(sec4) 

# Create a new_df with the correct date and filling the missing data with NaN
main = main.merge(helperp, how='outer').sort_values('Data')
sec1 = sec1.merge(helper1, how='outer').sort_values('Data')
sec2 = sec2.merge(helper2, how='outer').sort_values('Data')
sec3 = sec3.merge(helper3, how='outer').sort_values('Data')
sec4 = sec4.merge(helper4, how='outer').sort_values('Data')

# Calculate the cumulative monthly rainfall

def monthly_total(x):
    '''Calculate the total accumulate monthly rainfall in one month (mm)'''
    monthly_rainfall = pd.Series()
    for i in range(len(x)):
        month = x.iloc[i,13:44]
        if month.isnull().sum() > 5:
            total_month = pd.Series(np.nan)
            monthly_rainfall = monthly_rainfall.append(total_month, ignore_index = True)
        else:
            total_month= pd.Series(month.sum())
            monthly_rainfall = monthly_rainfall.append(total_month, ignore_index = True)
    return monthly_rainfall

main_m = monthly_total(main)
sec1_m = monthly_total(sec1)
sec2_m = monthly_total(sec2)
sec3_m = monthly_total(sec3)
sec4_m = monthly_total(sec4)

helperp = main.iloc[:,2]
helper1 = sec1.iloc[:,2]
helper2 = sec2.iloc[:,2]
helper3 = sec3.iloc[:,2]
helper4 = sec4.iloc[:,2]

main_m = pd.concat([helperp, main_m], axis = 1 )
main_m.columns = ['Data','monthly_rainfall_mm']
sec1_m = pd.concat([helper1, sec1_m], axis = 1)
sec1_m.columns = ['Data', 'monthly_rainfall_mm']
sec2_m = pd.concat([helper2, sec2_m], axis = 1)
sec2_m.columns = ['Data', 'monthly_rainfall_mm']
sec3_m = pd.concat([helper3, sec3_m], axis = 1)
sec3_m.columns = ['Data', 'monthly_rainfall_mm']
sec4_m = pd.concat([helper4, sec4_m], axis = 1)
sec4_m.columns = ['Data', 'monthly_rainfall_mm']

main_m.to_csv('C:/CAROLINA/DOUTORADO/DADOS/02651004_monthly.csv', index = False)
sec1_m.to_csv('C:/CAROLINA/DOUTORADO/DADOS/02651015_monthly.csv', index = False)
sec2_m.to_csv('C:/CAROLINA/DOUTORADO/DADOS/02651023_monthly.csv', index = False)
sec3_m.to_csv('C:/CAROLINA/DOUTORADO/DADOS/02651028_monthly.csv', index = False)
sec4_m.to_csv('C:/CAROLINA/DOUTORADO/DADOS/02651020_monthly.csv', index = False)

del helperp, helper1, helper2, helper3, helper4 #del variables

# Calculate the total annual rainfall
def annual_total(x):
    '''Calculate the total annual cummulative rainfall in each year (mm)'''
    annual_rainfall = pd.Series()
    x_year = np.zeros((len(x),1))
    for i in range(len(x)):
        x_year[i] = x.iloc[i,0].year
    x_year = pd.DataFrame(x_year)
    helper_x = pd.concat([x_year, x.iloc[:,1]], axis = 1)
    helper_x.columns = ['year','monthly_rainfall']
    table = pd.pivot_table(helper_x, index = ['year'], aggfunc = {np.sum, 'count'})
    table = table.reset_index()
    for idx in range(len(table)):
        if table.iloc[idx,1] > 9:
            data = pd.DataFrame(table.iloc[idx,2].reshape(-1,1))
            index = pd.DataFrame(table.iloc[idx,0].reshape(-1,1))
            total_annual = pd. concat([index, data], axis = 1) 
            annual_rainfall = annual_rainfall.append(total_annual)
    return annual_rainfall

main_a = annual_total(main_m)
main_a.columns = ['Year', 'rainfall (mm)']
sec1_a = annual_total(sec1_m)
sec1_a.columns = ['Year', 'rainfall (mm)']
sec2_a = annual_total(sec2_m)
sec2_a.columns = ['Year', 'rainfall (mm)']
sec3_a = annual_total(sec3_m)
sec3_a.columns = ['Year', 'rainfall (mm)']
sec4_a = annual_total(sec4_m)
sec4_a.columns = ['Year', 'rainfall (mm)']

main_a.to_csv('C:/CAROLINA/DOUTORADO/DADOS/02651004_annual.csv', index = False)
sec1_a.to_csv('C:/CAROLINA/DOUTORADO/DADOS/02651015_annual.csv', index = False)
sec2_a.to_csv('C:/CAROLINA/DOUTORADO/DADOS/02651023_annual.csv', index = False)
sec3_a.to_csv('C:/CAROLINA/DOUTORADO/DADOS/02651028_annual.csv', index = False)
sec4_a.to_csv('C:/CAROLINA/DOUTORADO/DADOS/02651020_annual.csv', index = False)