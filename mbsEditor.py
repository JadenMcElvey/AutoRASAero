# mbsFile = open(r'C:\Users\Alex\Desktop\Code\Gatech\RocketClub\AutoRASAero\Resources\MBSTemplate.txt')
mbsFile2 = open(
    r'C:\Users\Alex\Desktop\Code\Gatech\RocketClub\AutoRASAero\Resources\MBSTemplate2.txt', 'r')

lineList = mbsFile2.readlines()

def mbsEditor(noseConeLength, noseConeDiameter, noseConeShape, noseConeBluntRadius, noseConeColor, bodyTubeLength, bodyTubeDiameter, bodyTubeColor, bodyTubeLength2, bodyTubeDiameter2, bodyTubeColor2, finChord, finSpan, finSweepDistance, finTipChord, finThickness, finLocation, boosterLength, boosterDiameter, boosterColor, finChord2, finSpan2, finSweepDistance2, finTipChord2, finThickness2, finLocation2, altitude, rodLength, windSpeed):
    lineList[5] = '      <Length>' + \
        str(noseConeLength) + '</Length>\n'
    lineList[6] = '      <Diameter>' + \
        str(noseConeDiameter) + '</Diameter>\n'
    lineList[7] = '      <Shape>' + \
        str(noseConeShape) + '</Shape>\n'
    lineList[8] = '      <BluntRadius>' + \
        str(noseConeBluntRadius) + '</BluntRadius>\n'
    lineList[10] = '      <Color>' + \
        str(noseConeColor) + '</Color>\n'
    lineList[14] = '      <Length>' + \
        str(bodyTubeLength) + '</Length>\n'
    lineList[15] = '      <Diameter>' + \
        str(bodyTubeDiameter) + '</Diameter>\n'
    lineList[21] = '      <Location>' + \
        str(noseConeLength) + '</Location>\n'
    lineList[22] = '      <Color>' + \
        str(bodyTubeColor) + '</Color>\n'
    lineList[30] = '      <Length>' + \
        str(bodyTubeLength2) + '</Length>\n'
    lineList[31] = '      <Diameter>' + \
        str(bodyTubeDiameter2) + '</Diameter>\n'
    lineList[37] = '      <Location>' + \
        str(noseConeLength + bodyTubeLength) + '</Location>\n'
    lineList[38] = '      <Color>' + \
        str(bodyTubeColor2) + '</Color>\n'
    lineList[45] = '        <Chord>' + \
        str(finChord) + '</Chord>\n'
    lineList[46] = '        <Span>' + \
        str(finSpan) + '</Span>\n'
    lineList[47] = '        <SweepDistance>' + \
        str(finSweepDistance) + '</SweepDistance>\n'
    lineList[48] = '        <TipChord>' + \
        str(finTipChord) + '</TipChord>\n'
    lineList[49] = '        <Thickness>' + \
        str(finThickness) + '</Thickness>\n'
    lineList[51] = '        <Location>' + \
        str(finChord + finLocation) + '</Location>\n'
    lineList[59] = '      <Length>' + \
        str(boosterLength) + '</Length>\n'
    lineList[60] = '      <Diameter>' + \
        str(boosterDiameter) + '</Diameter>\n'
    lineList[66] = '      <Location>' + \
        str(noseConeLength + bodyTubeLength + bodyTubeLength2) + '</Location>\n'
    lineList[69] = '      <Color>' + \
        str(boosterColor) + '</Color>\n'
    lineList[75] = '        <Chord>' + \
        str(finChord2) + '</Chord>\n'
    lineList[76] = '        <Span>' + \
        str(finSpan2) + '</Span>\n'
    lineList[77] = '        <SweepDistance>' + \
        str(finSweepDistance2) + '</SweepDistance>\n'
    lineList[78] = '        <TipChord>' + \
        str(finTipChord2) + '</TipChord>\n'
    lineList[79] = '        <Thickness>' + \
        str(finThickness2) + '</Thickness>\n'
    lineList[81] = '        <Location>' + \
        str(finChord2 + finLocation2) + '</Location>\n'
    lineList[99] = '    <Altitude>' + \
        str(altitude) + '</Altitude>\n'
    lineList[102] = '    <RodLength>' + \
        str(rodLength) + '</RodLength>\n'
    lineList[104] = '    <WindSpeed>' + \
        str(windSpeed) + '</WindSpeed>\n'



mbsEditor(3000, 500, 'round', 50, 60, 1000, 10, 20, 30, 40, 'red', 60, 70, 100, 200, 300, 10, 20, 30, 'blue', 40, 100, 230, 500, 10, 20, 30000, 50, 100)
mbsFile2 = open(
    r'C:\Users\Alex\Desktop\Code\Gatech\RocketClub\AutoRASAero\Resources\MBSTemplate2.txt', 'w')
mbsFile2.writelines(lineList)
mbsFile2.close()
