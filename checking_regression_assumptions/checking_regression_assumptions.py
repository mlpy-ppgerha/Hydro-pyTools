# -*- coding: utf-8 -*-
'''
Created on Mon Apr 29 13:54:34 2019

@author: Carolina Natel de Moura

Checking Linear Regression Assumptions for the predictors
1) Linear relationship
2) No or little multicollinearity

To check Linear Regression Assumptions for the residuals, go to 
checking_regression_assumptios_residual.py in this repo.
3) Normality of the residuals
4) Homoscedasticity of the residuals
5) Independence of the residuals

P.S.: In case you find any error ou you have any doubt, please contact: carolina.natel@gmail.com

'''

# Initial analysis - predictors (Assumptions 1 and 2)
import pandas as pd
import matplotlib.pyplot as plt

# Importing the dataset
main = pd.read_csv('02651004_monthly.csv').sort_values('Data')
sec1 = pd.read_csv('02651015_monthly.csv').sort_values('Data')
sec2 = pd.read_csv('02651023_monthly.csv').sort_values('Data')
sec3 = pd.read_csv('02651028_monthly.csv').sort_values('Data')
sec4 = pd.read_csv('02651020_monthly.csv').sort_values('Data')

# Select a common period between all the stations, useful for Multiple Linear
# Regression

def intersect_bydate(a, b, c=None, d=None, e=None):
    ''' This function select a period in common between the dataframes provided,
    function only available for minimum two dataframes and maximum five'''
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

dataset = intersect_bydate(main, sec1, sec2, sec3, sec4).dropna(axis = 0).reset_index(drop = True)
dataset.columns = ['Data', 'main', 'sec1', 'sec2', 'sec3', 'sec4']

# Descriptive statistics (using period in common)
data = dataset.iloc[:,1:].astype(float)
describe_data = data.describe()

# Descriptive statistics by station (using all period available)
describe_main = main.describe()
describe_sec1 = sec1.describe()
describe_sec2 = sec2.describe()
describe_sec3 = sec3.describe()
describe_sec4 = sec4.describe()

# No or little Multicollinearity

# Create correlation matrix
data = data.iloc[:,1:] # drop the main station (y variable)
corr = data.corr()

## Graphically display correlations
from pandas.plotting import scatter_matrix
plt.style.use('seaborn-whitegrid')
scatter_matrix(data, figsize=(16,12), alpha = 0.3)
plt.savefig('scatter_matrix.png')

# Select a commom period between two stations, useful for Simple Linear Regression
main_sec1 = intersect_bydate(main, sec1)
main_sec2 = intersect_bydate(main, sec2)
main_sec3 = intersect_bydate(main, sec3)
main_sec4 = intersect_bydate(main, sec4)

# Drop NaN
main_sec1 = main_sec1.dropna(axis = 0)
main_sec2 = main_sec2.dropna(axis = 0)
main_sec3 = main_sec3.dropna(axis = 0)
main_sec4 = main_sec4.dropna(axis = 0)

# Checking linearity

# Plot the scatter plots 
plt.style.use('seaborn-whitegrid')
fig = plt.figure()   # create a plot figure
plt.suptitle('Monthly rainfall (mm)')
# create the first of two panels and set current axis
plt.subplot(2, 2, 1) # (rows, columns, panel number)
plt.scatter(main_sec1.iloc[:,1], main_sec1.iloc[:,2], marker = '.', color = 'black')
plt.xlabel('Main station')
plt.ylabel('sec1')
# create the second panel and set current axis
plt.subplot(2, 2, 2)
plt.scatter(main_sec2.iloc[:,1], main_sec2.iloc[:,2], marker = '.', color = 'black')
plt.xlabel('Main station')
plt.ylabel('sec2')
# create the third of two panels and set current axis
plt.subplot(2, 2, 3) # (rows, columns, panel number)
plt.scatter(main_sec3.iloc[:,1], main_sec3.iloc[:,2], marker = '.', color = 'black')
plt.xlabel('Main station')
plt.ylabel('sec3')
# create the fourth panel and set current axis
plt.subplot(2, 2, 4)
plt.scatter(main_sec4.iloc[:,1], main_sec4.iloc[:,2], marker = '.', color = 'black')
plt.xlabel('Main station')
plt.ylabel('sec4')
fig.savefig('main_sec_scatter.png')

# Saving
describe_data.to_csv('describe.csv')
corr.to_csv('corr_matrix.csv')
fig1.savefig('residuals_scatter_SLR_sec1.png')
fig2.savefig('residual_plot_SLR_sec1.png')
fig3.savefig('residual_normality_SLR_sec1.png')
fig4.savefig('residuals_hist_SLR_sec1.png')
plt.savefig('residuals_fac_SLR_sec1.png')