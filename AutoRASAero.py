import RASAeroInstance
import keyboard
import pathlib
import sys
import time

cwd = str(pathlib.Path.cwd())
CDX1_FILE = cwd + r"\Resources\MBS_43.CDX1"
ENG_FILE = cwd + r"\Resources\TCIMC3_(9899.7771)_5_5_2.329_11.0789_2.eng"

RASAero = RASAeroInstance.RASAeroInstance()
RASAero.start()
RASAero.loadRocket(CDX1_FILE)
RASAero.loadEngine(ENG_FILE)
RASAero.setFinParameters(RASAeroInstance.RocketSection.BodyTube, 16, 7, 4, 10, 0.4)
RASAero.setFinParameters(RASAeroInstance.RocketSection.Booster, 16, 7, 4, 10, 0.4)
csvPath = cwd + "\\fin.csv"
RASAero.setIgnitionDelayAndExportFlightSimData(csvPath, 6)
sys.exit()
