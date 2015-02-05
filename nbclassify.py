import math,sys

def readModel(mFile):
    classes = {}
    priors = {}
    conditionalProbability = {}
    vocabulary = set()


    model = open(mFile,'r')
    # read total docs;
    docLine = model.readline().split()
    if docLine[0] == "TOTAL_DOCS":
        totalDocs = int(docLine[1])

    # read no of classes and word counts;
    clsLine = model.readline().split()
    if clsLine[0] == "CLASSES":
        for cls in range(int(clsLine[1])):
            classLine = model.readline().split()
            classes[classLine[0]] = classLine[1]

    # read prior probs;
    priorLine = model.readline().split()
    if priorLine[0] == "PRIORS":
        for prior in range(int(priorLine[1])):
            prLine = model.readline().split()
            priors[str(prLine[0])] = float(prLine[1])

    # read vocabulary;
    vocLine = model.readline().split()
    if vocLine[0] == "VOCABULARY":
        for word in range(int(vocLine[1])):
            vocWord = model.readline().split()
            vocabulary.add(str(vocWord[0]))

    # init condProb Dict;
    for cls in classes.keys():
        conditionalProbability[cls] = {}

    # read conditional probs;
    cprobLine = model.readline().split()
    if cprobLine[0] == "CON_PROB":
        conProbLine = model.readline()
        while(conProbLine != ""):
            conProb = conProbLine.split()
            wordProbDict = conditionalProbability[conProb[0]]
            wordProbDict[str(conProb[1])] = float(conProb[2])
            # conditionalProbability[str(conProb[0])] = wordProbDict
            conProbLine = model.readline()

    model.close()
    # print("todDoc: "+str(totalDocs))
    # print("classes len: " + str((classes["SPAM"])))
    # print("priors len: " + str((priors["HAM"])))
    # print("cP: "+ str(len(conditionalProbability)))
    # print("voc: "+str(len(vocabulary)))
    # print("condProb: " + str(len(conditionalProbability["SPAM"]))+"-2: "+str(len(conditionalProbability["HAM"])))
    return totalDocs,classes, priors, vocabulary,conditionalProbability

def classify(classes,priors,conditionalProbability,vocabulary,dfile):
    score = {} # Dictionary<Class,finalProb>
    vocoCount = len(vocabulary)
    prediction = []
    vals = []
    pc = 0

    dev = open(dfile,'r')
    # pred_out = open("spam.out",'w')
    # devClassVal = open("/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/val.txt",'w')

    for dline in dev.readlines():
        devLine = dline.split()
        vals.append(str( devLine[0]))
        # devClassVal.write(devLine[0]+"\n")
        for cl in classes.keys():
            score[cl] = math.log10(priors[cl])
            for word in devLine[1:]:
                if word not in vocabulary:
                    curProb = 1/(float(classes[cl]) + vocoCount)
                    curScore = math.log10(curProb)
                else:
                    wordDict = conditionalProbability[cl]
                    if word not in wordDict:
                        curProb2 = 1/(float(classes[cl]) + vocoCount)
                        curScore = math.log10(curProb2)
                    else:
                        curScore = float(wordDict[word])
                score[cl] += curScore

        # find maxscore for final predicted class;
        classList = list(classes.keys())
        maxClass = classList[0]
        maxScore = score[maxClass]
        for clss in score.keys():
            if score[clss] > maxScore:
                maxScore = score[clss]
                maxClass = clss
        #   TODO: print to STDOUT
        print(str(maxClass))
        # pred_out.write(maxClass+"\n")
        prediction.append(maxClass)
        pc+=1

    # devClassVal.close()
    # pred_out.close()
    dev.close()
    return prediction,vals


def getFScore(classes, preds,vs):
    valclassCounts = {}

    # actual spam/ham:
    for v in vs:
        if v not in classes:
            print("Error")
        if v not in valclassCounts:
            valclassCounts[v] = 0
        valclassCounts[v] += 1

    if len(preds) != len(vs):
        print("Error2")

    # classified spam/ham
    predclassCount = {}
    for c in range(len(preds)):
        cls = preds[c]
        if cls not in predclassCount:
            predclassCount[cls] = 0
        predclassCount[cls] += 1

    # correct spam/ham predictions
    truePreds = {}
    for ci in range(len(preds)):
        if vs[ci] == preds[ci]:
            clt = preds[ci]
            if clt not in truePreds:
                truePreds[clt] = 0
            truePreds[clt] += 1

    precision = {}
    recall = {}
    fScore = {}

    for clst in classes.keys():
        precision[clst] = truePreds[clst] / predclassCount[clst]
        # print("precision: " + str(clst) + " " + str(precision[clst]))
        recall[clst] = truePreds[clst] / valclassCounts[clst]
        # print("recall: " + str(clst) + " " + str(recall[clst]))
        fScore[clst] = (2 * precision[clst] * recall[clst]) / (precision[clst] + recall[clst])
        # print("fscore: " + str(clst) + " " + str(fScore[clst]))

    return precision, recall, fScore


if __name__ == '__main__':

    modelFile = sys.argv[1]
    testFile = sys.argv[2]

    td,cl,pr,voc,cprob = readModel(modelFile)
    preds,vs = classify(cl,pr,cprob,voc,testFile)

    # precision,recall,fscore = getFScore(cl,preds,vs)

