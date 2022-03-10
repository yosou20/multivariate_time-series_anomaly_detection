import numpy as np
import random
import pandas as pd
import random
import time
import itertools


import cufflinks as cf
import plotly.graph_objs as go
import plotly.offline as py
import plotly.express as px
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected= True)
cf.go_offline()


def residual_outlier_detection(series, window_size=15, threshold=2.5):
    """Time-series dataset as input parameter

    Args:
        series (dataset): _Time-series dataset_
        window_size (int, optional): _description_. Defaults to 15.
        threshold (float, optional): _description_. Defaults to 2.5.
    """
     
    s_mean = series.rolling(window_size).mean()
    s_mean.fillna(method='bfill', inplace=True)
    residual = series.values - s_mean
    sigma = np.round(residual.std(), 3)
    low_bound = -(threshold * sigma)
    upper_bound = +(threshold * sigma)
    poor_d = (residual < low_bound) | (residual > upper_bound)

    return poor_d  # series[poor_d]


def mean_std_residual_df(df, window=20, threshold=3.5):
    
    '''

    @param df:
    Take time-series dataset (univariate or multivariate)
    @param window:
    Specify rolling window size
    @param threshold:
    rolling window threshold
    @return:
    Return the dataframe along with the computed columns and outlier or anomaly dataset
    '''
    random.seed(101)

    # Computed column for the mean
    df['rolling mean'] = df['WFLOW'].rolling(window).mean()
    df['rolling standard deviation'] = df['WFLOW'].rolling(window).std()
    df.fillna(method='bfill', inplace=True)

    # A computed column for residual is created
    df['residual'] = df.WFLOW - df['rolling mean']

    # static Residual standard deviation is computed
    sigma = np.round(df['residual'].std(), 3)
    # Lower and Upper bounds
    outlier_min = -(threshold * sigma)
    # upper bound
    outlier_max = +(threshold * sigma)
    # Compute outliers
    outlier_df_v1 = df[(df['residual'] < outlier_min) | (df['residual'] > outlier_max)]
    # Print outliers
    # print('length: {} \nWFLOW was NaN: {}\nsigma: {}\n' \
    #      .format(len(outlier_df_v1), len(outlier_df_v1[outlier_df_v1['FilledNaN'] == 1]), sigma))

    # print(outlier_max)

    return df, outlier_df_v1

def plot_anomaly_data22(series, outlier_df):
    fig = go.Figure()
    # Add outlier_df trace
    fig.add_trace(go.Scattergl(x = outlier_df.index, y = outlier_df,
                    mode='markers',
                    name='Outlier Points'))
    #Add df trace
    fig.add_trace(go.Scattergl(x = series.index, y = series, mode = 'lines',
                    name='Actual Data'))
    fig.show()
    

def detect_high_variance_points(series, quantile = 0.9995, window = 5):
    """The method or function takes a time series data, rolling window and a threshold value and return a boolean
    whether some data points are considered as poor data or outlier.
    Args:
        series (_type_): _description_
        quantile (float, optional): _description_. Defaults to 0.9995.
        window (int, optional): _description_. Defaults to 5.

    Returns:
        _type_: boolean  whether  the data is poor /outlier or not.
    """  
    
    series_stds = series.rolling(window).var()
    series_stds.fillna(method='bfill', inplace=True)
    threshold = series_stds.quantile(quantile)
    poor_d = series_stds- series > threshold
       
    return poor_d  # series[poor_d]
