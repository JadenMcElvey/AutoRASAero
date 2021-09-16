import RASAeroInstance
import pathlib
import time
import csv
import sys

cwd = str(pathlib.Path.cwd())
CDX1_FILE = cwd + r"\Resources\MBS_43.CDX1"
ENG_FILE = cwd + r"\Resources\TCIMC3_(9899.7771)_5_5_2.329_11.0789_2.eng"
csvPath = cwd + "\\fin.csv"

finParams = []
finParams.append((16,7,4,10))

RASAero = RASAeroInstance.RASAeroInstance()
RASAero.start()
RASAero.loadRocket(CDX1_FILE)
RASAero.loadEngine(ENG_FILE)
RASAero.setFinParameters(RASAeroInstance.RocketSection.BodyTube, finParams[0][0], finParams[0][1], finParams[0][2], finParams[0][3])
RASAero.setFinParameters(RASAeroInstance.RocketSection.Booster, finParams[0][0], finParams[0][1], finParams[0][2], finParams[0][3])
RASAero.setIgnitionDelayAndExportFlightSimData(csvPath, 6)
time.sleep(10)

reader = csv.reader(open(csvPath))
minStability = 9999999
maxStability = 0
next(reader)
for row in reader:
    stabilityMargin = float(row[13])
    minStability = stabilityMargin if (stabilityMargin != 0) and (stabilityMargin < minStability) else minStability
    maxStability = stabilityMargin if stabilityMargin > maxStability else maxStability

finParamStr = "Root chord:" + str(finParams[0][0]) + " Span:" + str(finParams[0][1]) + " Tip Chord:" + str(finParams[0][2]) + " Sweep Distance: " + str(finParams[0][3])
finStabilityStr = "Min Stability:" + str(minStability) + " Max Stability:" + str(maxStability)
print(finParamStr, finStabilityStr)
