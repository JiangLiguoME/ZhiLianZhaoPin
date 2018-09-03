#coding = utf-8

class Job(object):
    def __init__(self,firstClass="",secondClass="",workplace='',job='',salary='',company='',positionUrl='',welfare=''):
        self.__firstClass = firstClass
        self.__secondClass = secondClass
        self.__workplace = workplace
        self.__company = company
        self.__salary = salary
        self.__job = job
        self.__positionUrl = positionUrl
        self.__welfare = welfare

    def attachDatabse(self,database):
        self.database = database

    def workplace(self,workplace_=None):
        if workplace_ is None:
            return self.__workplace
        elif isinstance(workplace_,str):
            self.__workplace = workplace_
        else:
            pass
            # print("警告：工作地点应为字符串类型")
               
    def salary(self,salary_):
        self.__salary = salary_

    def job(self,job_):
        self.__job = job_

    def company(self,company_):
        self.__company = company_

    def degree(self,degree_):
        self.__degree = degree_

    def num(self,num_):
        self.__num = num_

    def positionUrl(self,positionUrl_):
        self.__positionUrl =positionUrl_

    def welfare(self,welfare_):
        self.__welfare = welfare_

class Company(object):
    def __init__(self,firstClass='',secondClass='',name='',location='',assets='',scale='',field=''):
        self.__name = name
        self.__location = location
        self.__assets = assets
        self.__scale = scale
        self.__field = field
 
    def name(self,name_):
        self.__name = name_

    def location(self,location_):
        self.__location = location_

    def assets(self,assets_):
        self.__assets = assets_

    def scale(self,scale_):
        self.__scale = scale_

    def field(self,field_):
        self.__field = field_