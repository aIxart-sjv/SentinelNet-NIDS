import pandas as pd
import numpy as np

def clean_data(df):
    df.columns = df.columns.str.strip()
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    return df

def create_target(df):
    df['Label'] = df['Label'].str.strip()
    df['target'] = df['Label'].apply(lambda x: 0 if x == 'Benign' else 1)
    X = df.drop(columns=['Label', 'target'])
    y = df['target']
    return X, y
