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

def getHOGFeatures(img):
    cropImg = img[:,:446]
    hog = ft.hog(cropImg,orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1))
    ret = ""
    for feature in hog:
        ret = ret + str(feature) + " " 
    return ret

def removeTrashSymbols(string):
    string = string.replace("\n","").replace("[","").replace("]","")
    while "  " in string:
        string = string.replace("  "," ")
    string = string.partition(" ")[2]
    return string

def genHOG(inputFiles, outputPath):
    np.set_printoptions(suppress=True)
    if os.path.exists(outputPath):
        shutil.rmtree(outputPath)
    os.makedirs(outputPath)
    for dirClasses in inputFiles:
        os.makedirs(outputPath+dirClasses[0].rpartition('/')[-1])
        print "Generate HOG to " + dirClasses[0].rpartition("/")[-1] + " Class...\n"
        for ffile in dirClasses[1]:
            inputFile = "/home/svaigen/TIC"+dirClasses[0].rpartition("..")[-1]+"/"+ffile
            ft = str(getHOGFeatures(data.load(inputFile)))
            ft = removeTrashSymbols(ft)
            outputFile = outputPath + (dirClasses[0].rpartition('/')[-1]) + "/" + inputFile.rpartition('/')[-1].replace(".png",".txt")
            f = open(outputFile,"w")
            f.write(ft)
            f.close()

inputPath, outputPath = getArgs()
inputFiles = readInputFiles(inputPath)
genHOG(inputFiles,outputPath)
