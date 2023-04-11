from nltk import RegexpTokenizer
from pyarrow import json

from config import JSON_PATH


def build_request_vector(txt):
    name_list = RegexpTokenizer("[A-Za-z]\w{1,}").tokenize(txt)

    tokenized_name_list = []
    for word in name_list:
        tokenized_name_list.append(str(word).lower())

    request_vector = {}
    for word in tokenized_name_list:
        if word in request_vector:
            request_vector[word] += 1
        else:
            request_vector[word] = 1

    return request_vector


def request(text):
    request_vector = build_request_vector(text)
    inversed_index = json.load(open(JSON_PATH + 'reversed_index.json'))
    doc_vocab = json.load(open(JSON_PATH + 'doc-vocabulaire.json'))

    print("Request vector : ", request_vector)

    partial_result = {}
    request_vector_norm = 0
    for word in request_vector:
        for word_index in inversed_index:
            if word_index == word:
                line_trav = inversed_index[word_index]
                for document in line_trav:
                    if document in partial_result:
                        partial_result[document] += (inversed_index[word_index][document] * request_vector[word])
                    else:
                        partial_result[document] = (inversed_index[word_index][document] * request_vector[word])
                break
        request_vector_norm += request_vector[word] ** 2
    request_vector_norm = sqrt(request_vector_norm)

    for document in partial_result:
        partial_result[document] = partial_result[document] / (doc_vocab[document]["norme"] * request_vector_norm)

    return partial_result


def print_request(request, n):
    i = 1
    for k, v in reversed(sorted(request.items(), key=lambda x: x[1])):
        if i > int(n):
            break
        content = open("/home/matteo/Code/info4-acces-recherche/collection/" + k, "r").read()
        print(i, k, v, " : ", content[:20] + "...")
        i += 1
