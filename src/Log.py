#coding = utf-8

import os

class Log(object):
    def __init__(self, fileName):
        self.name = fileName
        if os.path.exists(fileName):
            pass
        else:
            with open(fileName,"w+") as f:
                pass
            
    def info(self,msg):
        if isinstance(msg,list) or isinstance(msg,tuple):
            for i in msg:
                print(i)
        elif isinstance(msg,dict):
            for key in msg:
                print("%s:%s"%(key,msg[key]))
        else:
            print(msg)

    def write(self,string):
        with open(self.name,"a+") as f:
            f.write(string)
        
    def readLast(self):
        with open(self.name,"r") as f:
            data = f.readlines()
        return data[-1]