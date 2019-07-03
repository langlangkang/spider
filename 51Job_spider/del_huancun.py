import os

class DelHuancun(object):
    def __init__(self):
        #默认参数，不要动
        self.file = './image/audio.mp3'

    def guanbihuancun(self):
        try:
            if os.path.exists(self.file):
                os.remove(self.file) #删除文件
                print('清理完成。。。。。。')
            else:
                print('当前没有缓存')
        except Exception as e:
            print('警告警告：',e)

delect=DelHuancun()
delect.guanbihuancun()