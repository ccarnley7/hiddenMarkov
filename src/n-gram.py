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

wordToTagProb = {}
tagToWordProb = {}

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
    for line in trainingData.splitlines():
        context = ['']
        for wordWithTag in line.split():
            word = (wordWithTag.split("_")[0]).lower()
            tag = wordWithTag.split("_")[1]
            temp = wordToTagModel.setdefault(str(context),{})
            temp[str(tag)] = temp.get(str(tag), 0) + 1
            wordToTagModel[str(context)] = temp

            tempTwo = tagToWordModel.setdefault(str(tag),{})
            tempTwo[str(word)] = tempTwo.get(str(word), 0) + 1
            tagToWordModel[str(tag)] = tempTwo

            context = (context+[word])[1:]
    wordToTagModel = generateProp(wordToTagModel)
    tagToWordModel = generateProp(tagToWordModel)

getWordList([''])
generateSenteces([''])
trainOnData()
print("test")