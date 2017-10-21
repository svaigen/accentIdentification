import os
import sys
import shutil

def getArgs():
    inputPath = ''
    outputPath = ''
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

    return inputPath, outputPath


inputPath, outputPath = getArgs()

if not os.path.exists(inputPath):
    print 'Error. The Input Path \"' + inputPath + '\" does not exists. Aborting...'
    sys.exit()
inputDirClasses = [inputPath + str(x) for x in os.listdir(inputPath)]
inputFiles = []
for dirClass in inputDirClasses:
    dirr = dirClass.rsplit("/")[-1]
    if os.path.exists(outputPath+dirr):
        shutil.rmtree(outputPath+dirr)
    os.makedirs(outputPath+dirr)
    for arq in os.listdir(dirClass):
        cmd = "sox " + dirClass + "/" + arq + " " + outputPath + dirr + "/" + arq.replace("mp3","wav")
        os.system(cmd)
