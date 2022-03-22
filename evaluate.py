# imports
from scipy import stats
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score

from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import f_regression 
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import seaborn as sns


def residuals(df, y, X):
    ''' Plug in the dataframe, target(column), and X(column) to compute the residuals. '''
    baseline = y.mean()
    df['yhat_baseline'] = baseline

    ols_model = LinearRegression().fit(X, y)
    df['yhat'] = ols_model.predict(X)
    
    df['residuals'] = df['yhat'] - y
    df['residual_baseline'] = df['yhat_baseline'] - y
    return

def plot_residuals(df, y, yhat, x):

    # create a residual column if it doesn't already exist
    if 'residuals' not in df.columns:
        df['residuals'] = y - yhat
    else:
        pass
    # create a residuals_baseline column if it doesn't already exist
    if 'residual_baseline' not in df.columns:
        df['residual_baseline'] = y - df['yhat_baseline']
    else:
        pass
    fig, ax = plt.subplots(1, 2, figsize = (10, 5))
    sns.scatterplot(x, y = 'residuals', data = df, ax = ax[0])
    ax[0].axhline(y = 0, color = 'red', linestyle = '--')
    ax[0].set_title('Residuals')
    ax[0].set_xlabel(x)
    ax[0].set_ylabel('Residuals')
    
    sns.scatterplot(x, y = 'residual_baseline', data = df, ax = ax[1])
    ax[1].axhline(y = 0, color = 'red', linestyle = '--')
    ax[1].set_title('Baseline Residuals')
    ax[1].set_xlabel(x)
    ax[1].set_ylabel('Residuals')
    return plt.show()

def regression_errors(df, y, yhat):
    sse = sum((y - yhat) ** 2)
    ess = sum((yhat - df['yhat_baseline']) ** 2)
    tss = ess + sse
    mse = sse / len(df)
    rmse = sqrt(mse)
    # compute explained variance
    r2 = ess/tss
    print('SSE:', round(sse,3))
    print('ESS:', round(ess,3))
    print('TSS:', round(tss,3))
    print('MSE:', round(mse,3))
    print('RMSE:', round(rmse,3))
    print('Explained Variance:', round(r2*100,2),'%')
    return 

def baseline_mean_errors(df, y):
    # create a residual baseline sq column if it doesn't already exist
    if 'residual_baseline_sq' not in df.columns:
        df['residual_baseline_sq'] = (y - df['yhat_baseline']) ** 2
    else:
        pass
    sse_baseline = sum(df['residual_baseline_sq'])
    mse_baseline = sse_baseline/len(df)
    rmse_baseline = sqrt(mse_baseline)
    
    print('SSE baseline:', round(sse_baseline,3))
    print('MSE baseline:', round(mse_baseline,3))
    print('RMSE baseline:', round(rmse_baseline,3))
    return 

def better_than_baseline(df, y, yhat):
    sse = sum((y - yhat) ** 2)
    mse = sse / len(df)
    rmse = sqrt(mse)
    sse_baseline = sum(df['residual_baseline_sq'])
    mse_baseline = sse_baseline/len(df)
    rmse_baseline = sqrt(mse_baseline)

    if sse < sse_baseline and mse < mse_baseline and rmse < rmse_baseline:
        print('The model you created is better than the baseline model.')
    else:
        print('The model you created is not better than the baseline model.')
    return 