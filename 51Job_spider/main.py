'''
author: kangkang
date: 2019/07/03
爬取51job职位信息
'''

import sys
import url_manager
import html_downloader
import html_parser
import data_analyse
import data_picture
import data_picture_pie
import time
import yuyin
import del_huancun
import os
from urllib import parse
from tools import user_agent

class SpiderMian(object):
    
    # 实例化爬虫模块
    def __init__(self):
        self.urls = url_manager.UrlManager() # url管理器
        self.downloder = html_downloader.HtmlDownloader() # 网页下载器
        self.parser = html_parser.HtmlParser() # 51JOB网页解析器
        self.dataanalyse=data_analyse.DataAnalyse() #数据分析
        self.datapicture=data_picture.DataPicture()#数据可视化
        self.datapicturepie=data_picture_pie.ShowJodSalary()#数据可视化pie
        self.yy=yuyin.YuYin() #语音播报
        #self.delect = del_huancun.DelHuancun()  #清理语音数据缓存
        self.user_agent=user_agent.Random_user_agent()  #随机请求头

    def craw(self, net_info):
        headers = self.user_agent.get_headers()  #获取随机 user_agent
        _page_total = 1 #默认参数
        currentPage = 1  #当前页
        count = 1 #默认参数
        parser = self.parser
        craw_type = net_info['type'] + '-' + net_info['keyword']    #拼接抓取分类

        if net_info['type'] == '51job' :    # 如果网站类型是51job
            search_url = net_info['url'] + '&pageno=' + str(currentPage) + '&keyword=' + net_info['keyword']    # 拼接首页查询地址

            # 下载页面源码方法 传入网址和头部
            html_content = self.downloder.download_html(search_url,headers) # 下载首页查询页面源码

            #返回51页，和网址   ===>对爬取回来的网址再进行爬取信息
            page_total, new_urls = self.parser.parse_search_page(html_content) # 分析首页查询页面，获取分页总数和职位详细的地址

            #全部网址new_urls
            self.urls.add_new_urls(new_urls)    #把职位详细的地址加入到url管理器

            #_page_total=51
            _page_total = page_total
            parser = self.parser

        #爬虫开始会播放语音
        self.yy.bofangkaishi()

        #self.urls.has_new_url()======>len(self.new_urls) != 0  也就是说，只要还有URL，就循环
        while self.urls.has_new_url():
            try:
                #urls_len剩余URL长度，new_url取出来的URL
                urls_len, new_url = self.urls.get_new_url() # 从url管理器中，获取未抓取的url
                #count=1，new_url网址
                print ("carwing for: ", count, new_url)

                html_content = self.downloder.download_html(new_url,headers) # 下载详情页源码===>返回文本内容
                #网址，页面文本内容，craw_type = net_info['type'] + '-' + net_info['keyword']
                new_data = parser.parse(new_url, html_content, craw_type) # 解析网页，获取数据===>数据在这里出

                #收集数据
                total_data=self.dataanalyse.collect_data(new_data)

                time.sleep(0.5)#限制速度

                count = count + 1
                if count > 40000:  # 如果爬到40000条数据，终止程序。
                    break
                #当前一页URL已爬取完，就跳下一页
                if urls_len == 0 and currentPage <= _page_total:    # 如果url管理器没有新的地址，并且当前查询页面的页数小于总页数，抓取当前页，获取新的地址
                    currentPage = currentPage + 1
                    if net_info['type'] == '51job' :
                        search_url = net_info['url'] + '&pageno=' + str(currentPage) + '&keyword=' + net_info['keyword'] # 拼接首页查询地址
                        html_content = self.downloder.download_html(search_url,headers) # 下载首页查询页面源码
                        page_total, new_urls = self.parser.parse_search_page(html_content) # 分析首页查询页面，获取分页总数和职位详细的地址
                        self.urls.add_new_urls(new_urls)  #把职位详细的地址加入到url管理器
            except Exception as e:
                print ('抓取失败！', e)

        # 爬虫完成会播放语音
        #self.yy.bofangjieshu()
        # 未清洗数据
        #raw_data=self.dataanalyse.sava_raw_data(total_data)
        # 已清洗数据  在本代码没用太多作用
        #cln_data = self.dataanalyse.save_new_data(raw_data)
        #对job位置数据分析===>ok
        #self.datapicture.show_job_location(cln_data)
        # 对job教育数据分析=======>ok
        #self.datapicture.show_job_education()
        # 对job教育数据分析==========>ok
        #self.datapicture.show_job_experience()
        # 对job要求数据分析==========>ok
        #self.datapicture.show_jod_duty(cln_data)
        # 对job薪资数据分析==========>ok
        #self.datapicturepie.show_jod_salary(cln_data)


if __name__=="__main__":
    path = './image'
    if not os.path.exists(path):
        os.mkdir(path)
    print('------可爬取，知识产权，java等关键词------')
    guanjianci=input('请输入爬虫要爬取的内容：')
    net_info1 = {
         'url': 'https://m.51job.com/search/joblist.php?jobarea=000000&keywordtype=2',
         'keyword': guanjianci,
         'type': '51job'
     }

    obj_spider = SpiderMian()   # 实例化爬虫
    obj_spider.craw(net_info1)   # 调用爬虫抓取方法
