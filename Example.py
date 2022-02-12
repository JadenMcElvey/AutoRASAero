import pathlib
import pandas as pd
from openpyxl import load_workbook
from mbsEditor import mbsEditor

from Automation.AutoRASAero import AutoRASAero

# grab new rocket data from excel file
xl = pd.ExcelFile('MBSExample.xlsx')
df = xl.parse('Run')

for i in range(df.shape[0]):
    # call mbsEditor with rocket data
    mbsEditor(
        df.loc[i, 0],
        df.loc[i, 1],
        df.loc[i, 2],
        df.loc[i, 3],
        df.loc[i, 4],
        df.loc[i, 5],
        df.loc[i, 6],
        df.loc[i, 7],
        df.loc[i, 8],
        df.loc[i, 9],
        df.loc[i, 10],
        df.loc[i, 11],
        df.loc[i, 12],
        df.loc[i, 13],
        df.loc[i, 14],
        df.loc[i, 15],
        df.loc[i, 16],
        df.loc[i, 17],
        df.loc[i, 18],
        df.loc[i, 19],
        df.loc[i, 20],
        df.loc[i, 21],
        df.loc[i, 22],
        df.loc[i, 23],
        df.loc[i, 24],
        df.loc[i, 25],
        df.loc[i, 26],
        df.loc[i, 27],
        df.loc[i, 28],
    )

# Get paths for rocket files and where to save the csv
cwd = str(pathlib.Path.cwd())
# CDX1_FILE = cwd + r"\Resources\MBS_43_A.CDX1"
CDX1_FILE = cwd + r"\Resources\MBSTemplate2.txt"
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
