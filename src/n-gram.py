import random

infilename = "2009-obama.txt"
trainingdata = open(infilename).read()

contextconst = [""]

context = contextconst
model = {}

for word in trainingdata.split():
    #print (word)
    model[str(context)] = model.setdefault(str(context),[])+ [word]
    context = (context+[word])[1:]

#print(model)

context = contextconst
for i in range(100):
    word = random.choice(model[str(context)])
    print(word,end=" ")
    context = (context+[word])[1:]

print()