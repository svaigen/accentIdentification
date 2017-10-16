import os
import sys
import shutil

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
        infoFile.write("Class: " + dirClass.rpartition("/")[-1] + " - Label: " + str(i) + "\n")
        i = i + 1
    infoFile.close()
    return featureList

featurePath, foldsPath, nFolds = getArgs()
featureList = createFtList(featurePath, foldsPath)
