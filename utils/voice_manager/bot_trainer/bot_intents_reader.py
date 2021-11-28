import nltk
import yaml
from nltk.stem import WordNetLemmatizer

from utils.misc.logging import logger


class BotIntentsReader:
    def __init__(self, file_path: str, **kwargs):
        tokenize_func = kwargs.pop('tokenize_func', nltk.word_tokenize)
        self.lemmatizer = kwargs.pop('lemmatizer', WordNetLemmatizer().lemmatize)
        log_info = kwargs.pop('log_info', False)
        self.intents = None
        self.words = []
        self.classes = []
        self.documents = []

        nltk.download('punkt')
        nltk.download('wordnet')

        self.read_yml(file_path)
        self.add_intents(tokenize_func)
        self.lemmatize_words(self.lemmatizer)

        if log_info:
            self.log_info()

    def read_yml(self, file_path: str):
        with open(file_path, 'rb') as stream:
            docs = yaml.safe_load(stream)
            self.intents = docs['intents']

    def add_intents(self, tokenize_func):
        for intent in self.intents:
            for pattern in intent['patterns']:
                token_pattern = tokenize_func(pattern)
                self.words.extend(token_pattern)
                self.documents.append((token_pattern, intent['tag']))

                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

    def lemmatize_words(self, lemmatizer):
        ignore_words = ['?', '!']
        self.words = [lemmatizer(w.lower()) for w in self.words if w not in ignore_words]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))

    def log_info(self):
        logger.info(f'{len(self.documents)} documents')
        logger.info(f'{len(self.classes)} classes {self.classes}')
        logger.info(f'{len(self.words)} unique lemmatized words {self.words}')
