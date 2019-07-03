'''
网页管理器
'''
class UrlManager(object):
    
    def __init__(self): 
        self.new_urls = set()  #未抓取url集合
        self.old_urls = set()  #已抓取url集合
    
    def add_new_url(self, url): #添加新的url
        if url is None:
            return      #return下面都不执行
        if url not in self.new_urls and url not in self.old_urls:   #如果地址不在集合之中，添加新的地址到集合中
            self.new_urls.add(url) 
    
    def add_new_urls(self, urls): #添加多个新的url
        if urls is None or len(urls) == 0:
            return
        for url in urls:    # 循环参数地址集合，依次调用 添加新的url
            self.add_new_url(url)
    
    def has_new_url(self):
        return len(self.new_urls) != 0  # 判断是否还有url管理器是否有新的地址
    
    def get_new_url(self):
        new_url = self.new_urls.pop()   # 取出一个新的url，并在集合中移除
        self.old_urls.add(new_url)  # 将新的url放入已抓取集合中
        return len(self.new_urls), new_url  # 返回管理器中未抓取的url长度 和新的url
