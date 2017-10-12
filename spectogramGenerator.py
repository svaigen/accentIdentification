#Exemplo de uso:
# python spectogramGenerator.py "../audios input/" "../spectograms/" 60 29 00:16 22000]

import os
import sys
import shutil

def getArgs():
    inputPath = ''
    outputPath = ''
    amplitude = ''
    pixelsPerSec = ''
    interval = ''
    rate = ''
    try:
        inputPath = sys.argv[1]
    except:
        print 'Error. Input Path not specified (argv[1]). Aborting...'
        sys.exit()
    try:
        outputPath = sys.argv[2]
    except:
        print 'Error. Output Path not specified (argv[2]). Aborting...'
        sys.exit()
    try:
        amplitude = sys.argv[3]
    except:
        print 'Error. Amplitude not specified (argv[3]). Aborting...'
        sys.exit()
    try:
        pixelsPerSec = sys.argv[4]
    except:
        print 'Error. Pixels per Second not specified (argv[4]). Aborting...'
        sys.exit()
    try:
        interval = sys.argv[5]
    except:
        print 'Error. Interval not specified (argv[5]). Aborting...'
        sys.exit()
    try:
        rate = sys.argv[6]
    except:
        print 'Error. Rate not specified (argv[6]). Aborting...'
        sys.exit()

    return inputPath, outputPath, amplitude, pixelsPerSec, interval, rate


def readInputFiles(inputPath):
    if not os.path.exists(inputPath):
        print 'Error. The Input Path \"' + inputPath + '\" does not exists. Aborting...'
        sys.exit()
    inputDirClasses = [inputPath + str(x) for x in os.listdir(inputPath)]
    inputFiles = []
    for dirClass in inputDirClasses:
        inputFiles.append([dirClass,os.listdir(dirClass)])
    return inputFiles

def genSpectogram(inputFiles, outputPath, amplitude, pixelsPerSec, interval, rate):
    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)
    os.makedirs(outputPath)

    for dirClasses in inputFiles:
        os.makedirs(outputPath+dirClasses[0].rpartition('/')[-1])
        for ffile in dirClasses[1]:
            inputFile = dirClasses[0]+"/"+ffile
            outputFile = outputPath + dirClasses[0].rpartition('/')[-1] + "/" + inputFile.rpartition('/')[-1].replace(".mp3","") + ".png"
            script = "sox \"" + inputFile + "\" -n spectrogram -z " + amplitude + " -d " + interval + " -X " + pixelsPerSec + " -y 694 -r -m -o " + outputFile
            os.system(script)

inputPath, outputPath, amplitude, pixelsPerSec, interval, rate = getArgs()
inputFiles = readInputFiles(inputPath)
genSpectogram(inputFiles, outputPath, amplitude, pixelsPerSec, interval, rate)
