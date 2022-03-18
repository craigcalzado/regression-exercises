import pandas as pd
import numpy as np
import os

from sklearn.impute import SimpleImputer

from sklearn.model_selection import train_test_split

from env import host, user, password

def get_zillow17_data(use_cache=True):
    filename = "zillow.csv"
    if os.path.isfile(filename) and use_cache:
        print("Let me get that for you...")
        return pd.read_csv(filename)
    print("Sorry, nothing on file, let me create one for you...")
    data = 'zillow'
    url = f'mysql+pymysql://{user}:{password}@{host}/{data}'
    query = '''
            SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
            FROM properties_2017
            LEFT JOIN propertylandusetype USING (propertylandusetypeid)
            WHERE propertylandusedesc IN ('Single Family Residential')
            '''
    zillow17_data = pd.read_sql(query, url)
    zillow17_data.to_csv(filename)
    return zillow17_data

# fuction for lesson
def wrangle_grades():
    """
    Read student_grades csv file into a pandas DataFrame,
    drop student_id column, replace whitespaces with NaN values,
    drop any rows with Null values, convert all columns to int64,
    return cleaned student grades DataFrame.
    """
    # Acquire data from csv file.
    grades = pd.read_csv("student_grades.csv")
    # Replace white space values with NaN values.
    grades = grades.replace(r"^\s*$", np.nan, regex=True)
    # Drop all rows with NaN values.
    df = grades.dropna()
    # Convert all columns to int64 data types.
    df = df.astype("int")
    return df
# acquire data from csv file

def get_telco_data(use_cache=True):
    filename = "telco.csv"
    if os.path.isfile(filename) and use_cache:
        print("Let me get that for you...")
        return pd.read_csv(filename)
    print("Sorry, nothing on file, let me create one for you...")
    data = 'telco_churn'
    url = f'mysql+pymysql://{user}:{password}@{host}/{data}'
    query = '''
    SELECT * FROM customers 
    JOIN contract_types USING (contract_type_id) 
    JOIN payment_types USING (payment_type_id) 
    JOIN internet_service_types USING (internet_service_type_id)
    '''
    df = pd.read_sql(query, url)
    df = df.drop(['customer_id', 'contract_type_id', 'payment_type_id', 'internet_service_type_id'], axis=1)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(['Unnamed: 0'], axis=1)
    df.to_csv(filename)
    return df

def wrangle_telco():
    '''
    Function checks to see if telco_churn.csv already exists, if so it returns the dataframe,
    if not it creates the dataframe and returns it.
    '''
    filename = "telco.csv"
    if os.path.isfile(filename):
        print("Let me get that for you...")
        df = pd.read_csv(filename)
    else:
        df = get_telco_data()
        df.to_csv(filename)
    # replace blank values and special characters
    df = df.replace(r"^\s*$", np.nan, regex=True)
    # change total charges to float
    df['total_charges'] = df['total_charges'].astype(float)
    # fill missing values
    df['total_charges'] = df['total_charges'].fillna(df['total_charges'].mean())
    return df