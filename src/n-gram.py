import random

infilename = "2009-obama.txt"
testingFile = "testing.txt"
trainingFile = "training.txt"
infiledata = open(infilename).read()
trainingData = open(trainingFile).read()
testingData = open(testingFile).read()

model = {}
wordToTagModel = {}
tagToWordModel = {}

tagToTagProb = {}
tagToWordProb = {}
startSentenceList = {}
listofTags = []
totalSentences = 0

def chooseWord(wordDictionary):
    total = 0
    probabilities = {}
    for word in wordDictionary:
        total += wordDictionary.get(word)
    for word in wordDictionary:
        probabilities[word] = (wordDictionary.get(word)/total) * 100
    guess = random.random()
    runningTotal = 0;
    for word in probabilities:
        prob = probabilities.get(word)
        runningTotal += prob
        if runningTotal > guess:
            return word

    return "ERROR"

def generateProp(model):
    newModel={}
    for key, value in model.items():
        probabilities = {}
        total = 0
        for word in value:
            total += value.get(word)
        for word in value:
            probabilities[word] = (value.get(word)/total) * 100
        newModel[key] = probabilities
    return newModel


def getWordList(context):
    for word in infiledata.split():
        word = word.lower()
        temp = model.setdefault(str(context),{})
        temp[str(word)] = temp.get(str(word), 0) + 1
        model[str(context)] = temp
        context = (context+[word])[1:]


def generateSenteces(context):
    for i in range(100):
        word = chooseWord(model[str(context)])
        print(word,end=" ")
        context = (context+[word])[1:]

    print()

def trainOnData():
    global wordToTagModel
    global tagToWordModel
    global totalSentences
    global startSentenceList
    global listofTags
    for line in trainingData.splitlines():
        context = ['']
        firstWord = True
        for wordWithTag in line.split():
            word = (wordWithTag.split("_")[0]).lower()
            tag = wordWithTag.split("_")[1]
            listofTags.append(tag)
            if firstWord:
                startSentenceList[tag] = startSentenceList.setdefault(tag, 0) + 1
                totalSentences += 1

                firstWord = False

            else:
                temp = wordToTagModel.setdefault(str(context),{})
                temp[str(tag)] = temp.get(str(tag), 0) + 1
                wordToTagModel[str(context)] = temp

            tempTwo = tagToWordModel.setdefault(str(tag),{})
            tempTwo[str(word)] = tempTwo.get(str(word), 0) + 1
            tagToWordModel[str(tag)] = tempTwo

            # context = (context+[word])[1:]
            context = tag

    for key, value in startSentenceList.items():
        startSentenceList[key] = value/totalSentences
    wordToTagModel = generateProp(wordToTagModel)
    tagToWordModel = generateProp(tagToWordModel)
    listofTags = set(listofTags)

def useTrainingData():
    for line in testingData.splitlines():
        for word in line:
            print(word)

getWordList([''])
# generateSenteces([''])
trainOnData()
useTrainingData()