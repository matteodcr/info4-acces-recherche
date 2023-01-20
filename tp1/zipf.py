from operator import itemgetter  
from math import log


def zipf():
    N = 3204
    M = 0
    dico = {}
    prime_dico = {}
    
    for i in range(1,N):
        sous_dico = {}
        prime_dico["CACM-"+str(i)+".tok"] = sous_dico
        src = open("collection_tokens/CACM-"+str(i)+".tok", "r")

        for line in src:
            if line.strip() in dico:
                dico[line.strip()] += 1
                
            else:
                dico[line.strip()] = 1

            if line.strip() in sous_dico:
                sous_dico[line.strip()] += 1

            else:
                sous_dico[line.strip()] = 1

            M += 1

        src.close
    
    My = len(dico)
    print("My = " + str(My)) # sans doute erreur
    print("Lambda = " + str((M/log(My))))
    print("Voici les 10 mots les plus fréquents et leur occurence : ")
    i=0;
    for e in reversed(sorted(dico.items(), key = itemgetter(1))):
        i+=1
        if i==11:
            break
        print(e)


zipf()