#coding = utf-8
#author:    liguo
#email:     15543770273@163.com
#date:      2018-7-26
#describe:  A mysql database library 

import pymysql
import getpass

class Database(object):
#mysql数据库类：
#   属性：
#       query:MYSQL语句字段,通过showResult()方法可以执行该语句并打印结果
#       database:当前数据库，可通过setDatabase()方法修改
#       cursor:当前操作游标
#       table:当前列表，通过setTable方法设置
#   方法：
#       __init__():
#           参数：
#               user:本次Mysql数据库用户名，当前仅供调试用
#               passwd:用户密码，当前仅供调试用
#               host:数据库服务器主机IP地址，默认为本机
#               port:数据库服务器端口，默认3306
#           作用：
#               初始化连接数据库，打印所有数据库
#       setDatabase():
#           参数:
#               dbName:要操作的数据库名
#           作用：
#               设置所使用的数据库
#       setTable():
#           参数:
#               table:要操作的表名
#           作用：
#               设置所使用的数据表
#       showResult():
#           参数：
#               returnType:返回结果类型，为tuple(默认)或list
#           作用：
#               执行query语句，打印并返回执行结果
#       showColumns():
#           参数：
#               无
#           作用：
#               查询当前数据表的所有列
#       convertCondition():
#           参数:
#               condition:字典类型，代表where条件语句的键和值
#           作用：
#               将condition字典数据转化为mysql语句
#       insert();
#           参数：
#               data:字典类型，要插入的数据
#           作用：
#               插入data数据到当前的数据表
#       select();
#           参数：
#               condition：字典类型（可选）
#           作用：
#               查询condition条件下的数据，condition为空时则打印全部
#       delete();
#           参数：
#               condition：字典类型（可选）
#           作用：
#               删除condition指定的数据，为空时则删除全部数据，删除前会询问用户是否确认
#       update();
#           参数：
#               data：修改后的数据，字典类型
#               condition：要修改的数据所符合的条件
#           作用：
#               修改数据段
# 

    def __init__(self, user="", passwd="", host="127.0.0.1",port=3306, database="TEST",charset='utf8'):
        user = input("请输入Mysql用户名：")
        passwd = getpass.getpass()
        self.database = pymysql.connect(host=host, port=port, user=user, password=passwd, database=database, charset=charset)
        self.username = user
        self.passwd = passwd
        self.cursor = self.database.cursor()
        print("当前所有数据库:")
        self.query = "SHOW DATABASES;"
        result = self.showResult()
        self.DATABASES = [db[0] for db in result]
        print(self.DATABASES)
        print("当前数据库所有表格：")
        self.query = "SHOW TABLES;"
        self.showResult()
 
    def setDatabase(self, dbName):
        print("当前所有数据库：%s"%self.DATABASES)
        if not isinstance(dbName, str):
            print("输入数据库名必须为字符串!")
            return False
        if dbName in self.DATABASES:
            self.query = "USE " + dbName
            self.showResult()
            print("切换到数据库:%s"%dbName)
            return True
        else:
            print(dbName + " cannot be found!")
            return False
       
    def setTable(self,table):
        self.table = table

    def showResult(self, resultType=tuple):
        #print(self.query)
        self.cursor.execute(self.query)
        resultTuple = self.cursor.fetchall()
        for result in resultTuple:
            print(result)
        print("\n")
        self.database.commit()
        return resultTuple

    def convertCondition(self, condition):
        if isinstance(condition,dict):
            self.query = self.query + " WHERE "
            andFlag = True 
            for key in condition:
                if andFlag is False:
                    self.query = self.query + " AND %s=%s "%(key, condition[key])
                else:
                    self.query = self.query + "%s=%s"%(key, condition[key])
                    andFlag = False
            self.query = self.query + ";"
            print(self.query)
            return True
        else:
            return False
    
    def showColumns(self):
        self.query = "SHOW COLUMNS FROM %s;"%self.table
        self.showResult()

    def select(self,condition=None):
        self.query = "SELECT * FROM %s"%(self.table)
        if condition is None:
            self.showResult()
            return True
        else:
            self.convertCondition(condition)
            self.showResult()

    def insert(self,data):
        self.query = "INSERT INTO %s "%self.table
        keys = ""
        values = ""
        for key in data:
            keys = keys + key + ','
            values = values + "'" + data[key] + "',"
        keys = keys.rstrip(',')
        values = values.rstrip(',')
        self.query = self.query + "(%s) VALUES (%s);"%(keys, values)
        print(self.query)
        self.showResult()

    def delete(self,condition=None):
        self.query = "DELETE FROM %s"%self.table
        if condition is None:
            flag = input("You will drop all data Yes(y) or Not(n)\n")
            if flag == 'y' or flag == 'Y':
                print("Delete all...")
                self.showResult()
                return True
            else:
                print("Interrupt...")
                return False
        else:
            self.convertCondition(condition)
            self.showResult()
        
    def update(self,data,condition):
        self.query = "UPDATE %s SET "%self.table
        query = ""
        for key in data:
            query = query + "%s=%s,"%(key, data[key])
        self.query = self.query + query.rstrip(',')
        print(self.query)
        self.convertCondition(condition)
        self.showResult()

    def close(self):
        self.cursor.close()
        
    def __checkCode(self):
        self.query = "SHOW VARIABLES LIKE '%char%';"
        print("当前编码：")
        self.code = self.showResult()
        
