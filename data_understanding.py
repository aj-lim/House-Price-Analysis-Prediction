"""import required libraries and packages"""
import pandas as pd

"""upload the data"""
df = pd.read_csv(r"C:\Users\lucyl\Desktop\Alex AI Weiterbilgung\Programming with Python\house data.csv", index_col=False)

"""view the first 5 lines of data to ensure correct upload"""
print(df.head())

"""check dimensions of dataset"""
print(f"the dataset has {df.shape[0]} rows and {df.shape[1]} columns")

"""check for any null values"""
print(df.isnull().values.any())

"""check how many unique values per column"""
for col in df.columns:
    try:
        unique_count = df[col].nunique(dropna=True)  # dropna=True ignores NaN in count
        print(f"The column '{col}' has {unique_count} unique values")
    except Exception as e:
        print(f"Error processing column '{col}': {e}")

"""drop country and date column"""
df = df.drop('country', axis=1)
df = df.drop('date', axis=1)

"""split statezip into state and zip columns and drop statezip column"""
df[['state', 'zip']] = df['statezip'].str.extract(r'^([A-Z]{2})\s+(.+)$')
df = df.drop('statezip', axis=1)

"""check unique values in state and zip columns"""
print(f"the state column has {df['state'].nunique()} unique values")
print(f"the zip column has {df['zip'].nunique()} unique values")

"""drop state column"""
df = df.drop('state', axis=1)

"""print unique values from view, condition and waterfront columns"""
columns_to_check = ['view', 'condition', 'waterfront']
for col in columns_to_check:
    unique_vals = df[col].dropna().unique().tolist()
    print(f"Unique values in column '{col}': {list(unique_vals)}")

print(df.head())

data_clean = df
