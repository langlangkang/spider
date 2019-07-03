from aip import AipSpeech
import pygame
import time
import os
import del_huancun
'''
调用百度api接口，baidu-aip
'''
class YuYin(object):
    def __init__(self):
        #默认参数，不要动
        self.file = './image/audio.mp3'
        self.app_id = "14975947"
        self.api_key = "X9f3qewZCohppMHxlunznUbi"
        self.secret_key = "LupWgIIFzZ9kTVNZSH5G0guNGZIqqTom"
        self.delect=del_huancun.DelHuancun()

    def bofangkaishi(self):
        #初始化
        client = AipSpeech(self.app_id, self.api_key, self.secret_key)
        #返回二进制数据 以二进制写模式打开
        result = client.synthesis("爬虫已准备开始，请耐心等候", "zh", 1, {
            "vol": 9,  # 音量
            "spd": 3,  # 语速
            "pit": 5,  # 语调
            "per": 5,  # 音色
        })
        self.xiaoaikaishi(result)

    def bofangjieshu(self):
        # 初始化
        client = AipSpeech(self.app_id, self.api_key, self.secret_key)
        # 返回二进制数据 以二进制写模式打开
        result = client.synthesis("爬虫已成功，请打开当前文件夹下的网页和表格查看结果", "zh", 1, {
            "vol": 9,  # 音量
            "spd": 3,  # 语速
            "pit": 5,  # 语调
            "per": 5,  # 音色
        })

        self.xiaoaijieshu(result)

    def xiaoaikaishi(self,result):
            #上下文管理器
            with open(self.file, "wb") as f:
                f.write(result)

            pygame.mixer.init() #初始化pygame
            pygame.mixer.music.load(self.file) #加载音乐
            pygame.mixer.music.play(loops=-1, start=0.0)  # start 参数控制音乐从哪里开始播放 loops代表重复次数
            if pygame.mixer.music.get_busy() == True: #判断是否播放
                print('-' * 150)
                print('小森正在说话：......')
                print('-' * 150)
            time.sleep(10)
            # print(pygame.mixer.music.get_volume())
            pygame.mixer.music.stop() #停止
            pygame.quit() #关闭

            #if os.path.exists(self.file):
                #os.remove(self.file)

    def xiaoaijieshu(self,result):
        # 上下文管理器
            with open(self.file, "wb") as f:
                f.write(result)

            pygame.mixer.init() #初始化pygame
            pygame.mixer.music.load(self.file) #加载音乐
            pygame.mixer.music.play(loops=-1, start=0.0)  # start 参数控制音乐从哪里开始播放 loops代表重复次数
            if pygame.mixer.music.get_busy() == True: #判断是否播放
                print('-' * 150)
                print('小森正在说话：......')
                print('-' * 150)
            time.sleep(11)
            # print(pygame.mixer.music.get_volume())
            pygame.mixer.music.stop() #停止
            pygame.quit() #关闭
            #exit() #退出整个程序
