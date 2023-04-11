import os

from nltk.tokenize import RegexpTokenizer

from config import EXTRACTED_DATA_PATH, TOKENIZER_REGEXP, TOKENIZED_DATA_PATH


def tokenizer():
    if not os.path.exists(TOKENIZED_DATA_PATH):
        os.makedirs(TOKENIZED_DATA_PATH)
    for filename in sorted(os.listdir(EXTRACTED_DATA_PATH)):
        src = open(EXTRACTED_DATA_PATH + filename, "r")
        content = src.read()
        name_list = RegexpTokenizer(TOKENIZER_REGEXP).tokenize(content)
        src.close()

        dst = open(TOKENIZED_DATA_PATH + filename + ".tok", "w+")
        for word in name_list:
            dst.write(str(word).lower() + "\n")
        dst.close()


tokenizer()
