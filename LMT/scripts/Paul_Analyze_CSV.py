"""
Created on 08 December 2022

@author : Paul
"""

import warnings
warnings.simplefilter(action='ignore')

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

#Select specific rows of specific columns
temp_df = df[(df["Date"] == 221013) & (df["Cage"] == 'Cage1') & (df["name"] == 'Move isolated') & (df["Night-Phase"] == 2)]
print(temp_df)

#Reduction of dataframe
# final_df = temp_df[['numberOfEvents', 'RFidA', 'Bin', 'GenoA', 'totalLength']]
final_df = temp_df[['numberOfEvents', 'RFidA', 'Bin', 'GenoA']]
print("final_df")
print(final_df)

bins = final_df['Bin'].unique()
print(bins)
animals = final_df['RFidA'].unique()
print("animals")
print(animals)
nbrAnimals = len(animals)
nbrEvents = {}

# #plot 'move isolated' event
for i in animals:
    x=final_df[final_df["RFidA"] == i]['Bin']
    y=final_df[final_df["RFidA"] == i]["numberOfEvents"]
    plt.plot(x,y, label = final_df[final_df["RFidA"] == i]['GenoA'].unique()[0])
    # final_df[final_df["RFidA"] == i].plot(x='Bin', y='numberOfEvents', kind = 'line')
    # nbrEvents[i] = final_df[(final_df["RFidA"] == i)]['numberOfEvents']
plt.title('Numbers of "Move isolated" per bin of each mouse')
plt.xlabel('Time bins')
plt.ylabel('Numbers of "Move isolated"')
plt.legend(loc = "upper left")
plt.show()
# # print("nbr events")
# # # print(nbrEvents)

# #plot 'contact' event
# for i in animals:
#     x=final_df[final_df["RFidA"] == i]['Bin']
#     y=final_df[final_df["RFidA"] == i]["numberOfEvents"]
#     plt.plot(x,y, label = final_df[final_df["RFidA"] == i]['GenoA'].unique()[0])
#     # final_df[final_df["RFidA"] == i].plot(x='Bin', y='numberOfEvents', kind = 'line')
#     # nbrEvents[i] = final_df[(final_df["RFidA"] == i)]['numberOfEvents']
# plt.title('Numbers of "Contact" per bin of each mouse')
# plt.xlabel('Time bins')
# plt.ylabel('Numbers of "Contact"')
# plt.legend(loc = "upper left")
# plt.show()
# # print("nbr events")
# # print(nbrEvents)

# test_crosstab = pd.crosstab(index=final_df['Bin'], columns=animals, values=final_df['numberOfEvents'], aggfunc=sum)
# print(test_crosstab)
#
# sns.lineplot(test_crosstab)
# plt.show()

# sns.set()  # use Seaborn styles
# crosstable = final_df.pivot_table(index='Bin', columns='RFidA', aggfunc='sum')
# sns.lineplot(crosstable)
#
# plt.show()
#
# # #WORKS
# pivot_table = final_df.pivot_table(index=['Bin'], columns=['RFidA'], values=['numberOfEvents'], aggfunc=np.sum)
# sns.lineplot(y=final_df['numberOfEvents'], x=final_df['Bin'], style=final_df['RFidA'], hue='GenoA', data= final_df)
# print(pivot_table)
# #sns.lineplot(pivot_table, hue="RFidA")
#
# plt.show()

# test = final_df.groupby(['RFidA', 'Bin'])['numberOfEvents'].sum()
# print(final_df.groupby(['RFidA', 'Bin'])['numberOfEvents'].sum())
#
# final_df.groupby(['RFidA', 'Bin'])['numberOfEvents'].sum().plot()
# plt.show()

# fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(15, 12))
# plt.subplots_adjust(hspace=0.5)
# fig.suptitle("Number of 'Move isolated' per bin", fontsize=18, y=0.95)
# axs = axs.ravel()
#
# for i in final_df['Bin'].unique():
#     plot = axs[i].scatter([str(el) for el in final_df['RFidA']], final_df['numberOfEvents'])
#     axs[i].set_title(str(i))
#     plt.xlabel("Mouse")
#     plt.ylabel("Number of 'Move isolated'")
#     plt.show()

# final_df2 = final_df[final_df['Bin'] == 1]
# print(final_df2)
#
# #WORK !!
# fig, ax = plt.subplots()
# plot = ax.scatter([str(el) for el in final_df2['RFidA']], final_df2['numberOfEvents'])
# plt.title('Bin 1')
# plt.xlabel("Mouse")
# plt.ylabel("Number of 'Move isolated'")
# plt.show()

# type(final_df['Bin'].unique())
# print(final_df['Bin'].unique())




