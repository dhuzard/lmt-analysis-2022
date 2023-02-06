import pandas as pd
import os
import csv

os.chdir("C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/")
df=pd.read_csv("Merge.csv")

df['Injection'] = df['Injection'].replace(['weekend1'], 'weekend1 (1)')
df['Injection'] = df['Injection'].replace(['1-Nacl'], '3Nacl (2)')
df['Injection'] = df['Injection'].replace(['2-1Amphet'], '1Amphet-1 (3)')
df['Injection'] = df['Injection'].replace(['3-1Amphet'], '1Amphet-2 (4)')
df['Injection'] = df['Injection'].replace(['4-1Amphet'], '1Amphet-3 (5)')
df['Injection'] = df['Injection'].replace(['weekend2'], 'weekend2 (6)')
df['Injection'] = df['Injection'].replace(['6-3Amphet'], '3Amphet-1 (7)')
df['Injection'] = df['Injection'].replace(['7-3Amphet'], '3Amphet-2 (8)')
df['Injection'] = df['Injection'].replace(['8-3Amphet'], '3Amphet-3 (9)')


df.pop("Unnamed: 0") #Add this line if there is a column named "Unnamed: 0"
df.to_csv("C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/Merge_v2.csv")