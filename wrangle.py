import pandas as pd
import os

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


# function to remove outliers
def remove_outliers(df, k, col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1  # Interquartile range
    fence_low = q1 - k * iqr
    fence_high = q3 + k * iqr
    df = df.loc[(df[col] > fence_low) & (df[col] < fence_high)]
    return df

    