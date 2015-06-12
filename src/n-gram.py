import random

infilename = "2009-obama.txt"
testingFile = "testing.txt"
trainingFile = "training.txt"
infiledata = open(infilename).read()

contextconst = [""]
model = {}

def chooseWord(wordDictionary):
    total = 0
    probabilities = {}
    for word in wordDictionary:
        total += wordDictionary.get(word)
        probabilities[word] = (wordDictionary.get(word)/total) * 100
    guess = random.random()
    runningTotal = 0;
    for word in probabilities:
        prob = probabilities.get(word)
        runningTotal += prob
        if runningTotal > guess:
            return word

    return "ERROR"

def getWordList(context):
    for word in infiledata.split():
        word = word.lower()
        temp = model.setdefault(str(context),{})
        temp[str(word)] = temp.get(str(word), 0) + 1
        model[str(context)] = temp
        context = (context+[word])[1:]


def generateSenteces(context):
    context = contextconst
    for i in range(100):
        word = chooseWord(model[str(context)])
        print(word,end=" ")
        context = (context+[word])[1:]

    print()



context = contextconst

getWordList([''])
context = contextconst
generateSenteces([''])