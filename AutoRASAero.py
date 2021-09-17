import RASAeroInstance
import pathlib
import time
import csv

class AutoRASAero:
    instanceNum = 0
    cdx1_file = None
    eng_file = None
    csv_path = None
    RASAero = None

    def __init__(self):
        AutoRASAero.instanceNum += 1
        if AutoRASAero.instanceNum > 1:
            print("Warning! Creating multiple instances of AutoRASAero may cause problems!")

    def __del__(self):
        AutoRASAero.instanceNum -= 1

    def setPaths(self, cdx1Path, engPath, csvPath):
        AutoRASAero.cdx1_file = cdx1Path
        AutoRASAero.eng_file = engPath
        AutoRASAero.csv_path = csvPath

    def startupRASAero(self):
        AutoRASAero.RASAero = RASAeroInstance.RASAeroInstance()
        AutoRASAero.RASAero.start()
        AutoRASAero.RASAero.loadRocket(AutoRASAero.cdx1_file)
        AutoRASAero.RASAero.loadEngine(AutoRASAero.eng_file)

    def runSimulation(self, bFinParams, sFinParams, ignitionDelay):
        AutoRASAero.RASAero.setFinParameters(RASAeroInstance.RocketSection.Sustainer, sFinParams[0], sFinParams[1], sFinParams[2], sFinParams[3])
        AutoRASAero.RASAero.setFinParameters(RASAeroInstance.RocketSection.Booster, bFinParams[0], bFinParams[1], bFinParams[2], bFinParams[3])
        boosterStr = "B_" + "_".join([str(x) for x in bFinParams])
        sustainerStr = "S_" + "_".join([str(x) for x in sFinParams])
        csvFileName = AutoRASAero.csv_path + "Fin_" + boosterStr + sustainerStr + ".csv"
        AutoRASAero.RASAero.setIgnitionDelayAndExportFlightSimData(csvFileName, ignitionDelay)
        simResults = self.__parseCSV(csvFileName)
        print(simResults)

    def __parseCSV(self, csvFileName):
        boosterStartStability, sustainerStartStability = None, None
        boosterEndStability, sustainerMaxStability = 0, 0
        globalMaxStability = 0
        globalMinStability = float("inf")

        csvFile = pathlib.Path(csvFileName)
        while not csvFile.is_file():
            time.sleep(1)
            i += 1
        time.sleep(1)
        
        reader = csv.reader(open(csvFileName))
        next(reader)

        for row in reader:
            stage = row[1]
            stabilityMargin = float(row[13])

            if stage == "B":
                if boosterStartStability == None:
                    boosterStartStability = stabilityMargin
                else:
                    boosterEndStability = stabilityMargin
            elif stage == "S":
                if sustainerStartStability == None:
                    sustainerStartStability = stabilityMargin
                else:
                    sustainerMaxStability = stabilityMargin if stabilityMargin > sustainerMaxStability else sustainerMaxStability

            globalMaxStability = stabilityMargin if stabilityMargin > globalMaxStability else globalMaxStability
            globalMinStability = stabilityMargin if (stabilityMargin != 0) and (stabilityMargin < globalMinStability) else globalMinStability

        #finParamStr = "Root chord:" + str(finParams[0][0]) + " Span:" + str(finParams[0][1]) + " Tip Chord:" + str(finParams[0][2]) + " Sweep Distance:" + str(finParams[0][3])
        finStabilityStr = "\nB(0):" + str(boosterStartStability) + " B(end):" + str(boosterEndStability)
        finStabilityStr += "\nS(0):" + str(sustainerStartStability) + " S(max):" + str(sustainerMaxStability)
        finStabilityStr += "\nGlobal Min:" + str(globalMinStability) + " Global Max:" + str(globalMinStability)
        print(finStabilityStr)
        return (boosterStartStability, boosterEndStability, sustainerStartStability, sustainerMaxStability, globalMinStability, globalMaxStability)
