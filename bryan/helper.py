import sqlite3
import pandas as pd

def run_sql(query, db_path, verbose=False):
    # Step 1: Connect to SQLite database
    conn = sqlite3.connect(db_path)
    
    df = pd.read_sql(query, conn)

    if verbose is True:
        print(df.head())  # Display the first 5 rows
        print(df.info())  # Display column data types and non-null counts
        print(df.describe())  # Summary statistics of numerical columns
    
    # Step 5: Close the connection
    conn.close()
    return df
