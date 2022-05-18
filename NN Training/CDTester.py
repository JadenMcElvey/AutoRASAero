# Simulations will be run for all values in the spreadsheet from STARTING_ROW to ENDING_ROW inclusive
STARTING_ROW = 2
ENDING_ROW = 3

import pathlib
import sys
import csv
import os

sys.path.append(".")
sys.path.append("..")
from Automation.AutoRASAero import AutoRASAero
from Automation.mbsEditor import mbsEditor

# Get paths for rocket files and where to save the csv
CDX1_FILE = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\Resources\MBS_43_A.CDX1'))) # This needs to change for every new rocket
ENG_FILE = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\Resources\PmotorRasp2.eng')))
csvPath = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\\Temp\\"

csvFileName = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\NN Training\Mach Input D2 Hypercube 12000.jmp.csv')))
csvFile = pathlib.Path(csvFileName)

file = open(csvFileName)
reader = csv.reader(file)

# Get to the correct starting row
for row in range(STARTING_ROW - 1):
    next(reader)

# Create an object to run the simulations
finSim = AutoRASAero()
# Set the paths for the simulations
finSim.setPaths(CDX1_FILE, ENG_FILE, csvPath)

outputPath = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\NN Training\outputTest2.csv')))
outputFile = open(outputPath, "w", newline='')
writer = csv.writer(outputFile)
writer.writerow(["Row", "Tip B", "Root B", "Span B", "Sweep B", "Body Length B", "Body Diameter B+S", "Tip S", "Root S" ,"Span S" ,"Sweep S" ,"Body Length S", "Mach Number", "S Power Off", "S Power On", "B+S Power Off", "B+S Power On", "CP S", "CP B+S"])


# the new output paths for TESTING
# create outputPath2 that creates a new csv file called results.csv
outputPath2 = '.\\NN Training\\results.csv'
outputFile2 = open(outputPath2, "w", newline='')
writer2 = csv.writer(outputFile2)



for row in range(ENDING_ROW - STARTING_ROW + 1):
    data = next(reader)
    # print(data)

    # Choose the tube parameters to simulate
    # First tuple is the parameters for the booster
    tipB = data[0]
    rootB = data[1]
    spanB = data[2]
    sweepB = data[3]
    bodyLengthB = data[4]
    bodyDiameterBS = data[5]
    boosterParams = (rootB, spanB, tipB, sweepB, bodyLengthB)
    # Second tuple is the parameters for the sustainer
    tipS = data[6]
    rootS = data[7]
    spanS = data[8]
    sweepS = data[9]
    bodyLengthS = data[10]
    sustainerParams = (rootS, spanS, tipS, sweepS, bodyLengthS)
    # Tube parameters are in the form (root chord, span, tip chord, sweep, tube length)
    tubeParams = [boosterParams, sustainerParams]
    # Get the body diameter and mach value
    bodyDiameter = data[5]
    # mach = data[11] old mach number

    # CODE THAT CHANGE THE PATH FOR EACH NEW ROCKET, CALL MBSEDITOR HERE

    rocketDict = {
        'noseConeLength': 6.17*6,
        'noseConeDiameter': 6.17,
        'noseConeShape': 'Von Karman Ogive',
        'noseConeBluntRadius': 0,
        'noseConeColor': 'Black',
        'bodyTubeLength': float(bodyLengthB),
        'bodyTubeDiameter': float(bodyDiameterBS),
        'bodyTubeColor': 'Black',
        'bodyTubeLength2': float(bodyLengthS),
        'bodyTubeDiameter2': float(bodyDiameterBS),
        'bodyTubeColor2': 'Black',
        'finChord': 15,
        'finSpan': float(spanS),
        'finSweepDistance': float(sweepS),
        'finTipChord': float(tipS),
        'finThickness': 0.5,
        'finLocation': 17,
        'boosterLength': 80.5,
        'boosterDiameter': float(bodyDiameterBS),
        'boosterColor': 'Black',
        'finChord2': 15,
        'finSpan2': float(spanB),
        'finSweepDistance2': float(sweepB),
        'finTipChord2': float(tipB),
        'finThickness2': 0.5,
        'finLocation2': 17,
        'altitude': 2050,
        'rodLength': 24,
        'windSpeed': 1, # Don't know what to do here, was mach number but can't do that anymore
    }

    mbsEditor(rocketDict)

    CDX1_FILE = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\Resources\MBSTemplate2.CDX1')))
    finSim.setPaths(CDX1_FILE, ENG_FILE, csvPath)

    
    # Start RASAero
    finSim.startupRASAero()
    # run the simulation and print the output
    # result = finSim.runCDSimulations(bodyDiameter, tubeParams[0], tubeParams[1])
    result = finSim.runCDSimulations(tubeParams[0], tubeParams[1])
    # print(result[0])
    # add results[0] to the second csv file
    writer2.writerow(result[0])

    newCDValues = [row + STARTING_ROW]
    mach = 0.1
    while mach < 6:
        data[11] = round(mach, 2)
        for inputValue in data:
            newCDValues.append(inputValue)
        newCDValues = newCDValues[:-6]
        newCDValues.append(finSim.getCDforMachValue(result[0], mach))
        newCDValues.append(finSim.getCDforMachValue(result[1], mach))
        newCDValues.append(finSim.getCDforMachValue(result[2], mach))
        newCDValues.append(finSim.getCDforMachValue(result[3], mach))
        newCDValues.append(finSim.getCDforMachValue(result[4], mach))
        newCDValues.append(finSim.getCDforMachValue(result[5], mach))
        writer.writerow(newCDValues)
        newCDValues = [row + STARTING_ROW]
        mach += 0.1
    # del data <-- do this to delete the row
    # Close RASAero
    finSim.closeRASAero()
        
outputFile.close()

# add two more columns for CP sustainer + booster and CP sustainer * Complete
# remove clicker functions for useless functions * Complete
# replace the template file
# use 100 mach number (random data points between 0 and 6) for each row * Complete (more or less, fix the issues)

# Figure out why it only runs the first row

# data is in AeroPlots