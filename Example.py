import pathlib

from Automation.AutoRASAero import AutoRASAero

# Get paths for rocket files and where to save the csv
cwd = str(pathlib.Path.cwd())
CDX1_FILE = cwd + r"\Resources\MBS_43.CDX1"
ENG_FILE = cwd + r"\Resources\TCIMC3_(9899.7771)_5_5_2.329_11.0789_2.eng"
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
