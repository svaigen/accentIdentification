import os
import sys
import shutil
import numpy as np
import scipy
import skimage.feature as ft
from skimage import data

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

def getLBPFeatures(image, points, radius):
    lbp = ft.local_binary_pattern(image=image, P=points, R=radius, method='nri_uniform')
    hist = scipy.stats.itemfreq(lbp)
    hist = np.asarray([value for (i, value) in hist])
    max_value = hist.sum()
    hist = hist / max_value
    return hist

def removeTrashSymbols(string):
    string = string.replace("\n","").replace("[","").replace("]","")
    while "  " in string:
        string = string.replace("  "," ")
    string = string.partition(" ")[2]
    return string

def genLBP(inputFiles, outputPath):
    np.set_printoptions(suppress=True)
    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)
    os.makedirs(outputPath)
    for dirClasses in inputFiles:
        os.makedirs(outputPath+dirClasses[0].rpartition('/')[-1])
        print "Generate LBP for " + dirClasses[0].rpartition("/")[-1] + " Class...\n"
        for ffile in dirClasses[1]:
            inputFile = "/home/svaigen/TIC"+dirClasses[0].rpartition("..")[-1]+"/"+ffile
            hist = str(getLBPFeatures(data.load(inputFile),8,2))
            hist = removeTrashSymbols(hist)
            outputFile = outputPath + (dirClasses[0].rpartition('/')[-1]) + "/" + inputFile.rpartition('/')[-1].replace(".png",".txt")
            f = open(outputFile,"w")
            f.write(hist)
            f.close()

inputPath, outputPath = getArgs()
inputFiles = readInputFiles(inputPath)
genLBP(inputFiles,outputPath)
