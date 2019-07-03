'''
网页解析器51
'''
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

class HtmlParser(object):
    
    def _get_new_urls(self, page_url, soup):
        new_urls = {} #定义字典
        links = soup.find_all('a', class_="e") #找节点
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url) #拼接
            new_urls.add(new_full_url) #添加
        return new_urls #返回

    # 网址，soup，craw_type = net_info['type'] + '-' + net_info['keyword']
    def _get_new_data(self, page_url, soup, type):
        res_data = {}   # 定义字典
        res_data['url'] = page_url  #收集地址

        #找jt节点
        jt_node = soup.find('div', {'class':'jt'})
        res_data['type'] = type #收集类型

        res_data['name'] = jt_node.find('p').get_text()#收集职位名称=>  <p>知识产权销售（双休+包住+高提成）</p>
        res_data['public_time'] = jt_node.find('span').get_text() #收集发布时间=>  <span>2019-03-18</span>
        res_data['address'] = jt_node.find('em').get_text() #收集公司地址=>  <em>武汉-洪山区</em>

        res_data['salary']  = soup.find('p',{'class':'jp'}).get_text() #收集薪资=>  0.6-1.2万/月</p>

        #先定义为空
        res_data['experience'] = ''  #收集经验要求
        res_data['education'] = ''    # 收集学历要求

        jd_node = soup.find('div', {'class':'jd'})
        s_n_node = jd_node.find('span', {'class':'s_n'})    #收集经验要求
        s_x_node = jd_node.find('span', {'class':'s_x'})    # 收集学历要求

        if s_n_node is not None:
            res_data['experience'] = s_n_node.get_text()    #收集经验要求
        if s_x_node is not None:
            res_data['education'] = s_x_node.get_text() # 收集学历要求

        res_data['company']  = soup.find('p', {'class':'c_444'}).get_text()    # 收集公司

        ain_p_nodes = soup.find('div', {'class':'ain'}).find_all('p') #里面内容<p>岗位职责：</p>，所以用find_all
                                                                    #但是会出现<p><br></p>
        duty = ''
#         requirement = ''
#         flag = 0;
        for node in ain_p_nodes:
            text = node.get_text()
            if text is None or text == '<br>':
                 continue   #退出这一轮的累加，继续下一轮
            duty = duty + text

        res_data['duty']  = duty #收集岗位职责
#         res_data['requirement']  = requirement
#         print('shuju:',res_data)
        return res_data

    # 网址，页面文本内容，craw_type = net_info['type'] + '-' + net_info['keyword']
    def parse(self, page_url, page_content, type):
        if page_url is None or page_content is None:
            return
        #, from_encoding='utf-8'
        soup = BeautifulSoup(page_content, 'html.parser') #利用BeautifulSoup，格式化html源码
        new_data = self._get_new_data(page_url, soup, type) # 调用分析方法获取数据
        return new_data
    
    # 分析搜索页数据，获取总页数和详细职位地址
    def parse_search_page(self,page_content):
        if page_content is None:
            return      #跳出方法
        new_urls = set()  # 集合add方法
        soup = BeautifulSoup(page_content, 'html.parser')  # 利用BeautifulSoup，格式化html源码
        links = soup.find('div', {'class': 'items'}).find_all('a')  # 职位链接节点
        for link in links:  # 循环链接节点
            new_url = link['href']  # 获取连接
            new_urls.add(new_url)  # 把职位链接添加到集合

        option_nodes = soup.find('div', {'class': 'paging'}).find('select').find_all('option')
        # print(len(option_nodes))# 页面总页数节点
        total = option_nodes[len(option_nodes) - 1].get_text()  # 获取总页数
        # print(type(total))
        return int(total), new_urls    #返回51页，和网址
