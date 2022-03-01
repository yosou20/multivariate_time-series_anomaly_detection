import numpy as np
import random
import pandas as pd
import random
import time
import itertools


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
