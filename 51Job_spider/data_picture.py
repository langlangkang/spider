'''
数据可视化
'''
import os
import numpy as np
import pandas as pd
import matplotlib
from pyecharts import Bar
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
from pyecharts import Pie

#一开始数据
RAW_DATA_FILE = './image/job_data.csv'
#清理后的数据
CLN_DATA_FILE = './image/data.csv'

class DataPicture(object):

    # 数据可视化
    def show_job_location(self,cln_data):
        '''
        对address进行分析
        '''
        data = cln_data['address']

        novelList = []
        for i in data:
            words = (i[:2])
            # print(words)
            novelList.append(words)

        # 统计出词频字典
        novelSet = set(novelList)
        novelDict = {}
        for word in novelSet:
            novelDict[word] = novelList.count(word)

        # 对词频进行排序
        novelListSorted = list(novelDict.items())
        novelListSorted.sort(key=lambda e: e[1], reverse=True)

        # 打印前20的词频
        topWordNum = 0
        data_list = []
        for topWordTup in novelListSorted:
            if topWordNum == 20:
                break
            # print(topWordTup)
            data_list.append(list(topWordTup))
            topWordNum += 1

        print('-' * 150)
        print('前20的词频:',data_list)
        print('-' * 150)

        data = [i[0] for i in data_list]
        bins = [i[1] for i in data_list]

        # 可视化结果
        bar = Bar("job位置分布", "前程无忧手机端")
        bar.add("需求", data, bins, is_more_utils=True)
        bar.render('./image/job位置分布.html')

    def show_job_education(self):
        '''
        #对education进行分析
        '''
        cln_data = pd.read_csv(CLN_DATA_FILE)

        #print(cln_data['education'])
        #print('*'*150)

        new_data = cln_data['education'] #取education值

        # 去除空记录后的数据
        data = new_data.dropna()
        #print(data)
        novelList = []
        for i in data:
            words = (i[:2])
            # print(words)
            novelList.append(words)

        # 统计出词频字典
        novelSet = set(novelList)
        novelDict = {}
        for word in novelSet:
            novelDict[word] = novelList.count(word)

        # 对词频进行排序
        novelListSorted = list(novelDict.items())
        novelListSorted.sort(key=lambda e: e[1], reverse=True)

        # 打印前4的词频
        topWordNum = 0
        data_list = []
        for topWordTup in novelListSorted:
            if topWordNum == 4:
                break
            # print(topWordTup)
            data_list.append(list(topWordTup))
            topWordNum += 1

        print('词频:',data_list)
        print('-' * 150)

        data = [i[0] for i in data_list]
        bins = [i[1] for i in data_list]

        # 可视化结果
        bar = Bar("job教育情况", "前程无忧手机端")
        bar.add("需求", data, bins, is_more_utils=True)
        bar.render('./image/job教育情况.html')

    def show_job_experience(self):
        '''
        饼形图
        '''
        cln_data = pd.read_csv(CLN_DATA_FILE)
        data = cln_data['experience'] #取experience值
        #print(data)
        data = data.dropna()  #去空值
        #print('-' * 150)
        print('experience:',data)

        new_data = []
        for i in data:
            a = i[:-4]
            new_data.append(a)
        #print(new_data)
        one_year = 0 #初始值
        two_year = 0 #初始值
        wu = 0 #初始值
        qi_ta = 0 #初始值
        for i in new_data:
            if i == '1年':
                one_year += 1
            elif i == '2年':
                two_year += 1
            elif i == '无':
                wu += 1
            else:
                qi_ta += 1

        print('-' * 150)
        print('1年工作经验:', one_year)
        print('2年工作经验:', two_year)
        print('无工作经验:', wu)
        print('更多工作经验:', qi_ta)
        print('-' * 150)

        # 让饼状图添加的中文不会出现卡框框
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']

        labels = '1年工作经验', '2年工作经验', '无工作经验', '更多工作经验'
        fracs = [one_year, two_year, wu, qi_ta]
        explode = [0.1, 0.05, 0.15, 0.2]  # 凸出这部分，
        plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
        # autopct ，show percet
        plt.pie(x=fracs, labels=labels, explode=explode, autopct='%3.1f %%',
                shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6)

        '''
        参数详情：
        labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
        autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
        shadow，饼是否有阴影
        startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
        pctdistance，百分比的text离圆心的距离
        patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
        '''
        #show饼状图
        plt.show()

    def show_jod_duty(self,cln_data):

        data = cln_data['duty']  # 取duty值
        data = data.dropna()  # 去空值
        newdata = []
        for i in data:
            newdata.append(i)
        newdata = str(newdata)
        #保存词
        with open('./image/duty_data.txt', 'w', encoding='utf-8') as f:
            f.write(newdata)

        print('在根目录下保存了词。。。。。。')
        print('-' * 150)
        # 1.读出词
        text = open('./image/duty_data.txt', 'r', encoding='utf-8').read()
        # 2.把词剪开
        cut_text = jieba.cut(text)
        # 3.以空格拼接起来
        result = " ".join(cut_text)

        # 4.生成词云
        wc = WordCloud(
            font_path='simhei.ttf',  # 字体路劲
            background_color='white',  # 背景颜色
            width=600,
            height=400,
            max_font_size=100,  # 字体大小
            min_font_size=20,
            mask=plt.imread('./词云图.jpg'),  # 背景图片
            max_words=2000,
            stopwords={'xa0'}  # 设置停用词
        )
        wc.generate(result)
        wc.to_file('./image/data.png')  # 图片保存

        # 5.显示图片
        plt.figure('data')  # 图片显示的名字
        plt.imshow(wc)
        plt.axis('off')  # 关闭坐标
        plt.show()

