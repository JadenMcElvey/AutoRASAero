import pathlib
import pandas as pd
from mbsEditor import mbsEditor

from Automation.AutoRASAero import AutoRASAero

# grab new rocket data from excel file
xl = pd.ExcelFile('MBSExample.xlsx')
df = xl.parse('Run')

for i in range(df.shape[0]):
    # call mbsEditor with rocket data
    mbsEditor(
        df.iloc[i, 0],
        df.iloc[i, 1],
        df.iloc[i, 2],
        df.iloc[i, 3],
        df.iloc[i, 4],
        df.iloc[i, 5],
        df.iloc[i, 6],
        df.iloc[i, 7],
        df.iloc[i, 8],
        df.iloc[i, 9],
        df.iloc[i, 10],
        df.iloc[i, 11],
        df.iloc[i, 12],
        df.iloc[i, 13],
        df.iloc[i, 14],
        df.iloc[i, 15],
        df.iloc[i, 16],
        df.iloc[i, 17],
        df.iloc[i, 18],
        df.iloc[i, 19],
        df.iloc[i, 20],
        df.iloc[i, 21],
        df.iloc[i, 22],
        df.iloc[i, 23],
        df.iloc[i, 24],
        df.iloc[i, 25],
        df.iloc[i, 26],
        df.iloc[i, 27],
        df.iloc[i, 28],
    )


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
finParams = [(16,7,4,10), (16,7,4,10)]
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
