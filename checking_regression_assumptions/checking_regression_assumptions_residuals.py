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
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Residual analysis (Assumptions 3 - 5)
residuals = pd.read_csv('residuals_SLR_sec1.csv')
y_pred = pd.read_csv('y_pred_SLR_sec1.csv')

# Plotting residuals
t = range(len(residuals))
fig1 = plt.figure()
plt.plot(t, residuals, '.')
plt.hlines(0,0,len(t))

# Checking homoscedasticity
fig2 = plt.figure()
plt.scatter(y_pred, residuals, color='darkblue')
plt.title("Residual Plot")
plt.xlabel("Predicted value")
plt.ylabel("Residual")

# Calculate Levene Test
from scipy.stats import levene
lev = levene(residuals, y_pred)
print('statistic: {}'.format(lev[0]) + '\n' 'p-value: {}'.format(lev[1]))

# Checking residuals normality
# by plotting
import scipy.stats as stats
fig3 = plt.figure()
stats.probplot(residuals.iloc[:,0], plot= plt)
plt.title("Model1 Residuals Probability Plot")

fig4 = plt.figure()
plt.hist(residuals.iloc[:,0])

# by Kolmogorov-Smirnov test
ks = stats.kstest(residuals, 'norm', args = (residuals.mean(), residuals.std()))
print('statistic: {}'.format(ks[0]) + '\n' 'p-value: {}'.format(ks[1]))

# Checking residuals randomness
sm.graphics.tsa.plot_acf(residuals, lags=40)
plt.title('Autocorrelation function')
plt.xlabel('Number of lags')
plt.ylabel('FAC')

from statsmodels.stats.stattools import durbin_watson
durbin_w = durbin_watson(residuals)
print('Durbin-Watson: {}'. format(durbin_w))
#For no serial correlation, the test statistic equals 2.
# This statistic will always be between 0 and 4. The closer to 0 the statistic, 
# the more evidence for positive serial correlation. The closer to 4, 
#the more evidence for negative serial correlation.

# Saving
fig1.savefig('residuals_scatter_SLR_sec1.png')
fig2.savefig('residual_plot_SLR_sec1.png')
fig3.savefig('residual_normality_SLR_sec1.png')
fig4.savefig('residuals_hist_SLR_sec1.png')
plt.savefig('residuals_fac_SLR_sec1.png')