import os
import sys
import shutil
from python_speech_features import mfcc
import scipy.io.wavfile as wav

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

def readInputFiles(inputPath):
    if not os.path.exists(inputPath):
        print 'Error. The Input Path \"' + inputPath + '\" does not exists. Aborting...'
        sys.exit()
    inputDirClasses = [inputPath + str(x) for x in os.listdir(inputPath)]
    inputFiles = []
    for dirClass in inputDirClasses:
        inputFiles.append([dirClass,os.listdir(dirClass)])
    return inputFiles

def genMfcc(inputFiles,outputPath):
    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)
    os.makedirs(outputPath)
    for dirClasses in inputFiles:
        os.makedirs(outputPath+dirClasses[0].rpartition('/')[-1])
        print "Generate MFCC for " + dirClasses[0].rpartition("/")[-1] + " Class..."
        for ffile in dirClasses[1]:
            (rate,sig) = wav.read(".."+ dirClasses[0].rpartition("..")[-1] + "/" + ffile)
            mfcc_feat = mfcc(signal=sig,samplerate=rate,nfft=2048)
            fid = open(outputPath + dirClasses[0].rpartition('/')[-1] + "/" + ffile.replace(".wav",".txt"), 'w')
            for c in range(len(mfcc_feat[0])):
                fid.write("%f " % mfcc_feat[0][c])
            for c in range(len(mfcc_feat[1])):
                fid.write("%f " % mfcc_feat[1][c])
            fid.close()


inputPath, outputPath = getArgs()
inputFiles = readInputFiles(inputPath)
genMfcc(inputFiles,outputPath)

#retirar com framework marsyas
