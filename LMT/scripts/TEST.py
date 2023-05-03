import sqlite3
import warnings
warnings.simplefilter(action='ignore')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import os

from lmtanalysis.Animal import AnimalPool
from lmtanalysis.Event import EventTimeLine, plotMultipleTimeLine
from lmtanalysis.FileUtil import getFilesToProcess
from lmtanalysis.Measure import *

if __name__ == '__main__':
    files = getFilesToProcess()
    if len(files) == 0:
        print("NO FILE TO PROCESS !!!!!")
    if len(files) >= 1:
        filenames = [os.path.basename(files[x]) for x in range(0, len(files))]
        # print(f"{files} => {filenames}")
    count = 0
    for file in files:
        print(f"The current Count is : {count}")
        print(f"file: {file}")
        print(f"File path: {file.title()}")
        fileName = filenames[count]
        print(f"File name: {fileName}")

        if len(files) >= 1:
            filenames = [os.path.basename(files[x]) for x in range(0, len(files))]
            # print(f"{files} => {filenames}")

            ### DEFINE CONSTANTS ###
            start = {}
            stop = {}

            timeBinsDuration = int(
                input("Enter the TIMEBIN for ALL the files (1min =  1800 frames / 1h = 108000 frames): "))

            fileGlobal = input("Enter the filename for the .csv WITH ALL DATA INSIDE: ")

            useNights = input(
                "Do you want to use the Nights from the .sqlite files to computes the data ? ('Yes'/'No'): ")

        #Check that 'filename' and the current file are the same
        #TODO CAN BE IMPROVED by extracting from the current file

        if fileName in file:
            print("THE FILE NAME MATCHES! !")
        else:
            print("!!! ERROR: FILE NAME DO NOT MATCH!!")

        connection = sqlite3.connect(file) # connect to database
        animalPool = AnimalPool() # create an animalPool, which basically contains your animals
        animalPool.loadAnimals(connection) # load infos about the animals

        animalNumber = animalPool.getNbAnimals()
        print(f"There are {animalNumber} animals,")

        if useNights.lower() == "yes" or useNights.lower() == "y":
            # Le problème vient d'ici (fonction getNightStartStop) ? Est-ce que ça ne prendrait pas juste la première
            # nuit ? Faire une boucle if qui dit que si night_phase > 1 alors on prendra, à chaque night_count,
            # les données des frames suivantes comme getNightStartStop ne prend que le startframe et le endframe de
            # l'évènement night ?
            NightFrames = animalPool.getNightStartStop()
            print("The night events are:")
            print(NightFrames)