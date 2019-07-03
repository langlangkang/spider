import pandas as pd
from pyecharts import Pie
import os
'''
#对salary进行分析
'''
#一开始数据
RAW_DATA_FILE = './image/job_data.csv'
#清理后的数据
CLN_DATA_FILE = './image/data.csv'
class ShowJodSalary(object):
    if os.path.exists(CLN_DATA_FILE):
        print('注意注意：文件夹目录下已有数据,准备覆盖......')
        cln_data = pd.read_csv(CLN_DATA_FILE)

    def show_jod_salary(self,cln_data):
        self.cln_data=cln_data
        data = self.cln_data['salary']

        data = data.dropna()  # 去空值

        new_data = [] #列表
        for i in data:
            a = i[:]
            new_data.append(a) #添加
        #print(new_data)
        juzhi_data=[]
        print('-' * 150)
        print('正在分析薪资。。。。。。')
        for i in new_data:
            print(i)
            try:            #防止没有出现年单位
                if i[-1] =='年':
                    if i[-3] == '千':
                        g=self.fangfa3(i)
                        juzhi_data.append(g)
                    elif i[-3] == '万':
                        g=self.fangfa4(i)
                        juzhi_data.append(g)
                    else:
                        continue
                elif i[-1] == '月':
                    if i[-3] == '千':
                        g=self.fangfa2(i)
                        juzhi_data.append(g)
                    elif i[-3] == '万':
                        g=self.fangfa1(i)
                        juzhi_data.append(g)
                    else:
                        continue
            except Exception as e:
                print('影响不大:',e)

        #print('juzhi_data:',juzhi_data)
        two=0 #0-2000
        three=0
        four=0 #2000-4000
        five=0
        six=0 #4000-6000
        seven=0
        eight=0 #6000-8000
        nine=0
        ten=0 #8000-10000
        qita=0 #10000以上

        for i in juzhi_data:
            if 0.0<= i < 2.0:
                two+=1
            elif 2.0<= i < 3.0:
                three+=1
            elif 3.0<= i < 4.0:
                four+=1
            elif 4.0 <= i < 5.0:
                five += 1
            elif 5.0 <= i < 6.0:
                six += 1
            elif 6.0<= i < 7.0:
                seven+=1
            elif 7.0<= i < 8.0:
                eight+=1
            elif 8.0<= i < 9.0:
                nine+=1
            elif 9.0<= i < 10.0:
                ten+=1
            else:
                qita+=1


        attr=['0-2000','2000-3000','3000-4000','4000-5000','5000-6000','6000-7000','7000-8000','8000-9000','9000-10000','10000以上']
        v1=[two,three,four,five,six,seven,eight,nine,ten,qita]
        pie=Pie('薪资分布分析  (元/月)',title_pos= 'center',width=900) #参数
        pie.add('薪资',attr,v1,center=[35,60],is_random=True,radius=[25,75],rosetype='area',is_legend_show=False,is_label_show=True)
        pie.render('./image/pie.html') #画图
        print('分析完毕。。。。。。')

    # 自己定义的方法
    def fangfa1(self,i):
        # a = '0.3-0.5万/月'
        b = i.split('/') #==>['0.3-0.5万','月']
        c = b[0][:-1] #==>['0.3-0.5']
        d = c.split('-') #==>['0.3','0.5']
        e = float(d[0]) * 10  #==>3.0
        f = float(d[1]) * 10  #==>5.0
        g = (e + f) / 2 #==>4.0
        #print(e,f,'千/月','均值为',g,'千/月')
        return g
    # 自己定义的方法
    def fangfa2(self,i):
        # a = '6-8千/月'
        b = i.split('/') #==>['6-8千','月']
        c = b[0][:-1] #==>['6-8']
        d = c.split('-') #==>['6','8']
        e = float(d[0])   #==>6.0
        f = float(d[1])   #==>8.0
        g = (e + f) / 2  # ==>7.0
        #print(e, f, '千/月', '均值为', g,'千/月')
        return g
    # 自己定义的方法
    def fangfa3(self,i):
        # a = '6-8千/年'
        b = i.split('/') #==>['6-8千','年']
        c = b[0][:-1] #==>['6-8']
        d = c.split('-') #==>['6','8']
        e = float(d[0])/12   #==>6.0
        f = float(d[1])/12  #==>8.0
        g = (e + f) / 2  # ==>7.0
        #print(e, f, '千/月', '均值为', g,'千/月')
        return g
    #自己定义的方法
    def fangfa4(self,i):
        # a = '6-8万/年'
        b = i.split('/') #==>['6-8万','年']
        c = b[0][:-1] #==>['6-8']
        d = c.split('-') #==>['6','8']
        e = float(d[0])*10/12   #==>6.0
        f = float(d[1])*10/12  #==>8.0
        g = (e + f) / 2  # ==>7.0
        #print(e, f, '千/月', '均值为', g,'千/月')
        return g
