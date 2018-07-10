#coding:utf-8

# 本例通过selenium + PhantomJS 爬取 新浪财经的外汇信息(foreign currency exchange)
# 动态获得数据  https://hq.sinajs.cn/etag.php?_=1531138157058&list=fx_susdcny

from selenium import webdriver  #导入Selenium
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
import time
import urllib


# TODO 下方注释是：另一种爬取动态数据的方式，浏览器F12 -> 网络 -> XHR 抓取AJAX报文，找到请求头的url 使用该url来进行爬取。类似豆瓣抓取排名的示例
"""
return_data = requests.get("https://hq.sinajs.cn/etag.php?_=1531138157058&list=fx_susdcny", verify = False)
print(return_data.text)     # 返回的是一个response对象  可以 print(return_data.text)
#"""


class ExchangeCalc():

    def __init__(self):  #类的初始化操作
        #self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        #要访问的网页地址
        self.usdcny_url = 'http://finance.sina.com.cn/money/forex/hq/USDCNY.shtml'  
        self.cnyusd_url = 'http://finance.sina.com.cn/money/forex/hq/CNYUSD.shtml'
        self.eurcny_url = 'http://finance.sina.com.cn/money/forex/hq/EURCNY.shtml'
        self.cnyeur_url = 'http://finance.sina.com.cn/money/forex/hq/CNYEUR.shtml'
        self.usdeur_url = 'http://finance.sina.com.cn/money/forex/hq/USDEUR.shtml'
        self.eurusd_url = 'http://finance.sina.com.cn/money/forex/hq/EURUSD.shtml'
        # self.folder_path = 'G:\\Python_Workspace\\crawler\\crawl_pics\\Beatles'  #设置图片要存放的文件目录

    def get_exchange(self):
        # print('开始网页get请求')
        # 使用selenium通过PhantomJS来进行网络请求
        driver = webdriver.PhantomJS()
        tag = 0
        while(tag==0):
            try:
                # C-人民币 U-美元 E-欧元
                driver.get(self.usdcny_url)
                UC = float(BeautifulSoup(driver.page_source,'html.parser').find('div',id='quoteWrap').find('h5').text)
                driver.get(self.cnyusd_url)
                CU = float(BeautifulSoup(driver.page_source,'html.parser').find('div',id='quoteWrap').find('h5').text)
                driver.get(self.eurcny_url)
                EC = float(BeautifulSoup(driver.page_source,'html.parser').find('div',id='quoteWrap').find('h5').text)
                driver.get(self.cnyeur_url)
                CE = float(BeautifulSoup(driver.page_source,'html.parser').find('div',id='quoteWrap').find('h5').text)
                driver.get(self.usdeur_url)
                UE = float(BeautifulSoup(driver.page_source,'html.parser').find('div',id='quoteWrap').find('h5').text)
                driver.get(self.eurusd_url)
                EU = float(BeautifulSoup(driver.page_source,'html.parser').find('div',id='quoteWrap').find('h5').text)
                print(u'汇率获取完毕 ')
                print('美-人:',UC,' 人-美:',CU,' 欧-人:',EC,' 人-欧:',CE,' 美-欧:',UE,' 欧-美:',EU)
                tag=1
            except:
                print(u'爬取数据故障，正在重新爬取。')
                time.sleep(5)
        if tag==1:
            return {'uc':UC,'cu':CU,'ec':EC,'ce':CE,'ue':UE,'eu':EU}
        # print('美元兑人民币： ',USDCNY.text)
        # print('开始获取所有a标签')
        
    def calc_profit(self,exchange_dic):
        begin_money = 1000
        end1 = begin_money*exchange_dic['cu']*exchange_dic['ue']*exchange_dic['ec']
        end2 = begin_money*exchange_dic['ce']*exchange_dic['eu']*exchange_dic['uc']
        profit1 = (end1-begin_money)/begin_money
        profit2 = (end2-begin_money)/begin_money
        if profit1>profit2 and profit1>0:
            print(u'人民币-> 欧元-> 美元-> 人民币 有套利空间: ',profit1)
        elif profit2>profit1 and profit2>0:
            print(u'人民币-> 美元-> 欧元-> 人民币 有套利空间: ',profit2)
        else:
            print(u'无套利空间。',profit1,profit2)
        
    def request(self, url):  #返回网页的response
        r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r



def main():
    while(True):
        ex_obj = ExchangeCalc()  #创建类的实例
        ddd = ex_obj.get_exchange()  #执行类中的方法
        # print(ddd['uc'],ddd['cu'],ddd['uc']*ddd['cu'])
        # print(ddd['ec'],ddd['ce'],ddd['ec']*ddd['ce'])
        # print(ddd['ue'],ddd['eu'],ddd['ue']*ddd['eu'])
        ex_obj.calc_profit(ddd)
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),'\n')
        time.sleep(30)

if __name__ == '__main__':
    main()

#"""
