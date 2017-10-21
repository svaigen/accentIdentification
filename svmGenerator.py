import os
import sys
import shutil
import random

def getArgs():
    featurePath = ''
    foldsPath = ''
    outputPath = ''

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
    try:
        balanced = int(sys.argv[4])
    except:
        print 'Error. Balanced Class type not specified (argv[4]). Aborting...'
        sys.exit()
    try:
        outputPath = sys.argv[5]
    except:
        print 'Error. Output Path not specified (argv[5]). Aborting...'
        sys.exit()

    return featurePath, foldsPath, nFolds, balanced, outputPath

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
    infoFile.write("----------------------------------------------------\n")
    infoFile.close()
    return featureList

def convertSVMFormat(featureList):
    listSVMFormat = []
    for ftClass in featureList:
        ftList = []
        for lineFt in ftClass[1]:
            features = ' '.join(['{}:{}'.format(i+1,ft) for (i,ft) in enumerate(lineFt.split(" "))]).replace('1. ','1.0 ')
            if "60:" in features: #fix feature 60 bug
                features = features.rpartition("59:")[0]
            svmLine = str(ftClass[0]) + " " + features + " \n"
            ftList.append(svmLine)
        random.shuffle(ftList)
        listSVMFormat.append([str(ftClass[0]),ftList])
    return listSVMFormat

def getMinExamples(listSVM):
    vMin = len(listSVM[0][1])
    for examples in listSVM:
        vMin = len(examples[1]) if vMin > len(examples[1]) else vMin
    return vMin

def generateFolds(listSVMFormat, foldsPath, nFolds,balanced):
    folds = [None] * nFolds
    infoFile = open(foldsPath+"info.txt","a")
    totalExamplesPerClass = getMinExamples(listSVMFormat) if balanced else 0
    for fold in range(nFolds):
        f = open(foldsPath+ "fold" + str(fold) + ".svm","w" if fold == 0 else "a")
        infoFile.write("Fold n. " + str(fold) + ": \n")
        for listSVM in listSVMFormat:
            nExamples = len(listSVM[1]) if totalExamplesPerClass == 0 else totalExamplesPerClass
            initIndex = int(nExamples / (nFolds)) * fold #index inclusive
            endIndex = nExamples if fold == (nFolds - 1) else int(nExamples / (nFolds)) * (fold + 1) #index exclusive
            line = ''.join(x for x in listSVM[1][initIndex:endIndex])
            f.write(line)
            infoFile.write("Class " + str(listSVM[0]) + ": " + str(endIndex - initIndex) + " occurrences \n")
        f.close()
        infoFile.write("\n")
    infoFile.close()

def execSVM(foldsPath, nFolds, fold):
    print "\nExec n. " + str(fold) + " - Training fold " + str(fold)
    execPath = foldsPath+"exec"+str(fold)+"/"
    classificationPath= execPath + "classification-fold" + str(fold) + ".svm"
    trainingPath = execPath + "training.svm"

    if os.path.exists(execPath):
        shutil.rmtree(execPath)
    os.makedirs(execPath)

    shutil.copy(foldsPath+"fold"+str(fold)+".svm",classificationPath)
    trainingFile = open(trainingPath,"w")
    for n in range(nFolds):
        if n != fold:
            f = open(foldsPath + "fold" + str(n) + ".svm", "r")
            content = f.readlines()
            f.close()
            for line in content:
                trainingFile.write(line)
    trainingFile.close()

    cmd = "python easySvaigen.py " + trainingPath + " " + classificationPath
    os.system(cmd)


featurePath, foldsPath, nFolds, balanced, outputPath = getArgs()
featureList = createFtList(featurePath, foldsPath)
listSVMFormat = convertSVMFormat(featureList)
generateFolds(listSVMFormat, foldsPath, nFolds, balanced)
print "Exec SVM...\n"
for fold in range(nFolds):
    execSVM(foldsPath,nFolds,fold)
os.system("python analysisGenerator.py " + foldsPath + " " + outputPath)
os.system("mv " + foldsPath + "* " + outputPath)
os.system("Classification done. See the results in: " + outputPath)
