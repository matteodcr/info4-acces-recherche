import os

from tqdm import tqdm


def extract_data(infile, outpath):
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    file_handler = open(infile, "r")
    debut = True
    with tqdm(desc="EXTRACTING FILES", unit=" files") as progress:
        while True:
            line = file_handler.readline()
            if not line:
                break
            if line[0:2] == '.I':
                if not debut:
                    f.close()
                debut = False
                a, b = line.split(" ")
                file_name = "CACM-" + b[:-1]
                f = open(os.path.join(outpath, file_name), "w+")
            if line[:-1] == '.T' or line[:-1] == '.A' or line[:-1] == '.W' or line[:-1] == '.B':
                out = True
                while out:
                    line = file_handler.readline()
                    if not line:
                        break
                    if line[:-1] == '.N' or line[:-1] == '.X' or line[:-1] == '.K' or line[:-1] == '.I':
                        break
                    elif line[:-1] != '.T' and line[:-1] != '.A' and line[:-1] != '.W' and line[:-1] != '.B':
                        f.write(line[:-1] + "\n")
                progress.update(1)
    file_handler.close()
