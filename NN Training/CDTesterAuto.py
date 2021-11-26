PASSWORD = ""
URL = "https://rrc-sim-orchestrator.fly.dev/"

import sys
import os
import requests

sys.path.append(".")
sys.path.append("..")
from Automation.AutoRASAero import AutoRASAero

if requests.get(URL+"status", auth=('bot', PASSWORD)).status_code != requests.codes.ok:
    sys.exit("Wrong password, failed to authenticate with API!")

# Get paths for rocket files and where to save the csv
CDX1_FILE = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\Resources\MBS_43_A.CDX1')))
ENG_FILE = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\Resources\PmotorRasp2.eng')))
csvPath = str(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\\Temp\\"

# Create an object to run the simulations
finSim = AutoRASAero()
# Set the paths for the simulations
finSim.setPaths(CDX1_FILE, ENG_FILE, csvPath)

while (True):
    response = requests.get(URL+"task", auth=('bot', PASSWORD)).json()
    data = response["data"]

    # Choose the tube parameters to simulate
    # First tuple is the parameters for the booster
    tipB = data["tip_b"]
    rootB = data["root_b"]
    spanB = data["span_b"]
    sweepB = data["sweep_b"]
    bodyLengthB = data["body_length_b"]
    boosterParams = (rootB, spanB, tipB, sweepB, bodyLengthB)
    # Second tuple is the parameters for the sustainer
    tipS = data["tip_s"]
    rootS = data["root_s"]
    spanS = data["span_s"]
    sweepS = data["sweep_s"]
    bodyLengthS = data["body_length_s"]
    sustainerParams = (rootS, spanS, tipS, sweepS, bodyLengthS)
    # Tube parameters are in the form (root chord, span, tip chord, sweep, tube length)
    tubeParams = [boosterParams, sustainerParams]
    # Get the body diameter and mach value
    bodyDiameter = data["body_diameter_bs"]
    mach = data["mach_number"]
    # Start RASAero
    finSim.startupRASAero()
    # run the simulation and upload the output
    result = finSim.runCDSimulations(bodyDiameter, tubeParams[0], tubeParams[1])
    powerOffS = finSim.getCDforMachValue(result[0], mach)
    powerOnS = finSim.getCDforMachValue(result[1], mach)
    powerOffBS = finSim.getCDforMachValue(result[2], mach)
    powerOnBS = finSim.getCDforMachValue(result[3], mach)

    payload = {
        "id": response["id"],
        "data": {
            "power_off_s": powerOffS,
            "power_on_s": powerOnS,
            "power_off_bs": powerOffBS,
            "power_on_bs": powerOnBS
        }
    }

    r = requests.post(URL+"task", json=payload, auth=('bot', PASSWORD))

    # Close RASAero
    finSim.closeRASAero()