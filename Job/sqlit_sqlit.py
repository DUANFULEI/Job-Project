import sqlite3


class SqliteToSqlite(object):
    def __init__(self):
        self.coon_one = sqlite3.connect(r'E:\python资料\课程\pyton爬虫\MultPageScrapy\MultPageScrapy\job.db')
        self.coon_two = sqlite3.connect(r'E:\python资料\课程\数据分析\Job\db.sqlite3')
        self.cursor_one = self.coon_one.cursor()
        self.cursor_two = self.coon_two.cursor()

    def run(self):
        a = self.cursor_one.execute('select * from jobs')
        for i in a:
            print(i[0])
            try :
                p = i[0].split('-')
                pay_a = p[0].rstrip('K')
                pay_b = p[1].rstrip('K')
            except Exception as e:
                pay_a = -1
                pay_b = -1

            sql_insert = """ insert into app_jobs(position,company,pay_a,pay_b,address,job_term,job_des) values(?,?,?,?,?,?,?) """
            param = (i[1], i[2],pay_a,pay_b,i[5], i[3], i[4])
            self.coon_two.execute(sql_insert,param)
            # self.coon_two.execute(
            #     "insert into app_jobs(position,company,pay,address,job_term,job_des) values('{}','{}','{}','{}','{}','{}') ".format(i[1], i[2], i[0], i[5], i[3], i[4]))
        self.coon_two.commit()
        self.coon_one.close()
        self.coon_two.close()

a = SqliteToSqlite()
a.run()



