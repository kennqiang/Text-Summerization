#!/usr/bin/env python
# -*- coding:utf-8 -*-
import codecs
import os
import math
import shutil
import re
import time
import pickle

# 遍历文件夹，获取文件名 列表
def funfolder(path):
    filesArray = []
    for root, dirs, files in os.walk(path):  # os.walk() 方法用于通过在目录树中游走输出在目录中的文件名,向上或者向下
        for file in files:
            each_file = str(root + "//" + file)
            filesArray.append(each_file)
    return filesArray

# 读取文本文件内容
def readtxt(path):
    # with codecs.open(path, "r", encoding="utf-8") as f:
    #     content = f.read().strip()
    # return content
    f = open(path, 'r', encoding="utf-8")
    new_content = []
    for line in f:
        if "@highlight" in line:
            break
        if re.match("CNN's.*contributed to this report",line) :
            break
        line.strip()
        line = re.sub(r'\(CNN\)', '', line)
        new_content.append(line)
    strlist = "".join(new_content)
    new_contents = str(strlist)
    return new_contents

def get_stop_words(path):
    stop_words=[]
    for line in open(path,'r'):
        stop_words.append(line.strip())
    return stop_words
# 统计词频，词语字典{词：个数}
def count_word(content):
    word_dic = {}
    # word_dic=()
    words_list = re.split('\s', content)#分词
    new_word_list = []
    for word in words_list:
        new_word_list.append(re.sub("[\.\,\"\'\:]", '', word))
    # del_word = ["\r\n", "/s", " ", "/n"]  # 停用词
    del_word=get_stop_words('stop_words_eng.txt')
    for word in new_word_list:
        if word not in del_word and word is not '':
            if word in word_dic:
                word_dic[word] = word_dic[word] + 1
            else:
                word_dic[word] = 1
    return word_dic


# 计算TF-IDF
# word_dict——语料库词语词典中的每个词
# files_dict——语料库词语字典（全部）
# files_Array——文件名 列表
def count_tfidf(word_dic_per_file, word_df, files_Array):
    word_tfidf = {}
    num_files = len(files_Array)
    #遍历某一个文件中的每一个单词
    for key, value in word_dic_per_file.items():
        if key != " ":
            word_tfidf[key] = value * math.log(num_files / (word_df[key] + 1))
    # 降序排序
    values_list = sorted(word_tfidf.items(), key=lambda item: item[1], reverse=True)
    return values_list

def get_word_df(all_words_dict):
    word_df={}
    for word_dict in all_words_dict:
        for w in set(word_dict):
            if w in word_df :
                word_df[w]+=1
            else:
                word_df[w]=0
    return word_df
# 新建文件夹
def buildfolder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    print("成功创建文件夹！")


# 写入文件
def out_file(path, content_list):
    with codecs.open(path, "a", encoding="utf-8") as f:
        for content in content_list:
            f.write(str(content[0]) + ":" + str(content[1]) + "\r\n")
    print("well done!")


def main():
    # 遍历文件夹，获取文件名列表
    folder_path = r"news"
    files_array = funfolder(folder_path)
    #生成词频文件
    # all_words_dic=[]
    # start1=time.process_time()
    # num1=1
    # for file_path in files_array:
    #     file_content = readtxt(file_path)
    #     word_dic = count_word(file_content)
    #     all_words_dic.append(word_dic)
    #     print(num1)
    #     num1+=1
    # end1=time.process_time()
    # print("time1:")
    # print(end1-start1)
    #保存词表
    # pickle.dump(all_words_dic,open('dict.dat','wb'))

    all_words_dic = pickle.load(open('dict.dat', 'rb'))
    #新建文件夹，用来存储单词的文档频率信息
    new_folder=r"df_result"
    buildfolder(new_folder)
    print('新建文档频率文件夹成功！')
    start2=time.process_time()
    word_df=get_word_df(all_words_dic)
    pickle.dump(word_df,open('df_result/word_df.dat','wb'))
    end2=time.process_time()
    print('计算单词的文档频率并写入文件用时：'+str(end2-start2))

    #新建文件夹用来存储每一个文件的tf-idf信息
    new_folder = r"tfidf_result"
    buildfolder(new_folder)
    word_idf=pickle.load(open('df_result/word_df.dat','rb'))
    # 计算tf-idf,并将结果存入txt
    start4=time.process_time()
    i = 0
    for word_dict in all_words_dic:
        start3=time.process_time()
        tf_idf = count_tfidf(word_dict, word_idf, files_array)
        end3=time.process_time()
        print('新闻'+str(i)+'的tf-idf计算时间：'+str(end3-start3))
        files_path = files_array[i].split("//")
        # print(files_path)
        outfile_name = files_path[1]
        # print(outfile_name)
        out_path = r"%s//%s_tfidf.txt" % (new_folder, outfile_name)
        out_file(out_path, tf_idf)
        i = i + 1
    end4=time.process_time()
    print('完成所有文档的tf-idf计算，用时：'+str(end4-start4))


if __name__ == '__main__':
    main()