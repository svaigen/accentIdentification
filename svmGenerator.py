import os
import sys
import shutil
import random

def getArgs():
    featurePath = ''
    foldsPath = ''

    try:
        featurePath = sys.argv[1]
    except:
        print 'Error. Feature Path not specified (argv[1]). Aborting...'
        sys.exit()
    try:
        foldsPath = sys.argv[2]
    except:
        print 'Error. Folds Path not specified (argv[2]). Aborting...'
        sys.exit()
    try:
        nFolds = int(sys.argv[3])
    except:
        print 'Error. Number of folds not specified (argv[3]) or it\'s not an integer value. Aborting...'
        sys.exit()

    return featurePath, foldsPath, nFolds

def createFtList(featurePath, foldsPath):
    if not os.path.exists(featurePath):
        print 'Error. The Feature Path \"' + featurePath + '\" does not exists. Aborting...'
        sys.exit()

    if os.path.exists(foldsPath):
        shutil.rmtree(foldsPath)
    os.makedirs(foldsPath)

    featureDirClasses = [featurePath + str(x) for x in os.listdir(featurePath)]
    featureList = []
    i = 0
    infoFile = open(foldsPath+"info.txt","w")
    for dirClass in featureDirClasses:
        fileList = []
        for fPath in os.listdir(dirClass):
            f = open(dirClass+"/"+fPath)
            fileList.append(f.read())
            f.close()
        featureList.append([i,fileList])
        infoFile.write("Class: " + dirClass.rpartition("/")[-1] + " - Label: " + str(i) + " \n")
        i = i + 1
    infoFile.close()
    return featureList

def convertSVMFormat(featureList):
    listSVMFormat = []
    for ftClass in featureList:
        ftList = []
        for lineFt in ftClass[1]:
            features = ' '.join(['{}:{}'.format(i,ft) for (i,ft) in enumerate(lineFt.split(" "))]).replace('1. ','1.0 ')
            if "59:" in features: #fix feature 59 bug
                features = features.rpartition("59:")[0]
            svmLine = str(ftClass[0]) + " " + features + " \n"
            ftList.append(svmLine)
        random.shuffle(ftList)
        listSVMFormat.append([str(ftClass[0]),ftList])
    return listSVMFormat

def generateFolds(listSVMFormat, foldsPath, nFolds):
    folds = [None] * nFolds
    for fold in range(nFolds):
        f = open(foldsPath+"fold"+str(fold)+".svm","w" if fold == 0 else "a")
        for listSVM in listSVMFormat:
            initIndex = int(len(listSVM[1]) / (nFolds)) * fold #index inclusive
            endIndex = len(listSVM[1]) if fold == (nFolds - 1) else int(len(listSVM[1]) / (nFolds)) * (fold + 1) #index exclusive
            line = ''.join(x for x in listSVM[1][initIndex:endIndex])
            f.write(line)
        f.close()


featurePath, foldsPath, nFolds = getArgs()
featureList = createFtList(featurePath, foldsPath)
listSVMFormat = convertSVMFormat(featureList)
generateFolds(listSVMFormat, foldsPath, nFolds)
