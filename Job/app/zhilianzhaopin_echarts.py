import sqlite3
import pandas as pd
from pyecharts import Pie, Bar
import numpy as np



class views(object):
    def __init__(self):
        self.coon = sqlite3.connect('db.sqlite3')
        self.df = pd.read_sql_query('select * from app_jobs',self.coon)

    def work_experience(self):
        a = list(self.df.loc[:,['job_term']].groupby(['job_term']).size())
        b =  self.df.loc[:,['job_term']].groupby(['job_term']).size().index.values
        pie = Pie("工作经验饼状视图")
        pie.add("工作年限", b,a, is_label_show=True)
        return pie

    def location(self):
        a = list(self.df[self.df['address']!=''].loc[:,['address']].groupby(['address']).size())
        b =  list(self.df[self.df['address']!=''].loc[:,['address']].groupby(['address']).size().index.values)
        num = len(a)
        for i in range(num):
            if a[num - i - 1] < 20:
                a.pop(num - i -1)
                b.pop(num - i -1)
        bar=Bar('示例')
        bar.add('',b,a,is_label_show=True,is_datazoom_show=True)
        bar.use_theme('dark')
        return bar





