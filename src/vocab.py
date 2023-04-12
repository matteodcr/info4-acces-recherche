import json
import os
from math import log
from operator import itemgetter

from nltk.stem.porter import *
from tqdm import tqdm

from config import JSON_PATH, SIMPLE_VOCABULARY_NAME, TOKENIZED_DATA_PATH


def build_vocab():
    file_list = os.listdir(TOKENIZED_DATA_PATH)
    stemmer = PorterStemmer()
    vocab = {}
    vocab_size = 0
    my = 0
    for filename in tqdm(file_list, desc="BUILDING VOCABULARY"):
        src = open(TOKENIZED_DATA_PATH + filename, "r")
        for line in src:
            racine = stemmer.stem(line.strip())
            if racine in vocab:
                vocab[racine] += 1
            else:
                vocab[racine] = 1
            vocab_size = vocab_size + 1
        src.close()

    my = len(vocab)
    open(JSON_PATH + SIMPLE_VOCABULARY_NAME, "w+").write(json.dumps(vocab, indent=4))
    return my, vocab_size


def print_vocab_details(my, vocab_size):
    vocab = json.load(open(JSON_PATH + SIMPLE_VOCABULARY_NAME))

    print("My = ", str(my))
    zipf_lambda = str((vocab_size / log(my)))
    print("Lambda = ", zipf_lambda)
    print("Voici les 10 mots les plus fréquents et leur occurence : ")
    i = 0
    for e in reversed(sorted(vocab.items(), key=itemgetter(1))):
        i += 1
        if i == 11:
            break
        print(e)

    return zipf_lambda, vocab_size
