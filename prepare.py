import pandas as pd
import os

from sklearn.impute import SimpleImputer

from sklearn.model_selection import train_test_split


# prepare data
def prep_zillow17(df):
    imputer = SimpleImputer(strategy='median')
    for col in df.columns:
        if col not in ['fips', 'yearbuilt']:
            df[col] = imputer.fit_transform(df[col].values.reshape(-1, 1))
    df['fips'].fillna(df['fips'].median(), inplace=True)
    df['yearbuilt'].fillna(df['yearbuilt'].median(), inplace=True)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    return df


# function to remove outliers
def remove_outliers(df, k, col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1  # Interquartile range
    fence_low = q1 - k * iqr
    fence_high = q3 + k * iqr
    df = df.loc[(df[col] > fence_low) & (df[col] < fence_high)]
    return df

# outlier removal specific to the data
def remove_outliers_fibs(df, k):
    for col in df.columns:
        if col not in ['fips', 'yearbuilt']:
            df = remove_outliers(df, k, col)
    return df

# common split data function
def split_dataframe(df):
   train, test = train_test_split(df, test_size=0.2, random_state=789)
   train, validate = train_test_split(train, test_size=0.3, random_state=789)
   return train, validate, test 
