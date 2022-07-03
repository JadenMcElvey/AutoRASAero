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
    lineList[30-16] = '      <Length>' + \
        str(rocketDict['bodyTubeLength']) + '</Length>\n'
    lineList[31-16] = '      <Diameter>' + \
        str(rocketDict['bodyTubeDiameter']) + '</Diameter>\n'
    lineList[37-16] = '      <Location>' + \
        str(rocketDict['noseConeLength']) + '</Location>\n'
    lineList[38-16] = '      <Color>' + \
        str(rocketDict['bodyTubeColor']) + '</Color>\n'
    lineList[45-16] = '        <Chord>' + \
        str(rocketDict['finChord']) + '</Chord>\n'
    lineList[46-16] = '        <Span>' + \
        str(rocketDict['finSpan']) + '</Span>\n'
    lineList[47-16] = '        <SweepDistance>' + \
        str(rocketDict['finSweepDistance']) + '</SweepDistance>\n'
    lineList[48-16] = '        <TipChord>' + \
        str(rocketDict['finTipChord']) + '</TipChord>\n'
    lineList[49-16] = '        <Thickness>' + \
        str(rocketDict['finThickness']) + '</Thickness>\n'
    lineList[51-16] = '        <Location>' + \
        str(rocketDict['finChord'] + rocketDict['finLocation']) + '</Location>\n'
    lineList[59-16] = '      <Length>' + \
        str(rocketDict['boosterLength']) + '</Length>\n'
    lineList[60-16] = '      <Diameter>' + \
        str(rocketDict['boosterDiameter']) + '</Diameter>\n'
    lineList[67-16] = '      <Location>' + \
        str(rocketDict['noseConeLength'] + rocketDict['bodyTubeLength']) + '</Location>\n'
    lineList[69-16] = '      <Color>' + \
        str(rocketDict['boosterColor']) + '</Color>\n'
    lineList[75-16] = '        <Chord>' + \
        str(rocketDict['finChord2']) + '</Chord>\n'
    lineList[76-16] = '        <Span>' + \
        str(rocketDict['finSpan2']) + '</Span>\n'
    lineList[77-16] = '        <SweepDistance>' + \
        str(rocketDict['finSweepDistance2']) + '</SweepDistance>\n'
    lineList[78-16] = '        <TipChord>' + \
        str(rocketDict['finTipChord2']) + '</TipChord>\n'
    lineList[79-16] = '        <Thickness>' + \
        str(rocketDict['finThickness2']) + '</Thickness>\n'
    lineList[81-16] = '        <Location>' + \
        str(rocketDict['finChord2'] + rocketDict['finLocation2']) + '</Location>\n'
    lineList[99-16] = '    <Altitude>' + \
        str(rocketDict['altitude']) + '</Altitude>\n'
    lineList[102-16] = '    <RodLength>' + \
        str(rocketDict['rodLength']) + '</RodLength>\n'
    lineList[104-16] = '    <WindSpeed>' + \
        str(rocketDict['windSpeed']) + '</WindSpeed>\n'

    mbsFile2 = open(r'.\Resources\MBSTemplate2.CDX1', 'w')
    mbsFile2.writelines(lineList)
    mbsFile2.close()
    