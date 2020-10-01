import numpy as np
import tflearn
import tensorflow as tf
import random
import pickle
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer
from copy import copy
from string import punctuation

stemmer = LancasterStemmer()

with open("intents.json") as file:
    data = json.load(file)

try:
    # try to load existing data
    with open("data.pickle", "rb") as f:
        words, labels, X, y = pickle.load(f)

except:
    intents = data['intents']
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in intents:

        for pattern in intent['pattern']:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append([stemmer.stem(w) for w in wrds if w not in punctuation])
            docs_y.append(intent['tag'])

        labels.append(intent['tag'])

    words = sorted(list(set([stemmer.stem(w.lower()) for w in words if w not in punctuation])))
    labels = sorted(labels)

    X = []
    y = []

    out_empty = [0 for _ in range(len(labels))]
    print(out_empty)
    for i, doc in enumerate(docs_x):
        bow = []

        for w in words:
            if w in doc:
                bow.append(1)
            else:
                bow.append(0)

        output_row = copy(out_empty)
        output_row[labels.index(docs_y[i])] = 1

        X.append(bow)
        y.append(output_row)

    X = np.array(X)
    y = np.array(y)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, X, y), f)

# create Neural Network:
tf.reset_default_graph()

net = tflearn.input_data(shape=[None, len(X[0])])  # input
net = tflearn.fully_connected(net, 8)  # hidden layer
net = tflearn.fully_connected(net, 8)  # hidden layer
net = tflearn.fully_connected(net, len(y[0]), activation='softmax')  # output layer
net = tflearn.regression(net)

model = tflearn.DNN(net)


try:
    model.load("model.tflearn")

except:
    # train model:
    model.fit(X, y, n_epoch=2000, batch_size=8, show_metric=True)
    model.save('model.tflearn')


def bag_of_words(s, words):

    bow = np.zeros(len(words))
    w_stemmed = [stemmer.stem(w.lower()) for w in nltk.word_tokenize(s)]

    for stem in w_stemmed:
        for i, w in enumerate(words):
            if w == stem:
                bow[i] = 1

    return np.array(bow)

def chat():
    print("Start talking to Iris:")

    while True:

        inp = input("You: ")
        if inp.lower() == "quit":
            break

        res = model.predict([bag_of_words(inp, words)])
        tag = labels[np.argmax(res)]
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
        print(random.choice(responses))

chat()



