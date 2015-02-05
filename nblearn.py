import math,os,sys

def createVocabulary(outputFile):
    spamTraining = open(outputFile,'r')
    vocabulary = set()
    classes = {}
    classCountMap = {}

    for lines in spamTraining.readlines():
        strLin = lines.split()
        # find Vocabulary words
        for word in strLin:
            if word not in vocabulary:
                if word.isalpha():
                    vocabulary.add(word)
        # find no of classes
        cls = strLin[0]
        if cls not in classes:
            classes[cls] = 0
            if cls not in classCountMap:
                classCountMap[cls] = 0

        # find class counts
        currClassCount = classCountMap[cls]
        classCountMap[cls] = currClassCount+1
        # find num of words in a class
        classes[cls] = classes[cls] +(len(strLin) - 1)

    spamTraining.close()
    # print("classes len: " + str(len(classes)))
    # print("vocabulary: " + str(len(vocabulary)))
    # print("classContMap: " + str(len(classCountMap)))

    return vocabulary, classes, classCountMap


def getTotalDocs(classCntMap):
    docsCount = 0
    for clsd in classCntMap:
        docsCount += classCntMap[clsd]
    return docsCount


def getClassPriors(classCountMap, docuCount):
    classPriors = {}
    for clsPrior in classCountMap:
        classPriors[clsPrior] = classCountMap[clsPrior] / docuCount
    # print("priors len: " + str(len(classPriors)))
    return classPriors

def learn(vocabulary,classes,classCountMap,docuCount,spam_training_path):
    vocoCount = len(vocabulary)
    # print("voc Count"+str(vocoCount))
    priors = getClassPriors(classCountMap,docuCount)   #Dictionary<class,probability>

    classWordCountDictionary = {}  # Dictionary<Class,Dictionary<word,wordcount>>
    conditionalProbDictionary = {}      #Dictionary<Class,Dictionary<word,probability>>


    spamTrain = open(spam_training_path,'r')
    # finding word occurrence per class
    for clss in classes.keys():
        if clss not in classWordCountDictionary:
            classWordCountDictionary[clss] = {}
    # get counts of words|class
    for line in spamTrain.readlines():
        strLine = line.split()
        clsKey = strLine[0]
        for word in strLine[1:]:
            wordCountDictionary = classWordCountDictionary[clsKey]
            if word in vocabulary:
                if word not in wordCountDictionary:
                    wordCountDictionary[word] = 0
                wordCountDictionary[word] = wordCountDictionary[word] +1

    # print("classWCDict: " + str(len(classWordCountDictionary["SPAM"])) +"-1: "+str(len(classWordCountDictionary["HAM"])))
    spamTrain.close()

    # finding total word occurrences per class
    # for cls in classes:
    #     wordCountDictionaryNew = classWordCountDictionary[cls]
    #     wordOccurance = 0
    #     for word in wordCountDictionaryNew:
    #         wordOccurance += wordCountDictionaryNew[word]
    #     classWordOccuranceDictionary[cls] = wordOccurance
    # print("classWorOccDict: " + str(len(classWordOccuranceDictionary)))


    # finding conditional probability per word per class
    for clsp in classes.keys():
        # get probabilities of each word|class
        wordCountDictionaryFin = classWordCountDictionary[clsp]

        if clsp not in conditionalProbDictionary:
            conditionalProbDictionary[clsp] = {}

        for word in wordCountDictionaryFin:
            wordCountGivenClass = wordCountDictionaryFin[word] + 1 # add 1 smoothing:wordLevel;
            denom = classes[clsp] + vocoCount # add 1 smoothing:VocoLevel;
            wordProbability = conditionalProbDictionary[clsp]
            wordProbability[word] = math.log10(wordCountGivenClass/denom)
    # print("condProb: " + str(len(conditionalProbDictionary["SPAM"]))+"-2: "+str(len(conditionalProbDictionary["HAM"])))
    return priors,conditionalProbDictionary


def writeModel(classes,priors,conditionalProbability,vocabularyF,docuCount,model_file):
    if not os.path.isfile(model_file):
        model = open(model_file,'a')
    else:
        model = open(model_file,'w')

    # write totalDocs;
    model.write("TOTAL_DOCS"+" "+str(docuCount) + "\n")
    # write classes;
    model.write("CLASSES" + " " + str(len(classes))+"\n")
    for cls1 in classes:
        model.write(cls1+ " " + str(classes[cls1])+"\n")

    # write priors;
    model.write("PRIORS" + " " +str(len(priors))+"\n")
    for cls2 in priors:
        strPrior = cls2 + " " + str(priors[cls2])
        model.write(strPrior + "\n")

    # write vocabulary;
    model.write("VOCABULARY" + " " + str(len(vocabularyF))+"\n")
    for wrd in vocabularyF:
        strWord = str(wrd)
        model.write(strWord+ "\n")

    # write probabilities;
    model.write("CON_PROB"+" "+str(len(conditionalProbability))+"\n")
    # print(conditionalProbability)
    for cls3 in classes.keys():
        wordProbDict = conditionalProbability[cls3]
        for word in wordProbDict:
            strConProb = cls3+" "+word+" "+ str(wordProbDict[word])
            model.write(strConProb+"\n")

    model.close()


if __name__ == '__main__':

    #get spam_train & model_file from args

    trainFile = sys.argv[1]
    modelFile = sys.argv[2]


    # trainFile = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/spam_training.txt"
    # modelFile = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/spam.nb"


    vocabularyFO,classesFO,classCountMapFO = createVocabulary(trainFile)

    docuCount = getTotalDocs(classCountMapFO)

    priorsR,conditionalProbabilityR = learn(vocabularyFO,classesFO,classCountMapFO,docuCount,trainFile)

    writeModel(classesFO,priorsR,conditionalProbabilityR,vocabularyFO,docuCount,modelFile)
    