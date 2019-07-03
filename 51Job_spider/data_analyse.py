'''
数据分析
'''
import pandas as pd
import os

#一开始数据
RAW_DATA_FILE = './image/job_data.csv'
#清理后的数据
CLN_DATA_FILE = './image/data.csv'
#收集数据列表
total_data = []

class DataAnalyse(object):

    def inspect_data(self,cln_data):
        """
            查看数据集信息
        """
        print('数据集基本信息')
        print(cln_data.info())
        print('-' * 150)
        print('\n数据集统计信息')
        print(cln_data.describe())
        print('-' * 150)
        print('\n数据集预览')
        print(cln_data.head())
        print('-' * 150)

    def clean_data(self,raw_data):
        """
            数据清洗，包括去除空记录，去除重复记录
        """
        # 去除空记录后的数据
        non_empty_data_df = raw_data.dropna()  #去空值的数据 90
        n_empty = raw_data.shape[0] - non_empty_data_df.shape[0]  #空值 =10

        # 去重后的记录

        cln_data_df = non_empty_data_df.drop_duplicates()    #去空值的数据再去重 80
        n_repeat = non_empty_data_df.shape[0]-cln_data_df.shape[0]  # 去重复值的数据 90
        #n_duplicates = data_df.shape[0] - cln_data_df.shape[0]   #剩余数据=原来值-去重值 100-80=20
        print('原始数据共有{}条记录，清洗后的数据共有{}条有效记录。（其中空记录有{}条，重复记录有{}条。）'.format(
            raw_data.shape[0], cln_data_df.shape[0], n_empty, n_repeat))

        return cln_data_df

    def save_new_data(self,raw_data):
        cln_data=self.clean_data(raw_data)

        print('cln_data:',cln_data)
        #预览数据就打开
        self.inspect_data(cln_data)

        cln_data.to_csv(CLN_DATA_FILE, index=False, sep=',', encoding='utf-8')
        return cln_data

    def sava_raw_data(self,total_data):

        raw_data = pd.DataFrame(total_data,index=None)
        print('raw_data:',raw_data)
        raw_data.to_csv(RAW_DATA_FILE, index=False, sep=',', encoding='utf-8')

        return raw_data

    def collect_data(self,data):
        if data is None:
            return
        #total_data = []
        total_data.append(data)   # 把数据加入到集合中

        return total_data