import sqlite3
from time import *
import datetime
import matplotlib.pyplot as plt
import os
import sys
import traceback

from lmtanalysis.Util import *
from lmtanalysis.Animal import *
from lmtanalysis.Event import *
from lmtanalysis.Measure import *
from lmtanalysis.Util import getAllEvents
from lmtanalysis.BuildEventNight import *
from lmtanalysis import BuildEventApproachContact, BuildEventOtherContact, BuildEventPassiveAnogenitalSniff, \
    BuildEventHuddling, BuildEventTrain3, BuildEventTrain4, BuildEventTrain2, BuildEventFollowZone, BuildEventRear5, \
    BuildEventCenterPeripheryLocation, BuildEventRearCenterPeriphery, BuildEventFloorSniffing, BuildEventSocialApproach, \
    BuildEventSocialEscape, BuildEventApproachContact, BuildEventOralOralContact, BuildEventApproachRear, \
    BuildEventGroup2, BuildEventGroup3, BuildEventGroup4, BuildEventOralGenitalContact, BuildEventStop, \
    BuildEventWaterPoint, BuildEventMove, BuildEventGroup3MakeBreak, BuildEventGroup4MakeBreak, BuildEventSideBySide, \
    BuildEventSideBySideOpposite, BuildEventDetection, BuildDataBaseIndex, BuildEventWallJump, BuildEventSAP, \
    BuildEventOralSideSequence, CheckWrongAnimal, CorrectDetectionIntegrity, BuildEventNest4, BuildEventNest3, \
    BuildEventGetAway
from psutil import virtual_memory
from tkinter.filedialog import askopenfilename
from lmtanalysis.TaskLogger import TaskLogger
from lmtanalysis.FileUtil import getFilesToProcess
from lmtanalysis.EventTimeLineCache import flushEventTimeLineCache, \
    disableEventTimeLineCache, EventTimeLineCached

global startNightInput
global endNightInput

''' minT and maxT to process the analysis (in frame) '''
minT = 0

# maxT = 5000
maxT = 72 * oneHour
# maxT = (6+1)*oneHour
''' time window to compute the events. '''
# windowT = 1 * oneHour
windowT = 1 * oneDay
# windowT = 3*oneDay #int (0.5*oneDay)

USE_CACHE_LOAD_DETECTION_CACHE = True

class FileProcessException(Exception):
    pass

eventClassList = [
                BuildEventHuddling,
                BuildEventDetection,
                BuildEventOralOralContact,
                BuildEventOralGenitalContact,
                BuildEventSideBySide,
                BuildEventSideBySideOpposite,
                BuildEventTrain2,
                BuildEventTrain3,
                BuildEventTrain4,
                BuildEventMove,
                BuildEventFollowZone,
                BuildEventRear5,
                BuildEventCenterPeripheryLocation,
                BuildEventRearCenterPeriphery,
                BuildEventSocialApproach,
                BuildEventGetAway,
                BuildEventSocialEscape,
                BuildEventApproachRear,
                BuildEventGroup2,
                BuildEventGroup3,
                BuildEventGroup4,
                BuildEventGroup3MakeBreak,
                BuildEventGroup4MakeBreak,
                BuildEventStop,
                BuildEventWaterPoint,
                BuildEventApproachContact,
                BuildEventWallJump,
                BuildEventSAP,
                BuildEventOralSideSequence,
                BuildEventNest3,
                BuildEventNest4
                   ]

# eventClassList = [BuildEventStop]

# eventClassList = [BuildEventPassiveAnogenitalSniff, BuildEventOtherContact, BuildEventExclusiveSideSideNoseAnogenitalContact]
# eventClassList = [BuildEventApproachContact2]

'''eventClassList = [

                BuildEventDetection,
                BuildEventMove,
                BuildEventRear5,
                BuildEventCenterPeripheryLocation,
                BuildEventRearCenterPeriphery,
                BuildEventStop,
                BuildEventWaterPoint,
                BuildEventWallJump,
                BuildEventSAP
                   ]'''

def flushNightEvents(connection):
    ''' flush 'NIGHT' event in database '''
    print("delete night in DBs ?")
    deleteEventTimeLineInBase(connection, "night")

def flushEvents( connection ):

    print("Flushing events...")

    for ev in eventClassList:

        chrono = Chronometer( "Flushing event " + str(ev) )
        ev.flush( connection );
        chrono.printTimeInS()

def processTimeWindow(connection, file, currentMinT, currentMaxT):
    CheckWrongAnimal.check(connection, tmin=currentMinT, tmax=currentMaxT)

    # Warning: enabling this process (CorrectDetectionIntegrity) will alter the database permanently
    # CorrectDetectionIntegrity.correct(connection, tmin=0, tmax=maxT)

    # BuildEventDetection.reBuildEvent(connection, file, tmin=currentMinT, tmax=currentMaxT)

    animalPool = None

    flushEventTimeLineCache()

    if (USE_CACHE_LOAD_DETECTION_CACHE):
        print("Caching load of animal detection...")
        animalPool = AnimalPool()
        animalPool.loadAnimals(connection)
        animalPool.loadDetection(start=currentMinT, end=currentMaxT)
        print("Caching load of animal detection done.")

    for ev in eventClassList:
        chrono = Chronometer(str(ev))
        ev.reBuildEvent(connection, file, tmin=currentMinT, tmax=currentMaxT, pool=animalPool)
        chrono.printTimeInS()

def process(file):
    print("\n***************************************************************************")
    print("Start Process of Events")
    print(file)

    mem = virtual_memory()
    availableMemoryGB = mem.total / 1000000000
    print("Total memory on computer: (GB)", availableMemoryGB)

    if availableMemoryGB < 10:
        print("Not enough memory to use cache load of events.")
        disableEventTimeLineCache()

    chronoFullFile = Chronometer("File " + file)

    connection = sqlite3.connect(file)
    flushEvents(connection)

if __name__ == '__main__':
    print("Code launched.")

    files = getFilesToProcess()

    chronoFullBatch = Chronometer("Full batch")

    fileCount = 0  # File Counter
    # if files is not None:
    if files != None:
        for file in files:
            if fileCount == 0:  # First file
                try:
                    fileCount += 1  # Increment file Counter
                    print("\n")
                    buildEvents = input("Do you want to rebuild the Events ?")
                    if buildEvents == "Yes" or buildEvents == "yes" or buildEvents == 'Y' or buildEvents == "y":
                        print("In addition to the night events, this script will also Rebuild the database for those "
                              "events:")

                        for i in eventClassList:
                            print(i.__name__)

                        confirmEvents = input("Do you confirm ? ")

                    else:
                        print("The Events WILL NOT BE BUILD !!!!")

                    night = input("Do you want to rebuild the night ? Yes (Y) or No (N) :")

                    if (night == "Y") or (night == "Yes"):  # User replied Yes to rebuild the Nights
                        startNightInput = input("Time of the beginning of the night (hh:mm:ss):")
                        endNightInput = input("Time of the end of the night (hh:mm:ss):")
                        print("Processing file, Rebuilding the  nights...", file)
                    else:
                        print("THE NIGHTS WILL NOT BE BUILD !!!!")

                    if buildEvents == "Yes" or buildEvents == 'Y' or buildEvents == "yes":
                        process(file)

                except FileProcessException:
                    print("STOP PROCESSING FILE " + file, file=sys.stderr)

            else:  # For other files than the first one
                try:
                    print("Processing file", file)
                    process(file)
                except FileProcessException:
                    print("STOP PROCESSING FILE " + file, file=sys.stderr)

    chronoFullBatch.printTimeInS()