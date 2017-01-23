#encoding=utf-8
import json
import os
import re
import jieba
from pandas import DataFrame
import pandas as pd
import pygal
import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import image
from collections import Counter

basedir = os.path.dirname(os.path.dirname(__file__))

def jsontodataframe():
    # change data to srtucture of Dataframe
    # get current path
    path = basedir + "/results3.json"
    datas = []
    for line in open(path):
        try:
            datas.append(json.loads(line))
        except:
            continue
    frame = DataFrame(datas)

    # write string to txt, prepare for jieba
    writepath = basedir + "/seekjob/spiders/seg.txt"
    try:
        with open(writepath, "w+") as f:
            for i in frame.jobdc:
                f.write(i.encode('utf-8'))
    except:
        print "some problems occur."
    finally:
        f.close()

def cutwords():
    # do sth with jieba
    writepath = basedir + "/seekjob/spiders/seg.txt"

    try:
        w = open(basedir + "/seekjob/spiders/jiebacount.txt", 'w+')
        c = open(basedir + "/seekjob/spiders/count.json", 'w+')

        with open(writepath) as f2:

            words = list(jieba.cut(f2.read(), cut_all=False))
            # count the sequence of words
            counts = Counter(words)

            jscounts = json.dumps(counts) + '\n'
            #c.write(jscounts)
            #c.close()
            print counts.most_common(30)
            # write the word-cut list
            for word in words:
                if len(word) > 1:
                    word = word + '\n'
                    w.writelines(word.encode('utf-8'))
            w.close()
            f2.close()
    except:
        print "some problems occur."

def wordcloud():
    # Read the whole text.
    text = open(basedir + "/seekjob/spiders/jiebacount.txt").read()
    # lower max_font_size
    wordcloud = WordCloud(max_font_size=60, background_color="white", margin=5, width=400, height=400, max_words=50).generate(text)
    # The pil way (don't use matplotlib)
    image1 = wordcloud.to_image()
    image1.show()
def printsth():
    print basedir
    print dir(jieba)
if __name__ == '__main__':
    jsontodataframe()
    cutwords()
    #printsth()
    wordcloud()








