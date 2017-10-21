import os
import sys
import shutil
import numpy as np

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

def calculateAccuracy(expectedList,predictedList):
    hits = 0
    for i in range(len(expectedList)):
        hits = hits + 1 if expectedList[i] == predictedList[i] else hits
    return (float(hits) / float(len(expectedList)))

def calculateConfusionMatrix(expectedList, predictedList):
    numberOfClass = expectedList.max() + 1
    cm = [[0 for i in range(numberOfClass)] for j in range(numberOfClass)]
    for i in range(numberOfClass):
        for j in range(numberOfClass):
            total = 0
            for k in range(len(expectedList)):
                if (expectedList[k] == i) and (predictedList[k] == j):
                    total = total + 1
            cm[i][j] = total
    return cm

def calculatePrecisionRecall(confusionMatrix):
    recalls = []
    for i in range(len(confusionMatrix)):
        recalls.append(float(confusionMatrix[i][i]) / float(confusionMatrix[i].sum()))
    precisions = []
    cmT = np.transpose(confusionMatrix)
    for i in range(len(cmT)):
        precisions.append(0 if cmT[i].sum() == 0 else float(cmT[i][i]) / float(cmT[i].sum()))
    return np.asarray(precisions,dtype=np.float), np.asarray(recalls,dtype=np.float)

def calculateFMeasure(precisions,recalls):
    fMeasures = []
    for i in range(len(precisions)):
        fMeasures.append(0 if precisions[i] + recalls[i] == 0 else (2*precisions[i]*recalls[i])/(precisions[i]+recalls[i]))
    return np.asarray(fMeasures,dtype=np.float)

def genAnalysisFile(foldNumber,expectedList,predictedList,predictionList,accuracy,confusionMatrix,precisions,recalls,fMeasures,macroF,outputPath):
    path = outputPath
    fileName = "fold"+str(foldNumber)+"-analysis.csv"
    if not os.path.exists(path):
        os.makedirs(path)
    f = open(path+fileName,"w")
    cabecalho = "".join("{};".format(i) for (i,ft) in enumerate(fMeasures))
    content = "Arquivo;fold"+str(foldNumber)+"-analysis.csv\n"
    content += "Acertos;" + str(accuracy)+"\n\n"
    content += "Classe Esperada;Classe Predita;" + cabecalho + "\n"
    for i in range(len(expectedList)):
        content += str(expectedList[i]) + ";" + str(predictedList[i]) + ";" + predictionList[i]  + "\n"
    content += "\nMatriz de Confusao;" + cabecalho + "Recall\n"
    for i in range(len(confusionMatrix)):
        content += str(i) + ";" + ''.join("{};".format(d) for (i,d) in enumerate(confusionMatrix[i])) + str(recalls[i]) + "\n"
    content += "Precision;"
    for i in range(len(confusionMatrix)):
        content += str(precisions[i]) + ";"
    content+="\n\nClasse;F-Measure\n"
    for i in range(len(fMeasures)):
        content+=str(i)+";"+str(fMeasures[i])+"\n"
    content+="MacroF;"+str(macroF)
    f.write(content)
    f.close()


def genAnalysis(inputPath,outputPath):
    files = os.listdir(inputPath)
    svmFiles = []
    accuracys = []
    for f in files:
        svmFiles.append(f) if ".svm" in f else None
    for svmF in svmFiles:
        f = open(inputPath+svmF,"r")

        #lendo as classes esperadas
        expectedList = []
        for line in f.readlines():
            classExpected = line.partition(" ")[0]
            expectedList.append(classExpected)

        #lendo as classes preditas e os valores de predicoes
        predictedList = []
        predictionList = []
        foldNumber = svmF.partition("fold")[2].partition(".")[0]
        fp = open(inputPath+"exec"+foldNumber+"/classification-fold"+foldNumber+".predict","r")
        lines = fp.readlines()
        lines = lines[1:]
        for line in lines:
            predictedList.append(line.split(" ",1)[0])
            predictionList.append(line.split(" ",1)[1].replace("\n","").replace(" ",";"))
        fp.close()
        f.close()

        #calculos gerais
        accuracy = calculateAccuracy(expectedList,predictedList)
        confusionMatrix = calculateConfusionMatrix(np.asarray(expectedList,dtype=np.uint8),np.asarray(predictedList,dtype=np.uint8))
        precisions, recalls = calculatePrecisionRecall(np.asarray(confusionMatrix,dtype=np.uint8))
        fMeasures = calculateFMeasure(precisions, recalls)
        macroF = np.mean(fMeasures)
        genAnalysisFile(foldNumber,expectedList,predictedList,predictionList,accuracy,confusionMatrix,precisions,recalls,fMeasures,macroF,outputPath)
        accuracys.append([foldNumber,accuracy])

    return accuracys

def genInfoFiles(accuracys):
    f = open(inputPath+"info.txt","a")
    f.write("------------------------------------------\n")
    f.write("------Classification accuracy info:\n")
    for acc in accuracys:
        f.write("- Fold " + str(acc[0]) + ": "+str(acc[1])+"\n")
    f.close()

print "Generating Analysis..."
inputPath, outputPath = getArgs()
accuracys = genAnalysis(inputPath, outputPath)
genInfoFiles(accuracys)
