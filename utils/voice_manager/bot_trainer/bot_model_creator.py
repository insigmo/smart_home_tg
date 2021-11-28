import json
import os
import pickle
import random

import numpy as np
from tensorflow.keras.layers import (
    Dense,
    Dropout
)
from tensorflow.keras.optimizers import SGD
from tensorflow.python.keras.models import Sequential

from utils.misc.logging import logger


class BotModelCreator:
    def __init__(self, bot_data, verbose=0):
        self.verbose = verbose
        self.classes = bot_data.classes
        self.words = bot_data.words
        self.documents = bot_data.documents
        self.lemmatizer = bot_data.lemmatizer
        self.intents = bot_data.intents

        self.train_x = None
        self.train_y = None
        self.model = None

        self.order_data()
        self.creat_model()

    def order_data(self):
        training = []
        output_empty = [0] * len(self.classes)
        for doc in self.documents:
            bag = []
            pattern_words = [self.lemmatizer(word.lower()) for word in doc[0]]

            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)

            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1

            training.append([bag, output_row])
        random.shuffle(training)
        training = np.array(training, dtype="object")

        self.train_x = list(training[:, 0])
        self.train_y = list(training[:, 1])
        if self.verbose != 0:
            logger.info("Training data created {training.shape}")

    def creat_model(self):
        self.model = Sequential()
        self.model.add(Dense(32, input_shape=(len(self.train_x[0]),), activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(16, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(len(self.train_y[0]), activation='softmax'))

        sgd = SGD(learning_rate=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        if self.verbose != 0:
            logger.info("model created")

    def train_model(self):
        hist = self.model.fit(
            np.array(self.train_x), np.array(self.train_y),
            epochs=500,
            batch_size=5,
            verbose=self.verbose
        )

        return hist

    def save_models(self, out_path="training_data"):
        pickle.dump(self.words, open(os.path.join(out_path, 'words.pkl'), 'wb'))
        pickle.dump(self.classes, open(os.path.join(out_path, 'classes.pkl'), 'wb'))
        pickle.dump(self.lemmatizer, open(os.path.join(out_path, 'lemmatizer.pkl'), 'wb'))

        self.model.save(os.path.join(out_path, 'chatbot_model.h5'), self.model)
        json.dump(self.intents, open(os.path.join(out_path, 'intents.json'), 'w'))
