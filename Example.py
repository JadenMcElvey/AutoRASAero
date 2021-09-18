import pathlib
import sys

from AutoRASAero import AutoRASAero

cwd = str(pathlib.Path.cwd())
CDX1_FILE = cwd + r"\Resources\MBS_43.CDX1"
ENG_FILE = cwd + r"\Resources\TCIMC3_(9899.7771)_5_5_2.329_11.0789_2.eng"
csvPath = cwd + "\\Temp\\"

finParams = [(16,7,4,10)]

finSim = AutoRASAero()
finSim.setPaths(CDX1_FILE, ENG_FILE, csvPath)
finSim.startupRASAero()
result = finSim.runSimulation(finParams[0], finParams[0], 6)

print(result)
