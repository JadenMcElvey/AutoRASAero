import pathlib
import sys

sys.path.append(".")
from Automation.AutoRASAero import AutoRASAero

# Get paths for rocket files and where to save the csv
cwd = str(pathlib.Path.cwd())
CDX1_FILE = cwd + r"\Resources\MBS_43.CDX1"
ENG_FILE = cwd + r"\Resources\TCIMC3_(9899.7771)_5_5_2.329_11.0789_2.eng"
csvPath = cwd + "\\Temp\\"

# Choose the tube parameters to simulate
# First tuple is the parameters for the booster
# Second tuple is the parameters for the sustainer
# Fin parameters are in the form (root chord, span, tip chord, sweep, tube length)
tubeParams = [(16, 7, 4, 10, 145), (16, 7, 4, 10, 145)]
mach = 0.69
# Create an object to run the simulations
finSim = AutoRASAero()
# Set the paths for the simulations
finSim.setPaths(CDX1_FILE, ENG_FILE, csvPath)
# Start RASAero
finSim.startupRASAero()
# run the simulation and print the output
result = finSim.runCDSimulations(5, tubeParams[0], tubeParams[1])
print("S Power Off: " + finSim.getCDforMachValue(result[0], mach))
print("S Power On: " + finSim.getCDforMachValue(result[1], mach))
print("B+S Power Off: " + finSim.getCDforMachValue(result[2], mach))
print("B+S Power On: " + finSim.getCDforMachValue(result[3], mach))
# Close RASAero
finSim.closeRASAero()
