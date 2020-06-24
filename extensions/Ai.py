import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import tensorflow
import numpy,tflearn,random,json,pickle,os

dst = os.path.join(str(os.getcwd()),'Data/ai')
picklepath = os.path.join(dst,'data.pickle')
modelpath = os.path.join(dst,'model.tflearn')
intentpath = os.path.join(dst,'intents.json')

with open(intentpath) as file:
    data = json.load(file)


try:
    with open(picklepath,"rb") as f:
        words,labels,training,output = pickle.load(f)

    print("Data retrieved")

except Exception as err:
    print(err)
    words = []
    labels = []
    docsx = []
    docsy = []

    for intent in data["intents"]:

        for pattern in intent["patterns"]:
            wrds=nltk.word_tokenize(pattern)
            words.extend(wrds)
            docsx.append(wrds)
            docsy.append(intent["tag"])
            
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x,doc in enumerate(docsx):

        bag = []
        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docsy[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open(picklepath,"wb") as f:
        pickle.dump((words,labels,training,output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load(modelpath)
    print("model loaded")
except:
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=2000, batch_size=8, show_metric=True)
    model.save(modelpath)


def bag_words(s,words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.wordpunct_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i,w in enumerate(words):

            if w == se:
                bag[i] = 1

        return numpy.array(bag)

def getrep(inp):

    print("user input: "+inp)

    res = model.predict([bag_words(inp,words)])

    res_index = numpy.argmax(res)
    tag = labels[res_index]
         
    for tg in data["intents"]:
        if tg["tag"] == tag:
            rep = tg["responses"]
    
    print("Predicted Input type: "+tag)
    rep = random.choice(rep)

    print("Aprropriate response: "+rep+"\n")
        
    return rep 

import discord
from discord.ext import commands

class Chatbot(commands.Cog,name="Ai"):

    def __init__(self,client):
        self.client = client

    @commands.command()
    async def ask(self,ctx,*,inp):

        inpu = "".join(inp)

        rep = getrep(inpu)

        await ctx.send(rep)

def setup(client):
    client.add_cog(Chatbot(client))
        
