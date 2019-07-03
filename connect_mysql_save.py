import pymysql
import pandas as pd

class Mysql():
    def __init__(self):
        '''
        host 主机
        port 端口
        user 用户
        passwd 密码
        charset  编码
        database 数据库
        '''
        self.config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'passwd': 'root',
            'charset': 'utf8mb4',
            'database': 'jods-data'
        }
        self.datas = pd.read_csv('python_analy_data.csv',encoding = 'utf-8')

    def connect(self):
        print('当前有多少条数据',len(self.datas))
        #创建db对象
        db = pymysql.connect(**self.config)
        print('connect success')

        return db

    def save(self,db):
        cursor = db.cursor()
        a = 0
        for i in self.datas.values:
            # pythonanalydata数据库  （类名） VALUES  （占位符） （数值）
            sql = "INSERT INTO pythonanalydata (id,city,company_name,education,name,salary,workyears,detail) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" % (
            int(a), i[0], i[1], i[3], i[4], i[5], i[6], i[2])
            cursor.execute(sql)
            db.commit()
            a += 1
            print('保存成功', a)

            # data = cursor.fetchall()
            # print(data)

        cursor.close()
        db.close()

if __name__ == '__main__':
    mysql=Mysql()
    db=mysql.connect()
    mysql.save(db)