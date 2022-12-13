"""
Created on 08 December 2022

@author : Paul
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import csv

# Read csv
df = pd.read_csv("C:/Users/paulc/Desktop/Stage/lmt-analysis-2022/LMT/scripts/Dataframes/Merge.csv")
print(df.info())
# print(df.columns)

# To select the columns we want
# cols = []
# cols.append(df.columns)
# print(cols[0][1])

# columns = dict()
#
# for col in df:
#     columns[col] = list(df[col].unique())
#
# for key, value in columns.items():
#     print(key, value[0])

# temp_df = df[df["Date"] == 221013, "name"]
# print(temp_df)

# print(df["name"] == 'Move isolated')

temp_df = df[(df["Date"] == 221013) & (df["Cage"] == 'Cage1') & (df["name"] == 'Move isolated') & (df["Night-Phase"] == 1)]
print(temp_df)

final_df = temp_df[['numberOfEvents', 'RFidA', 'Bin']]
print(final_df)

# final_df2 = final_df[final_df['Bin'] == 1]
# print(final_df2)

fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(15, 12))
plt.subplots_adjust(hspace=0.5)
fig.suptitle("Number of 'Move isolated' per bin", fontsize=18, y=0.95)
axs = axs.ravel()

for i in final_df['Bin'].unique():
    plot = axs[i].scatter([str(el) for el in final_df['RFidA']], final_df['numberOfEvents'])
    axs[i].set_title(str(i))
    plt.xlabel("Mouse")
    plt.ylabel("Number of 'Move isolated'")
    plot.show()

# for line in final_df['Bin'].unique().tolist():
#     fig, ax = plt.subplots(nrows=3, ncols=4, figsize=(15, 12))
#     plt.subplots_adjust(hspace=0.5)
#     fig.suptitle("Number of 'Move isolated' per bin", fontsize=18, y=0.95)
#     plot = ax.scatter([str(el) for el in final_df2['RFidA']], final_df2['numberOfEvents'])
#     plt.title('Bin 1')
#     plt.xlabel("Mouse")
#     plt.ylabel("Number of 'Move isolated'")
# plt.show()

# #WORK !!
# fig, ax = plt.subplots()
# plot = ax.scatter([str(el) for el in final_df2['RFidA']], final_df2['numberOfEvents'])
# plt.title('Bin 1')
# plt.xlabel("Mouse")
# plt.ylabel("Number of 'Move isolated'")
# plt.show()

# type(final_df['Bin'].unique())
# print(final_df['Bin'].unique())

# for bin in bins:
#     fig, ax = plt.subplots()
#     plot = ax.scatter(final_df['numberOfEvents'], final_df['RFidA'])
#     plt.xlabel("Mouse")
#     plt.ylabel("Number of 'Move isolated'")
#     plt.show()


# dict = {el:0 for el in x}
# print(dict)
#
# for line in name.values:
#     print(line)
#     print(line[14])
#     dict[line[14]] += 1
#
# print(dict)


# fig, ax = plt.subplots()
# plot = ax.scatter([str(el) for el in dict.keys()], [int(el) for el in dict.values()])
# plt.xlabel("Mouse")
# plt.ylabel("Number of 'Move isolated'")
# plt.show()



