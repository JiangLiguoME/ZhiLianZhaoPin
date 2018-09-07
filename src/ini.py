#coding = utf-8

#测试信息
testInfo = '''
本程序为爬取智联招聘招聘信息爬虫，请勿将其用于商业用途，否则后果自负！
请先运行MYSQL脚本新建数据表格，再运行本程序。
    作者：liguo
    程序测试环境：python3.5 + ubuntu 16.04LTS
    联系邮箱:15543770273@163.com
'''

#Mysql数据库相关配置
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = "3306"
DATABASE_NAME = "Jobs"

#爬虫相关配置
AGENT1 = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"
AGENT2 = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
AGENT3 = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.140 Chrome/64.0.3282.140 Safari/537.36'
AGENT4 = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.140 Chrome/64.0.3282.140 Safari/537.36'
AGENT5 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
AGENTS =[AGENT1,AGENT2,AGENT3,AGENT4,AGENT5]

WEBSITE={
    "name":"智联招聘",
    "url":"https://www.zhaopin.com/"
}
STARTURL = WEBSITE["url"]

