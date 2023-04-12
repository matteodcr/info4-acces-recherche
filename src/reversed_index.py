import json
import os
from math import log, sqrt

from nltk import PorterStemmer
from tqdm import tqdm

from config import *


def build_detailed_vocab():
    vocab = json.load(open(JSON_PATH + SIMPLE_VOCABULARY_NAME))
    doc_vocab = json.load(open(JSON_PATH + SIMPLE_DOC_VOCABULARY_NAME))
    file_list = os.listdir(TOKENIZED_DATA_PATH)

    for key in tqdm(vocab, desc="BUILDING DETAILED VOCABULARY"):
        tmp = {"occurences": vocab[key], "idfi": 0}
        for key_doc in doc_vocab:
            for key_word in doc_vocab[key_doc]['liste']:
                if key_word == key:
                    tmp["idfi"] += 1
        vocab[key] = tmp
        if tmp != 0:
            vocab[key]["idfi"] = log(len(file_list) / tmp["idfi"])

    json_file = open(JSON_PATH + VOCABULARY_NAME, "w")
    json_file.write(json.dumps(vocab, indent=4))


def build_doc_vocab():
    doc_vocab = {}
    if not os.path.exists(TOKENIZED_DATA_PATH):
        os.makedirs(TOKENIZED_DATA_PATH)
    file_list = os.listdir(TOKENIZED_DATA_PATH)
    stemmer = PorterStemmer()

    with tqdm(total=len(file_list), desc="BUILDING DOCUMENT VOCABULARY") as progress:
        for filename in file_list:
            tmp = {}
            src = open(os.path.join(TOKENIZED_DATA_PATH, filename), "r")

            for line in src:
                racine = stemmer.stem(line.strip())

                if racine in tmp:
                    tmp[racine] += 1

                else:
                    tmp[racine] = 1

            doc_vocab[filename.split(".")[0]] = {'norme': 0, 'liste': tmp}
            src.close()
            progress.update(1)

    with open(os.path.join(JSON_PATH, SIMPLE_DOC_VOCABULARY_NAME), "w") as json_file:
        json.dump(doc_vocab, json_file, indent=4)


def build_detailed_doc_vocab():
    vocab = json.load(open(JSON_PATH + VOCABULARY_NAME))
    doc_vocab = json.load(open(JSON_PATH + SIMPLE_DOC_VOCABULARY_NAME))

    for doc in tqdm(doc_vocab, desc='BUILDING DETAILED DOCUMENT VOCABULARY'):
        tmp = 0
        for word in doc_vocab[doc]['liste']:
            doc_vocab[doc]['liste'][word] = doc_vocab[doc]['liste'][word] * vocab[word]["idfi"]
            tmp += doc_vocab[doc]['liste'][word] ** 2
        doc_vocab[doc]['norme'] = sqrt(tmp)

    json_file2 = open(JSON_PATH + DOC_VOCABULARY_NAME, "w")
    json_file2.write(json.dumps(doc_vocab, indent=4))


def build_reverse_index():
    doc_vocab = json.load(open(JSON_PATH + DOC_VOCABULARY_NAME))
    global_vocab = json.load(open(JSON_PATH + VOCABULARY_NAME))
    reversed_index = {}

    for word in tqdm(global_vocab, desc="BUILDING REVERSED INDEX"):
        tmp = {}
        for doc in doc_vocab:
            for doc_word in doc_vocab[doc]['liste']:
                if doc_word == word:
                    tmp[doc] = doc_vocab[doc]['liste'][doc_word]
        reversed_index[word] = tmp

    open(JSON_PATH + REVERSED_INDEX_NAME, "w+").write(json.dumps(reversed_index, indent=4))
    return reversed_index
