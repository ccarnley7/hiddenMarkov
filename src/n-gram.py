import random
import collections

infilename = "2009-obama.txt"
testingFile = "testing.txt"
trainingFile = "training.txt"
infiledata = open(infilename).read()
trainingData = open(trainingFile).read()
testingData = open(testingFile).read()

model = {}
tagToTagModel = {}
tagToWordModel = {}

tagToTagProb = {}
tagToWordProb = {}
startSentenceList = {}
tagsAndMs = {}
totalSentences = 0

correctGuesses = 0
totalGuesses = 0

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
    global tagToTagModel
    global tagToWordModel
    global totalSentences
    global startSentenceList
    global tagsAndMs
    for line in trainingData.splitlines():
        context = ['']
        firstWord = True
        for wordWithTag in line.split():
            word = (wordWithTag.split("_")[0]).lower()
            tag = wordWithTag.split("_")[1]
            tagsAndMs[tag] = 0
            if firstWord:
                startSentenceList[tag] = startSentenceList.setdefault(tag, 0) + 1
                totalSentences += 1

                firstWord = False

            else:
                temp = tagToTagModel.setdefault(str(context),{})
                temp[str(tag)] = temp.get(str(tag), 0) + 1
                tagToTagModel[str(context)] = temp

            tempTwo = tagToWordModel.setdefault(str(tag),{})
            tempTwo[str(word)] = tempTwo.get(str(word), 0) + 1
            tagToWordModel[str(tag)] = tempTwo

            # context = (context+[word])[1:]
            context = tag

    for key, value in startSentenceList.items():
        startSentenceList[key] = value/totalSentences
    tagToTagModel = generateProp(tagToTagModel)
    tagToWordModel = generateProp(tagToWordModel)
    # tagsAndMs = set(listofTags)

def getTagFromLine(line):
    lineDic = collections.OrderedDict()
    for wordWithTag in line.split():
        word = (wordWithTag.split("_")[0]).lower()
        tag = wordWithTag.split("_")[1]
        lineDic[word] = tag
    return lineDic

def useTestData():
    global correctGuesses
    global totalGuesses
    for line in testingData.splitlines():
        dic = getTagFromLine(line)
        isFirstWord = True
        items = list(dic.items())
        firstWord = items[0][0]
        maxMTag = initCalcM(firstWord)
        if maxMTag == items[0][1]:
            correctGuesses += 1
        totalGuesses += 1
        for word, realTag in dic.items():
            if isFirstWord:
                isFirstWord = False
                continue
            currentMaxM = 0
            currentMaxTag = ""
            for outerTags in tagsAndMs:
                probWordGivenTag = tagToWordModel.get(outerTags).get(word, 0)
                currentInnerMaxM = 0
                currentInnerMaxTag = ""
                for innerTag in tagsAndMs:
                    innerTagModel = tagToTagModel.get(innerTag)
                    probTagToTag = innerTagModel.get(outerTags, 0)
                    innerTagM = tagsAndMs[innerTag]

                    newInnerM = probTagToTag * innerTagM
                    if newInnerM > currentInnerMaxM:
                        currentInnerMaxM = newInnerM
                        currentInnerMaxTag = innerTag
                newM = probWordGivenTag*currentInnerMaxM
                tagsAndMs[outerTags] = newM
                if newM > currentMaxM:
                    currentMaxM = newM
                    currentMaxTag = outerTags
            if currentMaxTag == "":
                currentMaxTag = "NN"
            # print(currentMaxTag, ":", realTag)
            if currentMaxTag == realTag:
                correctGuesses += 1
            totalGuesses += 1

            # print(word)
    print(correctGuesses/totalGuesses)

def initCalcM(word):
    maxM = 0
    maxTag = ""
    for tag in tagsAndMs:
        if tag in startSentenceList:
            startProb = startSentenceList[tag]
            wordListProb = tagToWordModel.get(tag)
            wordProb = wordListProb.get(word, 0)
            newM = startProb*wordProb
            tagsAndMs[tag] = newM
            if newM > maxM:
                maxM = newM
                maxTag = tag
        else:
            tagsAndMs[tag] = 0.000000001
    return maxTag

getWordList([''])
# generateSenteces([''])
trainOnData()
useTestData()