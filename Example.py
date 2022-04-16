import pathlib
import pandas as pd
from Automation.mbsEditor import mbsEditor
from xlwt import Workbook


from Automation.AutoRASAero import AutoRASAero

# grab new rocket data from excel file
xl = pd.ExcelFile('Mach Input D2 Hypercube 12000.jmp.xlsx')
df = xl.parse('Mach Input D2 Hypercube 12000.j')

wb = Workbook()
sheet2 = wb.add_sheet('Sheet 2')

sheet2.write(0, 0, 'Booster Start Stability')
sheet2.write(0, 1, 'Booster End Stability')
sheet2.write(0, 2, 'Sustainer Start Stability')
sheet2.write(0, 3, 'Sustainer Max Stability')
sheet2.write(0, 4, 'Global Min Stability')
sheet2.write(0, 5, 'Global Max Stability')
sheet2.write(0, 6, 'Apogee')


for i in range(df.shape[0]):
    # rocketDict = {
    #     'noseConeLength': df['noseConeLength'][i],
    #     'noseConeDiameter': df['noseConeDiameter'][i],
    #     'noseConeShape': df['noseConeShape'][i],
    #     'noseConeBluntRadius': df['noseConeBluntRadius'][i],
    #     'noseConeColor': df['noseConeColor'][i],
    #     'bodyTubeLength': df['bodyTubeLength'][i],
    #     'bodyTubeDiameter': df['bodyTubeDiameter'][i],
    #     'bodyTubeColor': df['bodyTubeColor'][i],
    #     'bodyTubeLength2': df['bodyTubeLength2'][i],
    #     'bodyTubeDiameter2': df['bodyTubeDiameter2'][i],
    #     'bodyTubeColor2': df['bodyTubeColor2'][i],
    #     'finChord': df['finChord'][i],
    #     'finSpan': df['finSpan'][i],
    #     'finSweepDistance': df['finSweepDistance'][i],
    #     'finTipChord': df['finTipChord'][i],
    #     'finThickness': df['finThickness'][i],
    #     'finLocation': df['finLocation'][i],
    #     'boosterLength': df['boosterLength'][i],
    #     'boosterDiameter': df['boosterDiameter'][i],
    #     'boosterColor': df['boosterColor'][i],
    #     'finChord2': df['finChord2'][i],
    #     'finSpan2': df['finSpan2'][i],
    #     'finSweepDistance2': df['finSweepDistance2'][i],
    #     'finTipChord2': df['finTipChord2'][i],
    #     'finThickness2': df['finThickness2'][i],
    #     'finLocation2': df['finLocation2'][i],
    #     'altitude': df['altitude'][i],
    #     'rodLength': df['rodLength'][i],
    #     'windSpeed': df['windSpeed'][i]
    # }

    rocketDict = {
        'noseConeLength': 6.17*6,
        'noseConeDiameter': 6.17,
        'noseConeShape': 'Von Karman Ogive',
        'noseConeBluntRadius': 0,
        'noseConeColor': 'Black',
        'bodyTubeLength': df['Body Length B'][i],
        'bodyTubeDiameter': df['Body Diameter B+S'][i],
        'bodyTubeColor': 'Black',
        'bodyTubeLength2': df['Body Length S'][i],
        'bodyTubeDiameter2': df['Body Diameter B+S'][i],
        'bodyTubeColor2': 'Black',
        'finChord': 15,
        'finSpan': df['Span S'][i],
        'finSweepDistance': df['Sweep S'][i],
        'finTipChord': df['Tip S'][i],
        'finThickness': 0.5,
        'finLocation': 17,
        'boosterLength': 80.5,
        'boosterDiameter': df['Body Diameter B+S'][i],
        'boosterColor': 'Black',
        'finChord2': 15,
        'finSpan2': df['Span B'][i],
        'finSweepDistance2': df['Sweep B'][i],
        'finTipChord2': df['Tip B'][i],
        'finThickness2': 0.5,
        'finLocation2': 17,
        'altitude': 2050,
        'rodLength': 24,
        'windSpeed': df['Mach Number'][i],
    }
    try:
        mbsEditor(rocketDict)
        print(i)
        if i == 10:
            break
    except:
        print('Error on row {}'.format(i))
        break

    sheet2.write(i+1, 0, rocketDict['noseConeLength'])
    sheet2.write(i+1, 1, rocketDict['noseConeDiameter'])
    sheet2.write(i+1, 2, rocketDict['boosterDiameter'])
    sheet2.write(i+1, 3, rocketDict['noseConeBluntRadius'])
    sheet2.write(i+1, 4, rocketDict['finSpan'])
    sheet2.write(i+1, 5, rocketDict['bodyTubeLength'])
    sheet2.write(i+1, 6, rocketDict['finSweepDistance'])

    # save the data to the workbook

    wb.save('xlwt simulationResults.xls')




# # Get paths for rocket files and where to save the csv
# cwd = str(pathlib.Path.cwd())
# # CDX1_FILE = cwd + r"\Resources\MBS_43_A.CDX1"
# CDX1_FILE = cwd + r"\Resources\MBSTemplate2.CDX1"
# ENG_FILE = cwd + r"\Resources\PmotorRasp2.eng"
# csvPath = cwd + "\\Temp\\"

# # Choose the fin parameters to simulate
# # First tuple is the parameters for the booster
# # Second tuple is the parameters for the sustainer
# # Fin parameters are in formar (root chord, span, tip chord, sweep)
# finParams = [(17, 7.2, 12, 10), (17, 7.2, 12, 10)]
# # Create an object to run the simulations
# finSim = AutoRASAero()
# # Set the paths for the simulations
# finSim.setPaths(CDX1_FILE, ENG_FILE, csvPath)
# # Start RASAero
# finSim.startupRASAero()
# # run the simulation and print the output
# result = finSim.runStabilitySimulation(finParams[0], finParams[1], 6)
# print(result)
# # Close RASAero
# finSim.closeRASAero()
