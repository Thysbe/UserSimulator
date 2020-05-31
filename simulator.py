from userManager import UserManager
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import numpy
import sys
import nltk
nltk.download('stopwords')


def simulateUser(messages):
    corpus = tokenizeMessages(messages)
    return "Hello " + corpus

# takes an array of strings


def tokenizeMessages(messages):
    corpus = ""
    for message in messages:
        corpus = corpus + message + " "
    corpus = corpus.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(corpus)
    filtered = filter(lambda token: token not in stopwords.words(
        'english'), tokens)  # maybe we should remove this
    return " ".join(filtered)


def convert_chars(corpus):
    chars = sorted(list(set(corpus)))
    char_to_num = dict((c, i) for i, c in enumerate(chars))
    input_len = len(corpus)
    vocab_len = len(chars)
    return ""
