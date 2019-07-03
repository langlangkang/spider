'''
网页下载器
'''
import urllib
from urllib import request
import requests

class HtmlDownloader(object):
    #headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    
    # 下载页面源码方法 传入网址和头部                已看
    def download_html(self,url,headers):
        # none是空值
        if url is None:
            return None
        resp = requests.get(url, headers=headers)  # 访问网址,返回200
        time_out = resp.status_code  #得到它的状态 200
        if time_out != 200:  # 200代表连接正常
            return None  # 返回空，并退出这个方法
        resp.encoding='utf-8'  #用'utf-8'解码
        r = resp.text  # 返回文本

        return r  # 读取报文内容
