'''
Created on 13 sept. 2017

@author: Fab
'''

import sqlite3
from time import *
import datetime
from lmtanalysis.Util import *

from lmtanalysis.Animal import *
import matplotlib.pyplot as plt
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
import os
import sys
import traceback
from lmtanalysis.FileUtil import getFilesToProcess
from lmtanalysis.EventTimeLineCache import flushEventTimeLineCache, \
    disableEventTimeLineCache, EventTimeLineCached

global startNightInput
global endNightInput

''' minT and maxT to process the analysis (in frame) '''
minT = 0

# maxT = 5000
maxT = 11 * oneHour
# maxT = (6+1)*oneHour
''' time window to compute the events. '''
windowT = 1 * oneDay
# windowT = 3*oneDay #int (0.5*oneDay)


USE_CACHE_LOAD_DETECTION_CACHE = True


class FileProcessException(Exception):
    pass


eventClassList = [
                #BuildEventHuddling,
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
                #BuildEventWaterPoint,
                BuildEventApproachContact,
                #BuildEventWallJump,
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

    # update missing fields
    try:
        connection = sqlite3.connect(file)
        c = connection.cursor()
        query = "ALTER TABLE EVENT ADD METADATA TEXT";
        c.execute(query)
        connection.commit()

    except:
        print("METADATA field already exists", file)

    BuildDataBaseIndex.buildDataBaseIndex(connection, force=False)
    # build sensor data
    animalPool = AnimalPool()
    animalPool.loadAnimals(connection)
    # animalPool.buildSensorData(file)

    currentT = minT

    try:

        # flushNightEvents(connection)

        while currentT < maxT:

            currentMinT = currentT
            currentMaxT = currentT + windowT
            if (currentMaxT > maxT):
                currentMaxT = maxT

            chronoTimeWindowFile = Chronometer(
                "File " + file + " currentMinT: " + str(currentMinT) + " currentMaxT: " + str(currentMaxT));
            processTimeWindow(connection, file, currentMinT, currentMaxT)
            chronoTimeWindowFile.printTimeInS()

            currentT += windowT

        print("Full file process time: ")
        chronoFullFile.printTimeInS()

        TEST_WINDOWING_COMPUTATION = False

        if (TEST_WINDOWING_COMPUTATION):

            print("*************")
            print("************* TEST START SECTION")
            print("************* Test if results are the same with or without the windowing.")

            # display and record to a file all events found, checking with rolling idA from None to 4. Save nbEvent and total len

            eventTimeLineList = []

            eventList = getAllEvents(connection)
            file = open("outEvent" + str(windowT) + ".txt", "w")
            file.write("Event name\nnb event\ntotal duration")

            for eventName in eventList:
                for animal in range(0, 5):
                    idA = animal
                    if idA == 0:
                        idA = None
                    timeLine = EventTimeLineCached(connection, file, eventName, idA, minFrame=minT, maxFrame=maxT)
                    eventTimeLineList.append(timeLine)
                    file.write(timeLine.eventNameWithId + "\t" + str(len(timeLine.eventList)) + "\t" + str(
                        timeLine.getTotalLength()) + "\n")

            file.close()

            # plotMultipleTimeLine(eventTimeLineList)

            print("************* END TEST")

        flushEventTimeLineCache()

    except:

        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        error = ''.join('!! ' + line for line in lines)

        t = TaskLogger(connection)
        t.addLog(error)
        flushEventTimeLineCache()

        print(error, file=sys.stderr)

        raise FileProcessException()


def insertNightEventWithInputs(file):
    '''
    This function create night event
    '''

    print("Global variables:")
    print(startNightInput, endNightInput)

    connection = sqlite3.connect(file)

    print("--------------")
    print("Current file: ", file)

    print("--------------")
    print("Loading existing Night events...")
    nightTimeLine = EventTimeLine(connection, "night", None, None, None, None)

    print("\n")
    print("The Night Event list is:")
    print("--------------")
    for event in nightTimeLine.eventList:
        print(event)
    print("--------------")

    print("\n")
    print("Flushing the night events...")
    flushNightEvents(connection)

    nightTimeLineFlushed = EventTimeLine(connection, "night", None, None, None, None)

    print("The Night Event list, After Flushing:")
    print("--------------")
    for event in nightTimeLineFlushed.eventList:
        print(event)
    print("--------------")

    print("\n")
    try:
        startNight = datetime.time(int(startNightInput.split(":")[0]), int(startNightInput.split(":")[1]),
                                   int(startNightInput.split(":")[2]))
        print(startNight)
    except ValueError:
        raise ValueError("Incorrect time format, should be hh:mm:ss")

    try:
        endNight = datetime.time(int(endNightInput.split(":")[0]), int(endNightInput.split(":")[1]),
                                 int(endNightInput.split(":")[2]))
        print(endNight)
    except ValueError:
        raise ValueError("Incorrect time format, should be hh:mm:ss")

    """
    Two cases: 
    - end night hour < start night hour means end night hour is the day after
    - end night hour > start night hour means the night is during the day: reverse cycle
    """

    print("**** Test End/start times****")
    if (endNight < startNight):
        cycle = "normal"
        print("The cycle is ", cycle)
    else:
        cycle = "reverse"
        print("The cycle is ", cycle)

    print("\n")
    currentNight = Night(startHour=startNight, endHour=endNight, cycle=cycle)

    '''Beginning and end of the experiment'''
    startExperimentDate = getStartInDatetime(file)
    print(f"start Xp date: {startExperimentDate}")

    endExperimentDate = getEndInDatetime(file)
    print(f"End Xp date: {endExperimentDate}")

    currentDay = datetime.datetime.strftime(startExperimentDate, "%Y-%m-%d")
    currentDay = datetime.datetime(int(currentDay.split("-")[0]), int(currentDay.split("-")[1]),
                                   int(currentDay.split("-")[2]))
    previousDay = currentDay - datetime.timedelta(days=1)
    previousDay = datetime.datetime.strftime(previousDay, "%Y-%m-%d")

    print(f"currentDay : {currentDay}")
    print(f"previousDay : {previousDay}")

    currentStartNightDate = datetime.datetime.strptime("%s %s" % (previousDay, startNight), "%Y-%m-%d %H:%M:%S")
    print(f"currentStartNightDate : {currentStartNightDate}")

    lastFrame = getNumberOfFrames(file)

    currentNight.setStartEndDate(currentStartNightDate)

    while (True):
        if (currentNight.startDate > endExperimentDate):
            break

        tmpStartFrame = recoverFrame(file, str(currentNight.startDate))
        tmpEndFrame = recoverFrame(file, str(currentNight.endDate))

        if ((tmpStartFrame == 0) & (tmpEndFrame == 0)):
            if ((currentNight.startDate < startExperimentDate) & (currentNight.endDate > endExperimentDate)):
                tmpStartFrame = 1
                tmpEndFrame = lastFrame
                nightTimeLineFlushed.addEvent(Event(tmpStartFrame, tmpEndFrame))
                nightTimeLineFlushed.endRebuildEventTimeLine(connection, deleteExistingEvent=True)
                print("** nightTimeLineFlushed is now:")
                print(nightTimeLineFlushed)
            else:
                '''night outside the experiment'''
                pass
        else:
            if (tmpStartFrame == 0):
                tmpStartFrame = 1

            if (tmpEndFrame == 0):
                tmpEndFrame = lastFrame

            nightTimeLineFlushed.addEvent(Event(tmpStartFrame, tmpEndFrame))
            nightTimeLineFlushed.endRebuildEventTimeLine(connection, deleteExistingEvent=True)
            print("*** nightTimeLineFlushed is now:")
            print(nightTimeLineFlushed)

        '''next day'''
        print("\n")
        print("Going to the next day: ")
        currentNight.nextDay()


if __name__ == '__main__':
    print("Code launched.")

    files = getFilesToProcess()

    chronoFullBatch = Chronometer("Full batch")

    fileCount = 0  # File Counter

    if files != None:
        for file in files:
            if fileCount == 0:  # First file
                try:
                    fileCount += 1  # Increment file Counter
                    print("\n")
                    buildEvents = input("Do you what to rebuild the Events ?")
                    if buildEvents == "Yes" or buildEvents == 'Y' or buildEvents == "yes":
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
                        insertNightEventWithInputs(file)
                    else:
                        print("THE NIGHTS WILL NOT BE BUILD !!!!")

                    if buildEvents == "Yes" or buildEvents == 'Y' or buildEvents == "yes":
                        process(file)

                except FileProcessException:
                    print("STOP PROCESSING FILE " + file, file=sys.stderr)

            else:  # For other files than the first one
                try:
                    print("Processing file", file)
                    insertNightEventWithInputs(file)
                    process(file)
                except FileProcessException:
                    print("STOP PROCESSING FILE " + file, file=sys.stderr)

    chronoFullBatch.printTimeInS()

    print("*** ALL JOBS DONE ***")
