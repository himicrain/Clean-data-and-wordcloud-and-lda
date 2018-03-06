#!/usr/bin/env python2
# coding=utf-8
import os
import sys
import numpy as np
import lda
import matplotlib.pyplot as plt
import utils

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer

# 每个Topic 中几个关键字
Topic_words_num =  10
## 输出前N个最可能的Topic
Topics_doc_num = 10
#设置N个主题
Topic_num=5
def load_data(Dir,path):
    file_path = utils.generate_str_file(Dir,path)
    corpus = []
    for line in open(file_path, 'r'):
        # print line
        corpus.append(line.strip())
    return corpus


def draw(doc_topic):

    f, ax = plt.subplots(Topics_doc_num, 1, figsize=(8, 8), sharex=True)
    for i, k in enumerate(range(Topics_doc_num)):
        ax[i].stem(doc_topic[k, :], linefmt='r-',
                   markerfmt='ro', basefmt='w-')
        ax[i].set_xlim(-1, Topic_num+1)  # x坐标下标
        ax[i].set_ylim(0, 1.2)  # y坐标下标
        ax[i].set_ylabel("Prob")
        ax[i].set_title("Document {}".format(k))
    ax[5].set_xlabel("Topic")
    plt.tight_layout()
    plt.show()

def process(Dir,path):
    # 存储读取语料 一行预料为一个文档
    corpus = load_data(Dir,path)

    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    weight = X.toarray()

    model = lda.LDA(n_topics=Topic_num, n_iter=500, random_state=1)
    model.fit(np.asarray(weight))
    topic_word = model.topic_word_

    #所有词汇
    vocab = vectorizer.get_feature_names()

    # 文档-主题（Document-Topic）分布
    doc_topic = model.doc_topic_


    label = []
    for n in range(Topics_doc_num):
        topic_most_pr = doc_topic[n].argmax()
        label.append(topic_most_pr)
        print("doc: {} topic: {}".format(n, topic_most_pr))


    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-Topic_words_num-1:-1]
        print('*Topic {}, key words are : \n- {}'.format(i, '; '.join(topic_words)))

    #绘制图标，不用的话可以注释掉
    draw(doc_topic)

if __name__ == "__main__":
    Dir = './csv'
    path = 'data new version.csv'
    process(Dir,path)
