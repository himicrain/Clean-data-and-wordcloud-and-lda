#!/usr/bin/env python2
# coding=utf-8

import Clean
from collections import Counter
import time
import utils
from wordcloud import WordCloud
import matplotlib.pyplot as plt

start = time.time()
stop_words = Clean.stop_words
temp = [x.encode('utf-8') for x in stop_words]
stop_words = temp

def generate_word_cloud(text,N=50):

    cloud = WordCloud(width=800,height=400,max_words=N,background_color='white',scale=1.5,random_state=42,stopwords=stop_words,prefer_horizontal=0.8,margin=4)
    frequency = Counter(text.split(utils.Sign))
    cloud.generate_from_frequencies(dict(frequency))

    plt.imshow(cloud)
    plt.axis('off')
    plt.show()

def main(Dir,file):
    path = utils.generate_str_file(Dir,file)
    f = open(path)
    text = f.read(-1)
    generate_word_cloud(text,50)

if "__main__" == __name__:
    main('./csv','data new version.csv')