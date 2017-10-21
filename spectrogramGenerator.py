#Exemplo de uso:
# python spectrogramGenerator.py ../audios-mp3/ ../spectrograms/ 80 27 18000
# gera: sox ../audios-mp3/<arquivo> -n rate 18000 spectrogram -z 80 -X 27 -y 694 -r -m -o ../spectrograms/<arquivo>

import os
import sys
import shutil

def getArgs():
    inputPath = ''
    outputPath = ''
    amplitude = ''
    pixelsPerSec = ''
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
        rate = sys.argv[5]
    except:
        print 'Error. Rate not specified (argv[6]). Aborting...'
        sys.exit()

    return inputPath, outputPath, amplitude, pixelsPerSec, rate


def readInputFiles(inputPath):
    if not os.path.exists(inputPath):
        print 'Error. The Input Path \"' + inputPath + '\" does not exists. Aborting...'
        sys.exit()
    inputDirClasses = [inputPath + str(x) for x in os.listdir(inputPath)]
    inputFiles = []
    for dirClass in inputDirClasses:
        inputFiles.append([dirClass,os.listdir(dirClass)])
    return inputFiles

def genSpectogram(inputFiles, outputPath, amplitude, pixelsPerSec, rate):
    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)
    os.makedirs(outputPath)

    for dirClasses in inputFiles:
        print "Generating Spectrogram for path " + outputPath+dirClasses[0].rpartition('/')[-1] + "\n"
        os.makedirs(outputPath+dirClasses[0].rpartition('/')[-1])
        for ffile in dirClasses[1]:
            inputFile = dirClasses[0]+"/"+ffile
            outputFile = outputPath + dirClasses[0].rpartition('/')[-1] + "/" + inputFile.rpartition('/')[-1].replace(".mp3","") + ".png"
            script = "sox \"" + inputFile + "\" -n rate " + rate + " spectrogram -z " + amplitude + " -X " + pixelsPerSec + " -y 694 -r -m -o " + outputFile
            os.system(script)

inputPath, outputPath, amplitude, pixelsPerSec, rate = getArgs()
inputFiles = readInputFiles(inputPath)
genSpectogram(inputFiles, outputPath, amplitude, pixelsPerSec, rate)
