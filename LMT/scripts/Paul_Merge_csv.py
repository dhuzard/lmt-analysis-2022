import pandas as pd
import warnings
warnings.simplefilter(action='ignore')
import os
import glob
import csv

#read the csv file
df = pd.read_csv("C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/221018_Amphet_Cage1_2"
                 "-1Amphet.sqlite.csv")
#read the path
file_path = "C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/"
os.chdir("C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/")
#list all the files from the directory
file_list = os.listdir(file_path)

#list all csv files only
csv_files = glob.glob('*.{}'.format('csv'))
print(csv_files)

df_append = pd.DataFrame()  # append all files together

for file in csv_files:
    df_temp = pd.read_csv(file)
    df_append = df_append.append(df_temp, ignore_index=True)

print(df_append)

df_append.pop("Unnamed: 0") #Add this line if there is a column named "Unnamed: 0"
df_append.to_csv("C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/Merge.csv")
