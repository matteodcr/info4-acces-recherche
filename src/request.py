import json
import os
import socket
from datetime import datetime
from math import sqrt

from nltk import RegexpTokenizer

from config import JSON_PATH, EXTRACTED_DATA_PATH


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

    return partial_result, request_vector


def print_request(request, n, request_vector, markdown=True):
    i = 1
    items = reversed(sorted(request.items(), key=lambda x: x[1]))
    if markdown:
        output_dir = "../ressources/output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_filename = f"{output_dir}/{date}.md"
        with open(output_filename, "a") as f:
            f.write("# Search Report\n\n")
            f.write("Machine: " + socket.gethostname() + "\n\n")
            f.write("Time: " + date + "\n\n")

            f.write("## Request vector \n\n")

            f.write('| Key | Value |\n')
            f.write('| --- | --- |\n')
            for key, value in request_vector.items():
                f.write(f'| {key} | {value} |\n')

            f.write("\n## Results \n\n")
            f.write("\n| # | Filename | Score | Content |\n")
            f.write(
                "|:---:|:-------------:|:-------------------:|:-----------------------:|\n")
    for k, v in items:
        if i > int(n):
            break
        content = open(EXTRACTED_DATA_PATH + k, "r").read()
        if markdown:
            with open(output_filename, "a") as f:
                f.write(f"| {i} | [**{k}** ](../collection/{k})| {v} | {content[:20]}... |\n")
        else:
            print(i, k, v, " : ", content[:20] + "...")
        i += 1
    if markdown:
        print("GENERATED MARKDOWN REPORT AT " + output_filename)
