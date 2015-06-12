import random

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



infilename = "2009-obama.txt"
trainingdata = open(infilename).read()

contextconst = [""]

context = contextconst
model = {}

for word in trainingdata.split():
    #print (word)
    word = word.lower()
    temp = model.setdefault(str(context),{})
    temp[str(word)] = temp.get(str(word), 0) + 1
    model[str(context)] = temp
    context = (context+[word])[1:]

#print(model)

context = contextconst
for i in range(100):
    word = chooseWord(model[str(context)])
    print(word,end=" ")
    context = (context+[word])[1:]

print()