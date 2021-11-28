import json
import pickle
import random

import nltk
import numpy as np
from tensorflow.keras.models import load_model


class BotLoader:
    def __init__(self, bot_model, threshold=0.25):
        self.threshold = threshold
        if isinstance(bot_model, dict):
            self.lemmatizer = pickle.load(open(bot_model["lemmatizer"], 'rb'))
            self.model = load_model(bot_model['model'])
            self.intents = json.loads(open(bot_model['intents'], 'r').read())
            self.words = pickle.load(open(bot_model['words'], 'rb'))
            self.classes = pickle.load(open(bot_model['classes'], 'rb'))
        else:
            self.model = bot_model.model
            self.intents = bot_model.intents
            self.words = bot_model.words
            self.classes = bot_model.classes
            self.lemmatizer = bot_model.lemmatizer

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer(word.lower()) for word in sentence_words]
        return sentence_words

    def bow(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)

        for s in sentence_words:
            for i, w in enumerate(self.words):
                if w == s:
                    bag[i] = 1

        return np.array(bag)

    def predict_class(self, sentence):
        tokens = self.bow(sentence)

        if tokens.sum() > 0:
            predictions = self.model.predict(np.array([tokens]))[0]
            results = [[i, r] for i, r in enumerate(predictions) if r > self.threshold]
            results.sort(key=lambda x: x[1], reverse=True)

            return_list = []
            for result in results:
                return_list.append({"intent": self.classes[result[0]], "probability": str(result[1])})

        else:
            return_list = None

        return return_list

    def get_response(self, ints):
        tag = ints[0]['intent']

        result = None
        for i in self.intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break

        return result

    def chatbot_response(self, msg):
        ints = self.predict_class(msg)
        if ints is not None:
            res = self.get_response(ints)
        else:
            res = "I don't understand you, can you repeat"
        return res
