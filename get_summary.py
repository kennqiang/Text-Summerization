import codecs
import os
import math
import shutil
import tf_idf
import re
import operator

def readtxt(path):
    with codecs.open(path,"r",encoding="utf-8") as f:
        content = f.read().strip()
    return content

def tfidf(path):
    word_tfidf={}
    f=open(path,'r',encoding="utf-8")
    for line in f:
        word=line.split(':')[0]
        tfidf=line.split(':')[1]
        word_tfidf[word]=tfidf
    f.close()
    return word_tfidf

def get_summury(path1,content):
    word_tfidf=tfidf(path1)
    sentence_score={}
    sentence_list=content.split('\n\n')
    del_word=tf_idf.get_stop_words('stop_words_eng.txt')
    for s in sentence_list:
        # print(s)
        sentence_score[s]=0
        word_list=re.split('\s',s)
        new_word_list=[]
        for word in word_list:
            new_word_list.append(re.sub("[\.\,\'\"\:]",'',word))
        for w in new_word_list:
            if w not in del_word and w is not '':
                sentence_score[s]+=float(word_tfidf[w])
    result=sorted(sentence_score.items(),reverse=True,key=operator.itemgetter(1))
    print('======================')
    print('The summary:')
    print(result[0][0])
    return result[0][0]


def main():
    filefolder=r"news"
    files_array=tf_idf.funfolder(filefolder)
    new_folder = r"tfidf_summary1"
    tf_idf.buildfolder(new_folder)
    for file in files_array:
        filename=file.split('//')[1].split('.')[0]
        print(filename)
        tfidf_path='tfidf_result//'+filename+'.story_tfidf.txt'
        # print(tfidf_path)
        content=tf_idf.readtxt(file)
        summary=get_summury(tfidf_path,content)
        #创建新文件夹，用来存放通过tfidf方法获得的抽取式摘要
        summary_path='tfidf_summary1//'+filename+'.txt'
        file=codecs.open(summary_path,"a",encoding="utf-8")
        file.write(summary)

if __name__ == '__main__':
    main()