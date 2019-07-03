import pymysql
import pandas as pd

class Mysql():
    def __init__(self):

        self.config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'passwd': 'root',
            'charset':'utf8mb4',
            'database':'jods-data'
            }

    def connect(self):
        db = pymysql.connect(**self.config)
        cursor = db.cursor()
        return db,cursor


    def control(self,db,cursor):

        sql1 = "CREATE DATABASE job_info"  #====>创建数据库ok
        #sql="drop database job_info"  #====>删除数据库OK
        # cursor.execute(sql1)
        # db.commit()
        self.commit(db,cursor,sql1)

        sql2="use job_info"
        self.commit(db,cursor,sql2)

        sql3="CREATE TABLE jobdata(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT ," \
            "city VARCHAR(255) NOT NULL DEFAULT ''  ," \
            "company_name VARCHAR(255) NOT NULL DEFAULT '' ," \
            "education VARCHAR(255) NOT NULL DEFAULT '' ," \
            "name VARCHAR(255) NOT NULL DEFAULT '' ," \
            "salary VARCHAR(255) NOT NULL DEFAULT '' ," \
            "workyears VARCHAR(255) NOT NULL DEFAULT '' ," \
            "detail VARCHAR(255) NOT NULL DEFAULT '') charset=utf8 "

        self.commit(db,cursor,sql3)

        print('success')
        self.close_db(db,cursor)

    def commit(self,db,cursor,sql):
        cursor.execute(sql)
        db.commit()

    def close_db(self,db,cursor):
        cursor.close()
        db.close()

if __name__ == '__main__':
    mysql=Mysql()
    db,cursor=mysql.connect()
    mysql.control(db,cursor)