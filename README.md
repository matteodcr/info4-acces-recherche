# Project - Multimedia Retrieval

Mattéo Decorsaire

## Basic Usage

```bash
$ cd src
$ python3 main.py 
```

## Options

### `-i input_path`

> Define a custom path for the cacm.all

```bash
$ python3 main.py -i ../ressources/inputs/cacm.all 
```

### `-v`

> Print My, Lambda and top 10 words by frequency

```bash
$ python3 main.py -

...
My =  7407
Lambda =  19711.49681198287
Voici les 10 mots les plus fréquents et leur occurence : 
('the', 11018)
('of', 9031)
('and', 4536)
('to', 3771)
('is', 3727)
('in', 3446)
('cacm', 3204)
('for', 3164)
('are', 1988)
('algorithm', 1867)
...
```

### `-r`

> Re-analayse the cacm.all/regenerate the cacm.all

```bash
$ python3 main.py -r
```

### `-m`

> Generate a custom Markdown report

```bash
$ python3 main.py -m
```

[Example of a report](ressources/output/2023-04-12_15-52-20.md)

We can click on filenames to open the file !
