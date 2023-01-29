import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize, num, task, task_return
from  datacollect import face_check

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
global loaded
global intents_file
global data_file
global all_words
global tags
global model
global intents

all_words = []
tags = []
model = None
intents = []
loaded = False

intents_file = 'intents.json'
data_file = 'data.pth'


def load_model(intents_file, data_file):
    with open(intents_file, 'r') as json_data:
        intents = json.load(json_data)

    FILE = data_file
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    
    return all_words, tags, model, intents


def chat2_o(sentence):
    global loaded
    global intents_file
    global data_file
    global all_words, tags, model, intents
    if not loaded:
        all_words, tags, model, intents = load_model(intents_file, data_file)
        loaded = True
        
    if sentence == "quit":
        return "weak"

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if tag == "calculate":
                    number = num(sentence)
                    return str(number)
                    #print(f"{bot_name}: {number}")
                elif tag == "greeting":
                    name  = face_check()
                    return str(name) + ' ' + random.choice(intent['responses'])
                elif tag == "task":
                    task(sentence)
                    return random.choice(intent['responses'])
                elif tag == "task_return":
                    ta = task_return()
                    return str(ta)
                else:
                    #print(f"{bot_name}: {random.choice(intent['responses'])}")
                    return random.choice(intent['responses'])
    else:
        return " I do not understand..."



