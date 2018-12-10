
import jieba
import pandas as pd
import sqlite3
import re
from pyecharts import WordCloud


con = sqlite3.connect(r'E:\python资料\课程\数据分析\Job\db.sqlite3')
df = pd.read_sql('select * from app_jobs',con=con)
# print(df)
import pymongo
client = pymongo.MongoClient('localhost', port=27017)
db = client.jobword
coll = db.content


def stopwordslist():
    stopword = [line.strip() for line in open('stopwords', 'r', encoding='utf-8').readlines()]
    return stopword



def wordcould():
    a = coll.find()
    key_list = []
    count_list = []
    for i in a:
        # if i['_id'] not in stopwordslist():
        key_list.append(i['_id'])
        count_list.append(i['count'])

    wd = WordCloud(width=1200,height=600)
    wd.add('', key_list, count_list, word_size_range=(20, 100))
    return wd


def qieci():
    content = df['job_des'].tolist()
    # print(content)
    for i in content:
        for j in jieba.cut(i):
            # print(j)
            if j not in stopwordslist() and j.strip():
                print(j)
                result_find = coll.find_one({'_id':j})
                # print(result_find)
                if result_find:
                    count = result_find['count'] + 1
                    data_update = {'count':count}
                    coll.update({'_id':j},{'$set':data_update},upsert=True)
                else:
                    data = {"_id": j,'count':1}
                    coll.insert(data)
# qieci()
wordcould()