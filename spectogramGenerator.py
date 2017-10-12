import os
import sys


def readInputFiles():
    try:
        inputPath = sys.argv[1]
    except:
        print 'Error. Input Path not specified (argv[1]). Aborting...'
        sys.exit()

    if not os.path.exists(inputPath):
        print 'Error. The Input Path \"' + inputPath + '\" does not exists. Aborting...'
        sys.exit()

    inputDirClasses = [inputPath + "/" + str(x) for x in os.listdir(inputPath)]
    inputFiles = []
    for dirClass in inputDirClasses:
        inputFiles.append([dirClass,os.listdir(dirClass)])
    return 0


inputFiles = readInputFiles()
