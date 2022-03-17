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
            SELECT * 
            FROM properties_2017
            JOIN propertylandusetype USING (propertylandusetypeid)
            '''
    zillow17_data = pd.read_sql(query, url)
    zillow17_data.to_csv(filename)
    return zillow17_data

get_zillow17_data()
