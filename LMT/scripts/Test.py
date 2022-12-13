"""
Created on 08 December 2022

@author : Paul
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import csv

# Read csv
df = pd.read_csv("C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/Merge.csv")
print(df.columns)

columns = dict()

for col in df:
    columns[col] = list(df[col].unique())

for key, value in columns.items():
    print(key, value[0])

type(columns.iloc[0])
print(columns.iloc[0])

print(df.iloc(0))