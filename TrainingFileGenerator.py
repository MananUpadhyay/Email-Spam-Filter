import os,shutil,random,sys

def readDirectory(path,outputFile):
    filesList = os.listdir(path)
    docuCount = len(filesList)
    print(docuCount)
    out = open(outputFile,'w')

    for file in filesList:
        docLine = ""
        docInLine = readFile(path+"/"+file)
        fName = file.split(".")
        docLine = fName[0]+" "+docInLine+"\n"
        out.write(docLine)
    out.close()
    return docuCount

def readFile(file):
    mLine = ""
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''+'''+'''
    punctuationSet = set(punctuations)
    f = open(file ,'r',errors='ignore')
    for line in f.readlines():
        st = line.split()
        for ch in st:
            if ch not in punctuationSet:
                mLine += ch + " "
    f.close()
    return mLine

def makeSentimentDev(sent_path,sent_dev_path):

    flist = os.listdir(sent_path)
    dirLen = len(flist)
    print(str(dirLen))

    dev_set = set()
    devSetSize  = 1500
    for findx in range(devSetSize):
        rand = random.randrange(0,dirLen)
        set_file = flist[rand]
        if set_file not in dev_set:
            dev_set.add(set_file)

    if not os.path.exists(sent_dev_path):
        os.makedirs(sent_dev_path)

    for fil in dev_set:
        shutil.move(sent_path+"/"+fil,sent_dev_path)

    print("SentDevSet MAde")




if __name__ == '__main__':


    path = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/SPAM_training"
    outputFile = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/spam_training.txt"

    sent_path = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/SENTIMENT_training"
    sent_out = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/sentiment_training.txt"

    dev_path = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/SPAM_dev"
    dev_out = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/spam_dev.txt"

    sent_dev_path = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/SENTIMENT_dev"
    sent_devOut = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/sentiment_dev.txt"

    spam_test_path = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/SPAM_test"
    sent_test_path = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/SENTIMENT_test"

    spam_test = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/spam_test.txt"
    sent_test = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/sentiment_test.txt"

    # path = sys.argv[1]
    # outputFile = sys.argv[2]

    if not os.path.isfile(outputFile):
        print("making spam training")
        readDirectory(path,outputFile)

    if not os.path.isfile(dev_out):
        print("making spam dev")
        readDirectory(dev_path,dev_out)

    if not os.path.isfile(sent_dev_path):
        makeSentimentDev(sent_path,sent_dev_path)

    if not os.path.isfile(sent_out):
        print("making sentiment training")
        readDirectory(sent_path,sent_out)

    if not os.path.isfile(sent_devOut):
        print("making sentiment dev")
        readDirectory(sent_dev_path,sent_devOut)

    if not os.path.isfile(spam_test):
        print("making spam test")
        readDirectory(spam_test_path,spam_test)

    if not os.path.isfile(sent_test):
        print("making sentiment test")
        readDirectory(sent_test_path,sent_test)


    # v = createVocabulary(outputFile)
    # print(len(v))
    # vocabularyFile = "/Users/Manan/Documents/CS_srtSpring_2015/NLP/hw1/vocabulary.txt"
    # voc = open(vocabularyFile, 'w')
    # for w in v:
    #     voc.write(w+"\n")
    # voc.close()