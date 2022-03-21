import pandas as pd
import os

from env import host, user, password
#-----------------------------------------------------------------------------------------------------------------------
# Make a function named get_titanic_data that returns the titanic data from the codeup data science database as a pandas data frame.

def get_titanic_data(use_cache=True):
    filename = "titanic.csv"
    if os.path.isfile(filename) and use_cache:
        print("Let me get that for you...")
        return pd.read_csv(filename)
    print("Sorry, nothing on file, let me create one for you...")
    data = 'titanic_db'
    url = f'mysql+pymysql://{user}:{password}@{host}/{data}'
    titanic_data = pd.read_sql('SELECT * FROM passengers', url)
    titanic_data.to_csv(filename)
    return titanic_data

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Make a function named get_iris_data that returns the data from the iris_db on the codeup data science database as a pandas dataframe.

def get_iris_data(use_cache=True):
    filename = "iris.csv"
    if os.path.isfile(filename) and use_cache:
        print("Let me get that for you...")
        return pd.read_csv(filename)
    print("Sorry, nothing on file, let me create one for you...")
    data = 'iris_db'
    url = f'mysql+pymysql://{user}:{password}@{host}/{data}'
    iris_data = pd.read_sql('SELECT * FROM measurements LEFT JOIN species USING(species_id)', url)
    iris_data.to_csv(filename)
    return iris_data

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Make a function named get_telco_data that returns the data from the telco_churn database in SQL. 
# In your SQL, be sure to join all 4 tables together, so that the resulting dataframe contains all the contract, payment, and internet service options.

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
    telco_data = pd.read_sql(query, url)
    # drop columns that are not needed
    telco_data = telco_data.drop(['customer_id', 'contract_type_id', 'payment_type_id', 'internet_service_type_id'], axis=1)
    if 'Unnamed: 0' in telco_data.columns:
        telco_data = telco_data.drop(['Unnamed: 0'], axis=1)
    telco_data.to_csv(filename)
    return telco_data

