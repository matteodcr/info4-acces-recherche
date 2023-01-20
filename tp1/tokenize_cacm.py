from nltk.tokenize import RegexpTokenizer

def tokenizer():
    N = 3204
    for i in range(1,N):
        src = open("collection/CACM-"+str(i))
        content = src.read()
        nameList = RegexpTokenizer('[A-Za-z]\w{1,}').tokenize(content)
        src.close

        dst = open("collection_tokens/CACM-"+str(i)+".tok", "w")
        for word in nameList:
            dst.write(word.lower()+"\n")
        dst.close

tokenizer()
    