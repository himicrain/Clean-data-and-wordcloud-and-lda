#!/usr/bin/env python2
# coding=utf-8

import utils
import networkx as nx
import matplotlib.pyplot as plt
from nltk.metrics import *
from nltk.collocations import *
from collections import Counter

#关键字个数
NUM = 50


Sign = utils.Sign
def load_data(Dir,path):
    file_path = utils.generate_str_file(Dir,path)
    corpus = []
    for line in open(file_path, 'r'):
        # print line
        corpus.extend(line.strip().split(Sign))
    return corpus


def pmi(Dir,path):

    tokens=load_data(Dir,path)
    counter = Counter(tokens)
    top = dict(counter.most_common(NUM)).keys()
    print top
    finder=BigramCollocationFinder.from_words(tokens)
    bigram_measures=BigramAssocMeasures()

    list_pmi =  finder.score_ngrams(bigram_measures.pmi)
    res = []
    for a in list_pmi:
        aa = a[0]
        if aa[0] in top and aa[1] in top and aa[0] != aa[1]:
            res.append(a)
    res = dict(res)
    c = Counter(res).most_common(NUM)

    return c

def draw(edges):

    G = nx.Graph()  # 创建空的网络图
    plt.figure(figsize=(16,9))
    for a in edges:
        print a
        #为了显示看着舒服权重除以100
        vec = list([(a[0][0],a[0][1],a[1]/100)])
        G.add_weighted_edges_from(vec)

    nx.draw(G,pos = nx.spring_layout(G) ,node_color = 'g',edge_color = 'y',with_labels = True,font_size =13,node_size =9)

    plt.show()


if "__main__" == __name__:
    edges = pmi('./csv','data new version.csv')
    draw(edges)