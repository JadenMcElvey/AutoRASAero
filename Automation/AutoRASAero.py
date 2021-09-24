import Automation.RASAeroInstance as RASAeroInstance
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
        """
        Specify the paths to find the rocket, find the engine files, and save the csv output 
        
            Parameters:
                cdx1Path (string) : the path to the rocket file
                engPath (string) : the path to the engine file
                csvPath (string) : the directory to save the csvPath in
        """
        AutoRASAero.cdx1_file = cdx1Path
        AutoRASAero.eng_file = engPath
        AutoRASAero.csv_path = csvPath

    def startupRASAero(self):
        """
        Create a RASAeroInstance to automatically run simulation
        
            Parameters:
                
            Returns:
        """
        AutoRASAero.RASAero = RASAeroInstance.RASAeroInstance()
        AutoRASAero.RASAero.start()
        AutoRASAero.RASAero.loadRocket(AutoRASAero.cdx1_file)
        AutoRASAero.RASAero.loadEngine(AutoRASAero.eng_file)

    def closeRASAero(self):
        """
        Close a RASAeroInstance created with the startupRASAero() function
        
            Parameters:
                
            Returns:
        """
        AutoRASAero.RASAero.close()

    def runSimulation(self, bFinParams, sFinParams, ignitionDelay):
        """
        Run a simulation with the specified parameters and output the simulation results in the 
        previously specified csvPath
        
            Parameters:
                bFinParams [] : A list of floats representing the parameters for the fins on the 
                    booster in the following form [root chord, span, tip chord, sweep]
                sFinParams [] : A list of floats representing the parameters for the fins on the
                    sustainer in the following form [root chord, span, tip chord, sweep]
                ignitionDelay (float) : A float representing the ignition delay
                
            Returns:
                A tuple containing the flight sim results of the form (booster start stability, 
                booster end stability, sustainer start stability, sustainer max stability, 
                global min stability, global max stability, apogee) or None if the flight simulation
                fails 
        """
        AutoRASAero.RASAero.setFinParameters(RASAeroInstance.RocketSection.Sustainer, sFinParams[0], sFinParams[1], sFinParams[2], sFinParams[3])
        AutoRASAero.RASAero.setFinParameters(RASAeroInstance.RocketSection.Booster, bFinParams[0], bFinParams[1], bFinParams[2], bFinParams[3])
        boosterStr = "B_" + "_".join([str(x) for x in bFinParams])
        sustainerStr = "_S_" + "_".join([str(x) for x in sFinParams])
        csvFileName = AutoRASAero.csv_path + "Fin_" + boosterStr + sustainerStr + ".csv"
        if AutoRASAero.RASAero.setIgnitionDelayAndExportFlightSimData(csvFileName, ignitionDelay):
            return self.__parseCSV(csvFileName)
        else:
            return None

    def __parseCSV(self, csvFileName):
        boosterStartStability, sustainerStartStability = None, None
        boosterEndStability, sustainerMaxStability = 0, 0
        globalMaxStability = 0
        globalMinStability = float("inf")
        apogee = 0

        csvFile = pathlib.Path(csvFileName)
        while not csvFile.is_file():
            time.sleep(1)
        time.sleep(3)

        file = open(csvFileName)
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            try:
                stage = row[1]
                stabilityMargin = float(row[13])
                altitude = float(row[22])
            except IndexError:
                continue

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
            apogee = altitude if apogee < altitude else apogee

        file.close()
        return (boosterStartStability, boosterEndStability, sustainerStartStability, sustainerMaxStability, globalMinStability, globalMaxStability, apogee)
