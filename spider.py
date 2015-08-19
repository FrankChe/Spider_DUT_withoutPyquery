# -*- coding: utf-8 -*- 

__author__ = 'chexiaoyu'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import cookielib
import re
#from pyquery import PyQuery as pq
import getpass
import time
#DUT计算绩点


class DUT:

    def __init__(self,username,password):
        #登陆Url
        self.loginUrl = 'http://202.118.65.21:8089/loginAction.do'
        #本学期成绩Url
        #self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=fa'
        #self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=4242'
        self.gradeUrl = None
        #self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=sxinfo&lnsxdm=001'
        #self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=fa:164'
        self.cookies = cookielib.CookieJar()
        self.postdata = urllib.urlencode({
            'zjh':username,
            'mm':password
        })
        #构建opener
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        #学分list
        self.credit = []
        self.grades = []

        #课程list
        self.course = []
        self.ty = []


    #获取本学期成绩页面
    def getPage(self):
        request = urllib2.Request(
            url = self.loginUrl,
            data = self.postdata)
        result = self.opener.open(request)
        result = self.opener.open(self.gradeUrl)
        
        #print result.read().decode('gbk')
        #打印登陆内容

        return result.read().decode('gbk')
        #return result.read()

    def get_trueUrl(self):
        page = self.getPage()


    def getGrades_software(self):
        #获得本学期成绩(软件工程)
        self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=4242'
        page = self.getPage()

        pattern = re.compile(r'<td align[\s\S]*?<td align[\s\S]*?<td align[\s\S]*?>([\s\S]*?)</td>[\s\S]*?<td align[\s\S]*?<td align.*?>([\s\S]*?)</td>[\s\S]*?<td align[\s\S]*?>([\s\S]*?)</td>[\s\S]*?<td align[\s\S]*?<p.*?>(.*?)&nbsp;')
        p = pattern.findall(page)

        for i in p:
            self.credit.append(float("".join(i[1].split())))
            self.grades.append(float("".join(i[3].split())))
            self.course.append("".join(i[0].split()))
            self.ty.append("".join(i[2].split()))
        print "所有课程及成绩："
        for i in range(len(self.course)):
            print self.course[i],self.ty[i],self.grades[i],self.credit[i]

    def getGrades_required(self,type):
        #获得本学期必修课成绩
        if type == '1':
            self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=4242'
        else:
            self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=4243'
        page = self.getPage()
        credit = []
        grades = []
        #using regular expression
        pattern = re.compile(r'<td align[\s\S]*?<td align[\s\S]*?<td align[\s\S]*?>([\s\S]*?)</td>[\s\S]*?<td align[\s\S]*?<td align.*?>([\s\S]*?)</td>[\s\S]*?<td align[\s\S]*?>([\s\S]*?)</td>[\s\S]*?<td align[\s\S]*?<p.*?>(.*?)&nbsp;')
        p = pattern.findall(page)

        for i in p:
            t = "".join(i[2].split())
            if t == '必修':
                credit.append(float("".join(i[1].split())))
                grades.append(float("".join(i[3].split())))
        return credit,grades


    def getGrades_network(self):
        #获得本学期成绩(网络工程)
        self.gradeUrl = 'http://202.118.65.21:8089/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=4243'
        page = self.getPage()

        pattern = re.compile(r'<td align[\s\S]*?<td align[\s\S]*?<td align[\s\S]*?>([\s\S]*?)</td>[\s\S]*?<td align[\s\S]*?<td align.*?>([\s\S]*?)</td>[\s\S]*?<td align[\s\S]*?>([\s\S]*?)</td>[\s\S]*?<td align[\s\S]*?<p.*?>(.*?)&nbsp;')
        p = pattern.findall(page)

        for i in p:
            if "".join(i[3].split()) == "通过":
                continue
            self.credit.append(float("".join(i[1].split())))
            self.grades.append(float("".join(i[3].split())))
            self.course.append("".join(i[0].split()))
            self.ty.append("".join(i[2].split()))
        print "所有课程及成绩："
        for i in range(len(self.course)):
            print self.course[i],self.ty[i],self.grades[i],self.credit[i]



    def getGrade(self,type):
        #计算总绩点
        if type == '1':
            self.getGrades_software()
            credit, grades = self.getGrades_required(type)
        else:
            self.getGrades_network()
            credit, grades = self.getGrades_required(type)
        sum = 0.0
        weight = 0.0
        for i in range(len(self.credit)):
            sum += self.credit[i] * self.grades[i]
            weight += self.credit[i]

        sum_re = 0.0
        weight_re = 0.0
        for i in range(len(credit)):
            sum_re += credit[i] * grades[i]
            weight_re += credit[i]

        print "你的平均成绩为：",sum/weight
        print "你的GPA为(标准算法)：",sum*4/(weight*100)
        print "你的必修课平均成绩为：",sum_re/weight_re
        print "你的必修课GPA为(标准算法)：",sum_re*4/(weight_re*100)

    def getGrade_delete(self):
        course_del = raw_input("请输入要删除的课程  (输入q结束输入)")
        while course_del != 'q':
            if course_del not in self.course:
                print "没有该课程"
                course_del = raw_input("请输入要删除的课程  (输入q结束输入)")
            else:
                p = self.course.index(course_del)
                self.course.remove(course_del)
                self.credit.remove(self.credit[p])
                self.grades.remove(self.grades[p])
                course_del = raw_input("请输入要删除的课程  (输入q结束输入)")

        print "删除后的课程列表及成绩为："
        for i in range(len(self.course)):
            print self.course[i],self.ty[i],self.grades[i],self.credit[i]

        sum = 0.0
        weight = 0.0
        for i in range(len(self.credit)):
            sum += self.credit[i] * self.grades[i]
            weight += self.credit[i]
        print "你的平均成绩为：(删除指定课程删除指定课程后)",sum/weight
        print "你的GPA为(标准算法)：(删除指定课程后)",sum*4/(weight*100)
        print " "



while True:
    print "请输入学号和密码：(输入“q”退出)"
    username = raw_input()
    if username == 'q':
        exit(0)
    password = getpass.getpass()
    type = raw_input("请输入你的专业类型： 1. 软件工程   2. 网络工程") #用以区分专业类型
    if type != '1' and type != '2':
        print "输入非法，即将退出程序..."
        time.sleep(2)
        exit(1)

    try:
        dut = DUT(username,password)
        dut.getGrade(type)
        op = raw_input("要删除几门课程进行计算吗？ Y/N")
        if op == 'Y' or op == 'y':
            dut.getGrade_delete()
        elif op == 'N' or op == 'n':
            print "查询结束\n"
        else:
            print "输入非法\n"


    except:
        print "失败！"
