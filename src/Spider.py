#coding = utf-8

import requests
import os
import Database
import Log
from bs4 import BeautifulSoup as bs
import ini
import sys
import random
import urllib.error
from urllib.parse import urlencode
from Models import Company,Job
from functools import reduce
import time
import json

class Spider(object):
    def __init__(self,website,agents):
        self.__website = {
            "url":"https://www.zhaopin.com/",
            "name":"智联招聘"
        }
        self.__dataUrlQueue = []
        self.__commonUrlQueue = []
        self.__historyUrlQueue = []
        self.html = ""
        self.httpCode= 0
        self.__url = website["url"]
        self.agents = agents
        self.data = ""

        self.database = Database.Database(database="Jobs")
        self.database.setDatabase("Jobs")
        self.database.setTable("ZhiLian")
        self.log = Log.Log("log.txt")
        self.company = Company()
        self.job = Job()


    def fake(self):
        self.agent = self.agents[random.randint(0,len(self.agents)-1)]
        self.header = {
            "user-agent":self.agent
        }

    def setUrl(self,url):
        self.__url = url

    def fetchUrl(self,urlType="common"):
        if urlType == "common":
            if not len(self.__commonUrlQueue):
                self.__url = self.__commonUrlQueue.pop(0)
            else:
                print("url队列为空")
        elif urlType == "data":
            if not len(self.__dataUrlQueue):
                self.__url = self.__dataUrlQueue.pop(0)
            else:
                print("url队列为空")
        else:
            print("urlType错误")

    def getHtml(self,code="utf-8"):
        self.fake()
        print(self.__url)
        try:
            req = requests.get(self.__url, headers=self.header, timeout=3)
            self.html = str(req.content, code)
            self.httpCode = req.status_code
            self.bs = bs(self.html,"lxml")
            self.__historyUrlQueue.append(self.__url)
            self.__isGetHtml = True
        except KeyboardInterrupt as e:
            print("Exiting...")
            self.database.close()
            sys.exit(0)
        except urllib.error.HTTPError as e:
            print("HttpError  occur when visiting the url %s;\ncode:%s"%(self.__url,str(e)))
            self.__isGetHtml = False
        except urllib.error.URLError as e:
            print("url %s is wrong!"%self.__url)
            self.__isGetHtml = False

    def run(self):
        pass

       
class Spider_ZhiLian(Spider):
    def __init__(self,website,agents):
        Spider.__init__(self,website,agents)
        self.__job = Job()
        self.__company = Company()
        self.__classList = {}

    def getData(self):
        self.getHtml()
        self.data = json.loads(self.html)

    def getCategory(self):
        divs = self.bs.find_all("div","zp-jobNavigater-popContainer")
        for div in divs:
            firstClassContainer = div.find_all("div","zp-jobNavigater-pop-title")
            firstClass = firstClassContainer[0].string
            secondClassContainer = div.find_all("span")
            secondClass = [container.string for container in secondClassContainer]
            self.__classList[firstClass] = secondClass 
        # self.log.info(self.__classList)
    
    def generateUrl(self,kw,page):
        params = {
            "start": "60",
            "pageSize": "60",
            "cityId": "489",
            "workExperience": "-1",
            "education": "-1",
            "companyType": "-1",
            "employmentType": "-1",
            "jobWelfareTag": "-1",
            "kw": kw,
            "kt": "3",
            "lastUrlQuery": '{"p":%s,"pageSize":"60","jl":"489","kw":"%s","kt":"3"}' % (page, kw)
        }
        website = "https://fe-api.zhaopin.com/c/i/sou?"
        self.__url = website + urlencode(params,safe=':,') 
        self.setUrl(self.__url)
        print(self.__url)


    def dataFilter(self,firstClass,secondClass):
        count = 1 
        for result in self.data['data']['results']:
            print(result['welfare'])
            print(count)
            count = count + 1
            infomation = {
                'firstClass':firstClass,
                'secondClass':secondClass,
                'city':(result['city']['display']),
                'jobName':(result['jobName']),
                'positionUrl':(result['positionURL']),
                'salary':(result['salary']),
                'welfare':(','.join(result['welfare'])),
                'eduLevel':(result['eduLevel']['name']),
                'company':(result['company']['name'])
            }
            self.database.insert(infomation)
            # self.database.select()


    def run(self):
        self.database.delete()
        self.getHtml()
        self.getCategory()
        self.database.setDatabase("Jobs")
        self.database.setTable('ZhiLian')
        for firstClass in self.__classList:
            self.log.write(firstClass)
            print("正在查找：" + firstClass)
            for secondClass in self.__classList[firstClass]:
                print(secondClass)
                self.log.write(secondClass)
                print("正在查找：" + secondClass)
                page = 1
                while True:
                    self.database.select()
                    self.generateUrl(kw=secondClass, page=page)
                    page = page + 1
                    try:
                        self.getData()
                        self.dataFilter(firstClass,secondClass)
                        time.sleep(random.random()+1)
                    except urllib.error.URLError:
                        break
                self.log.write('\t第%s页下载成功'%page)
                self.log.write("\n"*3)
            self.log.write("\n"*6)


if __name__ == "__main__":
    spider = Spider_ZhiLian(ini.WEBSITE,ini.AGENTS)
    spider.run()
