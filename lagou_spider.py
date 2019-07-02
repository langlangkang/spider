from selenium import webdriver
from lxml import etree
import re
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
'''
也是不能爬的太快，不然会跳转到登录页面，重定向
'''


class Lagouspider(object):
    def __init__(self):
        self.driver=webdriver.Chrome()
        #self.url='https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        #self.url='https://www.lagou.com/jobs/list_python%20web?px=default&city=%E5%B9%BF%E5%B7%9E#filterBox'
        self.url='https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?oquery=python%20web&fromSearch=true&labelWords=relative&city=%E5%B9%BF%E5%B7%9E'
        self.popsitions=[]

    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            # 若没有找到  则等待
            WebDriverWait(driver=self.driver,timeout=10).until(EC.presence_of_element_located((By.XPATH,'//div[@class="pager_container"]/span[last()]')))
            self.parse_list_page(source)

            try:
                next_btn=self.driver.find_element_by_xpath("//div[@class='pager_container']/span[last()]")
                if "pager_next_disabled" in next_btn.get_attribute("class"):
                    break
                else :
                    time.sleep(4)
                    next_btn.click()
            except Exception as e:
                print('爬取失败，原因是：',e)
            time.sleep(5)

    def parse_list_page(self,source):
        html=etree.HTML(source)
        links=html.xpath("//a[@class='position_link']/@href")
        for link in links:
            self.request_detail_page(link)
            time.sleep(5)

    def request_detail_page(self,url):
        try:
            self.driver.execute_script('window.open("%s")' % url)  # 新建一个窗口打开详情页
            time.sleep(4)
            self.driver.switch_to.window(self.driver.window_handles[1])  # 跳转到第二个窗口
            time.sleep(2)
            # 若没有找到job-name  则等待其出现
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="job-name"]/span[@class="name"]')))

            source = self.driver.page_source  # 获取源码
            self.parse_datail_page(source)  # 对其解析
            time.sleep(4)
            self.driver.close()  # 关闭第二个详情页
            time.sleep(2)
            self.driver.switch_to.window(self.driver.window_handles[0])  # 跳转到第一个窗口

        except Exception as e:
            print('失败原因是',e)
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()  # 关闭第二个详情页
            time.sleep(4)
            self.driver.switch_to.window(self.driver.window_handles[0])  # 跳转到第一个窗口

    def parse_datail_page(self,source):
        html=etree.HTML(source)
        position_name=html.xpath("//span[@class='name']/text()")[0]  #工作名字
        job_request_spans=html.xpath("//dd[@class='job_request']//span")
        salary=job_request_spans[0].xpath(".//text()")[0].strip()   #薪资
        city=job_request_spans[1].xpath(".//text()")[0].strip()  #城市
        city=re.sub(r'[\s/]','',city)   #去空格
        work_years=job_request_spans[2].xpath(".//text()")[0].strip()  #工作年龄
        work_years=re.sub(r'[\s/]','',work_years)  #去空格
        education=job_request_spans[3].xpath(".//text()")[0].strip()  # 教育情况
        education = re.sub(r'[\s/]', '', education)  #去空格
        desc=''.join(html.xpath("//dd[@class='job_bt']//text()")).strip()  #全职
        companyname=html.xpath("//div[@class='job-name']/div[@class='company']/text()")[0]  #公司名字
        position={
            'name':position_name,
            'company_name':companyname,
            'salary':salary,
            'city':city,
            'workyears':work_years,
            'education':education,
            'desc':desc
        }
        self.popsitions.append(position)
        print('=' * 50)
        print('保存成功==========',position)
        #print(self.popsitions)
        pd.DataFrame(self.popsitions).to_csv('python_analy_data.csv',index=False,sep=',')

    def save_datail_page_data(self):
        pass

if __name__ == '__main__':
    spider=Lagouspider()
    spider.run()