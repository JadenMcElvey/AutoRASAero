def mbsEditor(rocketDict):
    mbsFile2 = open(r'.\Resources\MBSTemplate2.CDX1', 'r')

    lineList = mbsFile2.readlines()

    lineList[5] = '      <Length>' + \
        str(rocketDict['noseConeLength']) + '</Length>\n'
    lineList[6] = '      <Diameter>' + \
        str(rocketDict['noseConeDiameter']) + '</Diameter>\n'
    lineList[7] = '      <Shape>' + \
        str(rocketDict['noseConeShape']) + '</Shape>\n'
    lineList[8] = '      <BluntRadius>' + \
        str(rocketDict['noseConeBluntRadius']) + '</BluntRadius>\n'
    lineList[10] = '      <Color>' + \
        str(rocketDict['noseConeColor']) + '</Color>\n'
    lineList[14] = '      <Length>' + \
        str(rocketDict['bodyTubeLength']) + '</Length>\n'
    lineList[15] = '      <Diameter>' + \
        str(rocketDict['bodyTubeDiameter']) + '</Diameter>\n'
    lineList[21] = '      <Location>' + \
        str(rocketDict['noseConeLength']) + '</Location>\n'
    lineList[22] = '      <Color>' + \
        str(rocketDict['bodyTubeColor']) + '</Color>\n'
    lineList[30] = '      <Length>' + \
        str(rocketDict['bodyTubeLength2']) + '</Length>\n'
    lineList[31] = '      <Diameter>' + \
        str(rocketDict['bodyTubeDiameter2']) + '</Diameter>\n'
    lineList[37] = '      <Location>' + \
        str(rocketDict['noseConeLength'] + rocketDict['bodyTubeLength']) + '</Location>\n'
    lineList[38] = '      <Color>' + \
        str(rocketDict['bodyTubeColor2']) + '</Color>\n'
    lineList[45] = '        <Chord>' + \
        str(rocketDict['finChord']) + '</Chord>\n'
    lineList[46] = '        <Span>' + \
        str(rocketDict['finSpan']) + '</Span>\n'
    lineList[47] = '        <SweepDistance>' + \
        str(rocketDict['finSweepDistance']) + '</SweepDistance>\n'
    lineList[48] = '        <TipChord>' + \
        str(rocketDict['finTipChord']) + '</TipChord>\n'
    lineList[49] = '        <Thickness>' + \
        str(rocketDict['finThickness']) + '</Thickness>\n'
    lineList[51] = '        <Location>' + \
        str(rocketDict['finChord'] + rocketDict['finLocation']) + '</Location>\n'
    lineList[59] = '      <Length>' + \
        str(rocketDict['boosterLength']) + '</Length>\n'
    lineList[60] = '      <Diameter>' + \
        str(rocketDict['boosterDiameter']) + '</Diameter>\n'
    lineList[66] = '      <Location>' + \
        str(rocketDict['noseConeLength'] + rocketDict['bodyTubeLength'] + rocketDict['bodyTubeLength2']) + '</Location>\n'
    lineList[69] = '      <Color>' + \
        str(rocketDict['boosterColor']) + '</Color>\n'
    lineList[75] = '        <Chord>' + \
        str(rocketDict['finChord2']) + '</Chord>\n'
    lineList[76] = '        <Span>' + \
        str(rocketDict['finSpan2']) + '</Span>\n'
    lineList[77] = '        <SweepDistance>' + \
        str(rocketDict['finSweepDistance2']) + '</SweepDistance>\n'
    lineList[78] = '        <TipChord>' + \
        str(rocketDict['finTipChord2']) + '</TipChord>\n'
    lineList[79] = '        <Thickness>' + \
        str(rocketDict['finThickness2']) + '</Thickness>\n'
    lineList[81] = '        <Location>' + \
        str(rocketDict['finChord2'] + rocketDict['finLocation2']) + '</Location>\n'
    lineList[99] = '    <Altitude>' + \
        str(rocketDict['altitude']) + '</Altitude>\n'
    lineList[102] = '    <RodLength>' + \
        str(rocketDict['rodLength']) + '</RodLength>\n'
    lineList[104] = '    <WindSpeed>' + \
        str(rocketDict['windSpeed']) + '</WindSpeed>\n'

    mbsFile2 = open(r'.\Resources\MBSTemplate2.CDX1', 'w')
    mbsFile2.writelines(lineList)
    mbsFile2.close()
    