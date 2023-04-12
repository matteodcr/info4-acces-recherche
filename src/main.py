import getopt
import os
import sys

from config import RAW_DATA_PATH, EXTRACTED_DATA_PATH
from extract import extract_data
from request import print_request, request
from reversed_index import build_doc_vocab, build_reverse_index, build_detailed_doc_vocab, build_detailed_vocab
from tokenizer import tokenizer
from vocab import build_vocab, print_vocab_details


def main(argv):
    input_path = RAW_DATA_PATH
    is_vocab_info_print = False
    is_reset = False
    markdown = False
    opts, args = getopt.getopt(argv, "hvrmi:", ["ipath="])
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputpath>')
            sys.exit()
        elif opt in ("-i", "--inputpath"):
            input_path = arg
        elif opt in ("-v", "--vocabulary"):
            is_vocab_info_print = True
            is_reset = True
        elif opt in ("-r", "--reset"):
            is_reset = True
        elif opt in ("-m", "--markdown"):
            markdown = True

    if not os.path.exists("../ressources/json/reversed_index.json") or is_reset:
        # SETUP
        extract_data(input_path, EXTRACTED_DATA_PATH)
        n_docs = tokenizer()

        if not os.path.exists("../ressources/json/"):
            os.makedirs("../ressources/json/")

        # BUILD
        my, vocab_size = build_vocab()

        if is_vocab_info_print:
            zipf_lambda, vocab_size = print_vocab_details(my, vocab_size)

        build_doc_vocab()
        build_detailed_vocab()
        build_detailed_doc_vocab()
        build_reverse_index()

        if os.path.exists("../ressources/json/simple-doc-vocabulaire.json"):
            os.remove("../ressources/json/simple-doc-vocabulaire.json")
        if os.path.exists("../ressources/json/simple-vocabulaire.json"):
            os.remove("../ressources/json/simple-vocabulaire.json")
        print("SUCCESS")

    n = input("Max results (default: 10) : ")
    if n == "":
        n = 10
    # REQUEST
    while True:
        result, request_vector = request(input("Search : "))
        print_request(result, int(n), request_vector, markdown=markdown)


if __name__ == "__main__":
    main(sys.argv[1:])
