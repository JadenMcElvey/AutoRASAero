import pathlib
import pandas as pd
from Automation.mbsEditor import mbsEditor

from Automation.AutoRASAero import AutoRASAero

# grab new rocket data from excel file
xl = pd.ExcelFile('MBSExample.xlsx')
df = xl.parse('Run')


for i in range(df.shape[0]):
    rocketDict = {
        'noseConeLength': df['noseConeLength'][i],
        'noseConeDiameter': df['noseConeDiameter'][i],
        'noseConeShape': df['noseConeShape'][i],
        'noseConeBluntRadius': df['noseConeBluntRadius'][i],
        'noseConeColor': df['noseConeColor'][i],
        'bodyTubeLength': df['bodyTubeLength'][i],
        'bodyTubeDiameter': df['bodyTubeDiameter'][i],
        'bodyTubeColor': df['bodyTubeColor'][i],
        'bodyTubeLength2': df['bodyTubeLength2'][i],
        'bodyTubeDiameter2': df['bodyTubeDiameter2'][i],
        'bodyTubeColor2': df['bodyTubeColor2'][i],
        'finChord': df['finChord'][i],
        'finSpan': df['finSpan'][i],
        'finSweepDistance': df['finSweepDistance'][i],
        'finTipChord': df['finTipChord'][i],
        'finThickness': df['finThickness'][i],
        'finLocation': df['finLocation'][i],
        'boosterLength': df['boosterLength'][i],
        'boosterDiameter': df['boosterDiameter'][i],
        'boosterColor': df['boosterColor'][i],
        'finChord2': df['finChord2'][i],
        'finSpan2': df['finSpan2'][i],
        'finSweepDistance2': df['finSweepDistance2'][i],
        'finTipChord2': df['finTipChord2'][i],
        'finThickness2': df['finThickness2'][i],
        'finLocation2': df['finLocation2'][i],
        'altitude': df['altitude'][i],
        'rodLength': df['rodLength'][i],
        'windSpeed': df['windSpeed'][i]
    }

    mbsEditor(rocketDict)

# Get paths for rocket files and where to save the csv
cwd = str(pathlib.Path.cwd())
# CDX1_FILE = cwd + r"\Resources\MBS_43_A.CDX1"
CDX1_FILE = cwd + r"\Resources\MBSTemplate2.CDX1"
ENG_FILE = cwd + r"\Resources\PmotorRasp2.eng"
csvPath = cwd + "\\Temp\\"

# Choose the fin parameters to simulate
# First tuple is the parameters for the booster
# Second tuple is the parameters for the sustainer
# Fin parameters are in formar (root chord, span, tip chord, sweep)
finParams = [(17, 7.2, 12, 10), (17, 7.2, 12, 10)]
# Create an object to run the simulations
finSim = AutoRASAero()
# Set the paths for the simulations
finSim.setPaths(CDX1_FILE, ENG_FILE, csvPath)
# Start RASAero
finSim.startupRASAero()
# run the simulation and print the output
result = finSim.runStabilitySimulation(finParams[0], finParams[1], 6)
print(result)
# Close RASAero
finSim.closeRASAero()
