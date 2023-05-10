if __name__ == '__main__':
    files = getFilesToProcess()
    if len(files) == 0:
        print("NO FILE TO PROCESS !!!!!")
    if len(files) >= 1:
        filenames = [os.path.basename(files[x]) for x in range(0, len(files))]

        start = {}
        stop = {}

        timeBinsDuration = int(input("Enter the TIMEBIN for ALL the files (1min =  1800 frames / 1h = 108000 frames): "))

        useNights = input("Do you want to use the Nights from the .sqlite files to computes the data ? ('Yes'/'No'): ")

    dfGlobal = pd.DataFrame()

    count = 0
    for file in files:
        fileName = filenames[count]

        if fileName in file:
            print("THE FILE NAME MATCHES! !")
        else:
            print("!!! ERROR: FILE NAME DO NOT MATCH!!")

        connection = sqlite3.connect(file)
        animalPool = AnimalPool()
        animalPool.loadAnimals(connection)

        animalNumber = animalPool.getNbAnimals()

        if useNights.lower() == "yes" or useNights.lower() == "y":
            NightFrames = animalPool.getNightStartStop()

            nbTimebin = []

            startFrame = NightFrames[0][0]
            stopFrame = NightFrames[0][1]

            nbTimebin.append(int((stopFrame - startFrame) / timeBinsDuration)+1)

            nbTimebins = int((stopFrame - startFrame) / timeBinsDuration)+1

            for filename in filenames:
                start[filename] = startFrame
                stop[filename] = stopFrame

        if useNights.lower() == "no" or useNights.lower() == "no":
            print("AAAAaaaahhh")

        if animalNumber >= 1:
            behavioralEventsForOneAnimal = ["Move", "Move isolated", "Rearing", "Rear isolated",
                                            "Stop isolated", "WallJump", "SAP", "Huddling", "WaterPoint"]
            print("The behaviors extracted are:\n", behavioralEventsForOneAnimal)
        if animalNumber >= 2:
            behavioralEventsForTwoAnimals = ["Contact", "Oral-oral Contact", "Oral-genital Contact", "Side by side Contact",
                                             "Side by side Contact, opposite way", "Social approach", "Social escape",
                                             "Approach contact", "Approach rear", "Break contact", "Get away", "FollowZone Isolated",
                                             "Train2", "Group2", "Move in contact", "Rear in contact"]
        if animalNumber >= 3:
            behavioralEventsForThreeAnimals = ["Group3", "Group 3 break", "Group 3 make"]
        if animalNumber >= 4:
            behavioralEventsForFourAnimals = ["Group4", "Group 4 break", "Group 4 make", "Nest3", "Nest4"]

        dicoOfBehInfos = {
            "Filename": None,
            "Date": None,
            "Cage": None,
            "Injection": None,
            "Night-Phase": None,
            "Bin": None,
            "start_frame": None,
            "stop_frame": None,
            "name": None,
            "idA": None,
            "idB": None,
            "idC": None,
            "idD": None,
            "RFidA": None,
            "RFidB": None,
            "RFidC": None,
            "RFidD": None,
            "GenoA": None,
            "GenoB": None,
            "GenoC": None,
            "GenoD": None,
            "totalLength": None,
            "meanLength": None,
            "medianLength": None,
            "numberOfEvents": None,
            "stdLength": None,
            "CI95_low": None,
            "CI95_up": None
        }

        dfOfBehInfos = pd.DataFrame()

        allBehaviorsInfo = {}

        night_count = 1
        print(NightFrames)
        for night in NightFrames:
            print("The night is ", night)
            print("The night_ count is ", night_count)
            bin = 1
            for z in range(night[0], night[1], timeBinsDuration):
                print("Z is ", z)
                startBin = (start[fileName] + (bin-1) * timeBinsDuration) + (night_count-1) * (108000*24)
                stopBin = startBin + timeBinsDuration
                print(bin)

                animalPool.loadDetection(start=startBin, end=stopBin)

                dicoOfBehInfos["start_frame"] = startBin
                dicoOfBehInfos["stop_frame"] = stopBin
                dicoOfBehInfos["Bin"] = bin
                dicoOfBehInfos["Night-Phase"] = night_count

                dicoOfBehInfos["Filename"] = fileName[:-7]
                date, Xp, cage, Injection = fileName[:-7].split("_")
                dicoOfBehInfos["Date"] = date
                dicoOfBehInfos["Cage"] = cage
                dicoOfBehInfos["Injection"] = Injection

                for animal in animalPool.getAnimalList():
                    print("**")
                    print(f"Animal RFID: {animal.RFID} / Animal Id: {animal.baseId} / Animal name: {animal.name}")
                    print(f"Animal genotype: {animal.genotype}")

                if animalNumber >= 1:
                    for behavior in behavioralEventsForOneAnimal:
                        print("**** ", behavior, " ****")

                        for a in animalPool.getAnimalDictionnary():
                            eventTimeLine = EventTimeLine(connection, behavior, idA=a, minFrame=startBin, maxFrame=stopBin)

                            behavioralDataOne = computeBehaviorsData(eventTimeLine)
                            dicoOfBehInfos.update(behavioralDataOne)
                            dicoOfBehInfos.update({"RFidA": animalPool.getAnimalWithId(a).RFID,
                                                   "GenoA": animalPool.getAnimalWithId(a).genotype})

                            index = [0]
                            dfOfBehInfosTemp = pd.DataFrame(dicoOfBehInfos, index=index)
                            dfOfBehInfos = dfOfBehInfos.append(dfOfBehInfosTemp, ignore_index=True)

                if animalNumber >= 2:
                    for behavior in behavioralEventsForTwoAnimals:
                        print("**** ", behavior, " ****")
                        behavioralList2 = []

                        for a in animalPool.getAnimalDictionnary():
                            if behavior == "Move in contact" or behavior == "Rear in contact":  # Just idA in those behaviors
                                eventTimeLine = EventTimeLine(connection, behavior, idA=a, minFrame=startBin, maxFrame=stopBin)
                                continue
                            for b in animalPool.getAnimalDictionnary():
                                if a == b:
                                    continue
                                eventTimeLine = EventTimeLine(connection, behavior, idA=a, idB=b,
                                                              minFrame=startBin, maxFrame=stopBin)

                                behavioralDataTwo = computeBehaviorsData(eventTimeLine)
                                dicoOfBehInfos.update(behavioralDataTwo)
                                dicoOfBehInfos.update({"RFidA": animalPool.getAnimalWithId(a).RFID,
                                                       "RFidB": animalPool.getAnimalWithId(b).RFID,
                                                       "GenoA": animalPool.getAnimalWithId(a).genotype,
                                                       "GenoB": animalPool.getAnimalWithId(b).genotype})

                                index = [0]
                                dfOfBehInfosTemp = pd.DataFrame(dicoOfBehInfos, index=index)
                                dfOfBehInfos = dfOfBehInfos.append(dfOfBehInfosTemp, ignore_index=True)

                if animalNumber >= 3:
                    for behavior in behavioralEventsForThreeAnimals:
                        print("**** ", behavior, " ****")

                        for a in animalPool.getAnimalDictionnary():
                            if behavior == "Group 3 make" or behavior == "Group 3 break":
                                eventTimeLine = EventTimeLine(connection, behavior, idA=a, minFrame=startBin, maxFrame=stopBin)
                                continue
                            for b in animalPool.getAnimalDictionnary():
                                if a == b:
                                    continue
                                for c in animalPool.getAnimalDictionnary():
                                    if a == c or b == c:
                                        continue
                                    eventTimeLine = EventTimeLine(connection, behavior, idA=a, idB=b, idC=c,
                                                                  minFrame=startBin, maxFrame=stopBin)

                                    behavioralDataThree = computeBehaviorsData(eventTimeLine)
                                    dicoOfBehInfos.update(behavioralDataThree)
                                    dicoOfBehInfos.update({"RFidA": animalPool.getAnimalWithId(a).RFID,
                                                           "RFidB": animalPool.getAnimalWithId(b).RFID,
                                                           "RFidC": animalPool.getAnimalWithId(c).RFID,
                                                           "GenoA": animalPool.getAnimalWithId(a).genotype,
                                                           "GenoB": animalPool.getAnimalWithId(b).genotype,
                                                           "GenoC": animalPool.getAnimalWithId(c).genotype})

                                    index = [0]
                                    dfOfBehInfosTemp = pd.DataFrame(dicoOfBehInfos, index=index)
                                    dfOfBehInfos = dfOfBehInfos.append(dfOfBehInfosTemp, ignore_index=True)

                if animalNumber >= 4:
                    for behavior in behavioralEventsForFourAnimals:
                        print("**** ", behavior, " ****")

                        for a in animalPool.getAnimalDictionnary():
                            if behavior == "Group 4 make" or behavior == "Group 4 break":
                                eventTimeLine = EventTimeLine(connection, behavior, idA=a,
                                                              minFrame=startBin, maxFrame=stopBin)
                                continue
                            for b in animalPool.getAnimalDictionnary():
                                if a == b:
                                    continue
                                for c in animalPool.getAnimalDictionnary():
                                    if a == c or b == c:
                                        continue
                                    if behavior == "Nest3":
                                        eventTimeLine = EventTimeLine(connection, behavior, idA=a, idB=b, idC=c,
                                                                      minFrame=startBin, maxFrame=stopBin)
                                        continue
                                    for d in animalPool.getAnimalDictionnary():
                                        if a == d or b == d or c == d:
                                            continue
                                        eventTimeLine = EventTimeLine(connection, behavior, idA=a, idB=b, idC=c, idD=d,
                                                                      minFrame=startBin, maxFrame=stopBin)

                                        behavioralDataFour = computeBehaviorsData(eventTimeLine)
                                        dicoOfBehInfos.update(behavioralDataFour)
                                        dicoOfBehInfos.update({"RFidA": animalPool.getAnimalWithId(a).RFID,
                                                               "RFidB": animalPool.getAnimalWithId(b).RFID,
                                                               "RFidC": animalPool.getAnimalWithId(c).RFID,
                                                               "RFidD": animalPool.getAnimalWithId(d).RFID,
                                                               "GenoA": animalPool.getAnimalWithId(a).genotype,
                                                               "GenoB": animalPool.getAnimalWithId(b).genotype,
                                                               "GenoC": animalPool.getAnimalWithId(c).genotype,
                                                               "GenoD": animalPool.getAnimalWithId(d).genotype})

                                        index = [0]
                                        dfOfBehInfosTemp = pd.DataFrame(dicoOfBehInfos, index=index)
                                        dfOfBehInfos = dfOfBehInfos.append(dfOfBehInfosTemp, ignore_index=True)

                bin += 1
            night_count += 1
        count += 1

        dfGlobal = dfGlobal.append(dfOfBehInfos)

        dfOfBehInfos.to_csv(f"{fileName}.csv")
        connection.close()