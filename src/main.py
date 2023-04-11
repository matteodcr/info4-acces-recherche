# build_vocab()
# build_doc_vocab()
# build_detailed_vocab()
# build_detailed_doc_vocab()
# build_reverse_index()
from request import request, print_request

result = request(input("Recherche :"))
n = input("Nombre de résultats max")
print_request(result, n)
