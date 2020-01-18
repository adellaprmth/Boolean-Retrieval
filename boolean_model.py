from typing import List, Set, Dict
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import os
import re

stemmer = StemmerFactory().create_stemmer()

def read_file(dir_name = 'corpus') -> (List[str], List[str]):
    filenames = os.listdir(dir_name)

    document: List[str] = []
    for f in filenames :
        text = open(f"{dir_name}/{f}", 'r').read()
        document.append(text)

    # for i in range(len(document)):
    #     parse = re.split('\W', document[i].strip())
    #     parse = [x for x in parse if len(x)>0]
    #     document[i] = set(parse)
    return document, filenames

def preprocessing(documents: List[str], with_stem = True):
    
    result = [None] * len(documents)
    for i in range(len(documents)):
        parse = re.split(r'\W', documents[i].lower().strip())
        parse = [x for x in parse if len(x)>0]
        parse = set(parse)
        if (with_stem):
            result[i] = {stemmer.stem(x) for x in parse}
        else :
            result[i] = parse
    return result

def search(documents : List[Set[str]], query: str, with_stem = True):
    
    words = re.findall(r'[\s\(]*(\w+)[\s\)]*', query)
    words = set([x for x in words if x not in ('not', 'and', 'or')])
    words = list(words)
    selected = []
    for i, doc in enumerate(documents) :
        params = {}
        memo = {}
        for word in words:
            if with_stem:
                stemmed_word = stemmer.stem(word)
                if (stemmed_word  in memo):
                    params[word] = memo[stemmed_word]
                else :
                    params[word] = stemmed_word in doc
                    memo[stemmed_word] = params[word]
            else :
                if (word in memo):
                    params[word] = memo[word]
                else :
                    params[word] = word in doc
                    memo[word] = params[word]
        res = eval(query, params)
        if res :
            selected.append(i)
    return selected
    
def main():
    documents, filenames = read_file()
    documents = preprocessing(documents)
    result = search(documents, "(kebakaran and gereja) or isis")
    for i in result:
        print(filenames[i])
main()