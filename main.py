import base64
import hashlib
import http.cookiejar
import io
import json
import os
import sys
import threading
import time
import tkinter as tk
import urllib.request
from tkinter.messagebox import *

import pymysql
import requests
from pygame import mixer
from wmi import WMI
lock = threading.Lock()
module_path2 = os.path.dirname(os.path.realpath(sys.argv[0]))
secondpath = '\\date\\'
module_path = os.path.dirname(os.path.realpath(sys.argv[0]))
def app_path():#冻结路径，防止pyinstaller那个傻逼不认识
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(sys.executable)  #使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__)
def str_to_hex(s):
    return ' '.join([hex(ord(c)).replace('0x', '') for c in s])
def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])
def str_to_bin(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])
def bin_to_str(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])
def formatCooie(s):
    temlist = []
    for c in s:
        temlist.append(hex(ord(c)))
    temlist.append('0d')
    temlist.append('0a')
    cookie2=''
    for i in temlist:
        cookie2=cookie2+''.join(hex_to_str(i))
    return cookie2
def ToBase64(file, txt):
    with open(file, 'rb') as fileObj:
        image_data = fileObj.read()
        base64_data = base64.b64encode(image_data)
        fout = open(txt, 'w')
        fout.write(base64_data.decode())
        fout.close()
def ToFile(txt, file):
    with open(txt, 'r') as fileObj:
        base64_data = fileObj.read()
        ori_image_data = base64.b64decode(base64_data)
        fout = open(file, 'wb')
        fout.write(ori_image_data)
        fout.close()
def play():
    lock.acquire()
    path = module_path+'\\dh\\de.mh'
    path2= module_path+'\\dh\\ml.ad'

    ToFile(path, path2)
    mixer.init()
    mixer.music.load(path2)
    lock.release()
    while True:
        mixer.music.play()
        time.sleep(10)
def stop():
    mixer.music.stop()
def writefile(str,filename):
    path = module_path2+secondpath+filename
    f = open(path,'w')
    f.write(str)
    f.close()
def writedic(dic,filename):
    path = module_path2 + secondpath + filename
    f = open(path,'w')
    js = json.dumps(dic)
    f.write(js)
    f.close()
def readfile(filename):
    path = module_path2 + secondpath + filename
    f = open(path,'r')
    return f.read()
def readdic(filename):
    path = module_path2 + secondpath + filename
    f = open(path,'r')
    js = f.read()
    dic = json.loads(js)
    f.close()
    return  dic

class register:
    def __init__(self):
        self.Des_Key = "DESCRYPT"  # Key
        self.Des_IV = "\x15\1\x2a\3\1\x23\2\0"  # 自定IV向量
    global s
    s = WMI()
    # cpu 序列号
    def get_CPU_info(self):
        cpu = []
        cp = s.Win32_Processor()
        for u in cp:
            cpu.append(
                {
                    "Name": u.Name,
                    "Serial Number": u.ProcessorId,
                    "CoreNum": u.NumberOfCores
                }
            )
        #   print(":::CPU info:", json.dumps(cpu))
        return cpu
class ChongkeSchool(object):
    cookieStr = ''
    def __init__(self):
        print()
    def Login2(self,uname,upasswd):
        result=''
        date = {'username': uname,'password': upasswd, 'encodePassword': ''}
        header = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',
                   'Connection': 'open'
                   # 'Referer':'http://jwnew.cqust.edu.cn/eams/login.action?cqustadminweb=1'
                   }
        writedic(dic=date,filename='Logindate.date')
        login_url = readfile('loginurl.audr')
        s = requests.session()
        rs = s.post(login_url, date)
        c = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
        s.cookies.update(c)
        dic=s.cookies.get_dict()
        print(dic['JSESSIONID'])
        return 'JSESSIONID:'+dic['JSESSIONID']

    def Login(self,uname,upasswd):
        result=''
        date = {'username': uname,'password': upasswd, 'encodePassword': ''}

        writedic(dic=date,filename='Logindate.date')

        post_data = urllib.parse.urlencode(date).encode('utf-8')
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',
                   'Connection': 'open'
                   #'Referer':'http://jwnew.cqust.edu.cn/eams/login.action?cqustadminweb=1'
                   }
        # 登录时表单提交到的地址（用开发者工具可以看到
        login_url = readfile('loginurl.audr')
        # 构造登录请求
        req = urllib.request.Request(login_url, headers=headers, data=post_data)
        # 构造cookie
        cookie = http.cookiejar.CookieJar()
        # 由cookie构造opener
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        # 发送登录请求，此后这个opener就携带了cookie，以证明自己登录过
        resp = opener.open(req)
        # 登录后才能访问的网页
        url = readfile('urlLoginsuccess.sc')
        # 构造访问请求
        req = urllib.request.Request(url, headers=headers)
        try:
            resp = opener.open(req)
            cookieStr = ''
           # print(cookie)
            for item in cookie:
                cookieStr1 = cookieStr + item.name + '=' + item.value
                cookieStr = cookieStr+cookieStr1
            #print('cookie11111',cookieStr)
            #cookieStr=formatCooie(cookieStr)
            #print('cookie22222', cookieStr)
            ChongkeSchool.cookieStr = cookieStr
            headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',
                       'Cookie': cookieStr}
            resp2 = requests.get(url, headers=headers,verify=False)

            writefile(str=cookieStr,filename='cookie.cv')
            return resp2.status_code
        except Exception as e:
            return e
class Mysql(object):
    conn = pymysql.connect(host='',
                           port=3306, user='',
                           passwd='',
                           db='',
                           charset='utf8')
    ERROR = False
    def mysql_select(self,value):
        sql = "select t_kami from tb_kami where t_kami = '{value}'".format(value=value)
        #print(sql)
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            #result = cursor.fetchall()
            result =cursor.fetchone()
            #print('resu',result)
            for row in result:
                getKami = row[0]
            self.conn.commit()
        except Exception as e:
            print('reson:',e)
            self.conn.rollback()
        #cursor.close()
        #self.conn.close()
        return result
    def select2judge(self,value):
        ret = self.mysql_select(value)
        if ret:
            return True
        else:
            return False
    def mysql_delect(self,value):
        sql = "delete from tb_kami where t_kami='{value}'".format(value=value)
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            if cursor.rowcount:
                print('删除成功')
            self.conn.commit()
        except Exception as e:
            print('reson',e)
            self.conn.rollback()


    def insert(self,value):
        sql = "insert into tb_checkmain(checkmachin) values('{value}')".format(value=value)
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            print(cursor.rowcount)
            self.conn.commit()
        except Exception as e:
            print('reson', e)
            self.conn.rollback()


    def checkmain(self,value):
        sql = "select * from tb_checkmain where checkmachin = '{value}'".format(value=value)
        #print(sql)
        flag = False
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            #result = cursor.fetchall()
            result =cursor.fetchone()
            #print('resu',result)
            if result:
                flag = True
            else:
                flag = False
            self.conn.commit()
        except Exception as e:
            print('reson:',e)
            self.conn.rollback()

        return flag

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码


def xuanke(date3):#选课函数
    # chongkeCookie = ChongkeSchool.cookieStr
    ck = ChongkeSchool()
    allinfo={}
    allinfo = readfile('Logindate.date')
    allinfo=eval(allinfo)
    #print(allinfo,type(allinfo))
    sname = str( allinfo["username"])
    spwd = str(allinfo["password"])
    #print(sname,spwd)
    try:
        lock.acquire()
        cookie =readfile('cookie.cv') #ck.Login2(sname,spwd)
        lock.release()
        print(cookie)
        chongkeCookie = cookie
        date2 = date3
       # print(cookie)
        url2 = readfile('urlselectcourse.sc')#选课的URL连接，需要在文件里添加
        headers = {
            'Host': 'jwnew.cqust.edu.cn',
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'Accept':'text/html, */*; q=0.01',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate',
            'Referer': 'http://jwnew.cqust.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id=1322',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '27',
            'Connection':'close',
            'Cookie': chongkeCookie
        }
        resp1 = requests.get('http://jwnew.cqust.edu.cn/eams/home.action',headers=headers)
        proxies = {"https": "https://127.0.0.1:8080", "http": "http://127.0.0.1:8080"}

        resp2 = requests.post(url2, headers=headers, data=date2,proxies=proxies)

        print(resp2.url)
        print(resp2.headers)
        #resp2 = requests.get(url2)
        #print(resp2.text)

       # print(resp2.text)
        print(resp2.text.find("选课成功",0,len(resp2.text)))
        if resp2.text.find('登录失败') > 0:
            return '-1000'
        if resp2.text.find('人数已满') > 0:
            return '-1001'
        if resp2.text.find('选课成功') > 0:
            return '1000'
        else:
            print(resp2.status_code)
            return str(resp2.status_code)  # resp2.status_code
    except Exception as e:
        print(e)
        #print(resp2.text)
        return '-1004'
def chongKeloginSuccess():

    xuan = tk.Toplevel()
    xuan.geometry('530x600')
    xuan.title('重科抢课帮bate版———专业选课20年')
    classcode = tk.StringVar()
    classcode.set('')
    getcookie = tk.StringVar()
    getcookie.set('')
    threadNum = tk.StringVar()
    threadNum.set('4')

    lablename = tk.Label(xuan, text='课程编号:', justify=tk.RIGHT, width=80)
    lablename.place(x=10, y=50, width=100, height=20)
    ename = tk.Entry(xuan, width=100, textvariable=classcode)
    ename.place(x=130, y=50, width=200, height=20)

    labelxian = tk.Label(xuan, text='要开启的线程:', justify=tk.RIGHT, width=80)
    labelxian.place(x=10, y=100, width=100, height=20)
    entryxian = tk.Entry(xuan, width=50, textvariable=threadNum)
    entryxian.place(x=130, y=100, width=50, height=20)


    showinfo(title='警告',message='cookie失效，请先手动添加cookie再抢课')

    lablecookie = tk.Label(xuan, text='cookie:', justify=tk.RIGHT, width=80)
    lablecookie.place(x=10, y=150, width=100, height=20)
    entrycookie = tk.Entry(xuan, width=50, textvariable=getcookie)
    entrycookie.place(x=130, y=150, width=200, height=20)
    def addCookie():
       writefile(str='JSESSIONID='+getcookie.get(), filename='cookie.cv')
       def select_class():
           startnum = threadNum.get()
           startnum = int(startnum)

           class DownThread(threading.Thread):
               def __init__(self):
                   threading.Thread.__init__(self)
                   self._running = True

               def terminate(self):
                   self._running = False

               def setD(self):
                   threading.Thread.daemon = True

               def run(self):
                   if self._running:
                       sonThread()

           def sonThread():
               for i in range(int(startnum)):  # 创建线程
                   tname = '线程' + str(i)
                   temth = threading.Thread(target=myred, args=(tname, 2, 5), name=tname)
                   temth.start()
                   temth.join(1)

           m = DownThread()
           lock = threading.Lock()

           def myred(threadName, delay, clear):
               print(classcode.get())
               cdate = {
                   'operator0': str(classcode.get()) + ':true:0',
               }
               getcode = xuanke(date3=cdate)

               while getcode != '1000':
                   time.sleep(delay)
                   getcode = xuanke(date3=cdate)
                   temptxt = '在很努力的抢课呢'
                   if getcode == '-1000':
                       temptxt = '登录失败，当前选课不开放'
                   elif getcode == '-1001':
                       temptxt = '人数已满'
                   elif getcode == '-1004':
                       temptxt == '未知错误'
                   elif getcode == '1000':
                       lock.acquire()
                       play()
                       xtext.insert(1.0, '选课成功，快去看看吧！！' + '\n')
                       tk.messagebox.showinfo(message='选课成功，快去看看吧')
                       m.terminate()

                   xtext.insert(1.0, threadName + ':' + '开始抢课中:' + temptxt + '\n')
                   if clear == 10:
                       xtext.insert(1.0, '清空文本框中.....' + '\n')
                       clear = 0
                       xtext.delete(1.0, tk.END)
                   clear += 1

           if int(startnum) > 18:
               tk.messagebox.showinfo(title='警告！', message='亲亲，我们这边不太建议你选择太大线程呦！')
           m.setD()  # thread1,它做为程序主线程的守护线程,当主线程退出时,thread1线程也会退出,由thread1启动的其它子线程会同时退出,不管是否执行完任务
           m.run()

           # m.join()
           def stop_select():
               m.terminate()
               buttonLogin2.destroy()
               buttonLogin3 = tk.Button(xuan, text='开始选课', command=select_class)
               buttonLogin3.place(x=380, y=43, width=80, height=30)
               module_path = os.path.dirname(__file__)
               path2 = module_path + '\\dh\\ml.ad'
               stop()
               if os.path.exists(path2):
                   os.remove(path2)
               xuan.destroy()
               # for i in range(startnum):
               #
               #    temth['id' + str(i)].join()

           buttonLogin.destroy()
           buttonLogin2 = tk.Button(xuan, text='停止选课', command=stop_select)
           buttonLogin2.place(x=380, y=43, width=80, height=30)

       buttonLogin = tk.Button(xuan, text='开始抢课', command=select_class)
       buttonLogin.place(x=380, y=43, width=80, height=30)
       xtext = tk.Text(xuan)
       xtext.place(y=250, width=490, height=300)

       scroll = tk.Scrollbar(xuan, command=xtext.yview)
       xtext.configure(yscrollcommand=scroll.set)
       scroll.place(x=500, y=250, height=310)
    addcb = tk.Button(xuan, text='添加cookie', command=addCookie)
    addcb.place(x=380, y=153, width=80, height=30)
    xuan.mainloop()
#chongKeloginSuccess()
def nextstart():
    root = tk.Toplevel();
    root.title('重科抢课帮bate版——专业抢课20年')
    root.geometry('400x300')

    varname = tk.StringVar()
    varname.set('')
    varpwd = tk.StringVar()
    varpwd.set('')
    savedateLogin = readfile('Logindate.date')
    savedateLogin = eval(savedateLogin)  # 将存储的Logindate.txt文件转为字典格式
    if savedateLogin:
        varname.set(str(savedateLogin['username']))
        varpwd.set(str(savedateLogin['password']))
    # 创建标签
    lablename = tk.Label(root, text='学号:', justify=tk.RIGHT, width=80)
    # 将标签放在窗口上
    lablename.place(x=10, y=50, width=100, height=20)
    # 创建文本框，同时设置关联变量d
    ename = tk.Entry(root, width=100, textvariable=varname)
    ename.place(x=130, y=50, width=150, height=20)
    labpwd = tk.Label(root, text='密码:', justify=tk.RIGHT, width=80)
    labpwd.place(x=10, y=85, width=100, height=20)
    # 创建密码文本框
    epwd = tk.Entry(root, show='*', width=80, textvariable=varpwd)
    epwd.place(x=130, y=85, width=150, height=20)


    def cancel():
        varname.set('')
        varpwd.set('')
    def Login():
        # 获取用户名密码
        name = ename.get()
        pwd = epwd.get()

        chongke = ChongkeSchool()
        check = chongke.Login(uname=name, upasswd=pwd)
        if check == 200:
            tk.messagebox.showinfo(message='登陆成功',title='恭喜恭喜')
            root.destroy()
            chongKeloginSuccess()
        else:
            tk.messagebox.showinfo(message='登陆失败',title='卧槽，怎么登不上去')

    labpwd = tk.Label(root, text='密码:', justify=tk.RIGHT, width=80)
    labpwd.place(x=10, y=85, width=100, height=20)
    # 创建密码文本框
    epwd = tk.Entry(root, show='*', width=80, textvariable=varpwd)
    epwd.place(x=130, y=85, width=150, height=20)
    buttonLogin = tk.Button(root, text='登录', command=Login)
    buttonLogin.place(x=90, y=160, width=80, height=30)
    buttonCancel = tk.Button(root, text='退出', command=cancel)
    buttonCancel.place(x=240, y=160, width=80, height=30)
    root.mainloop()

def next2start():
    def MD5(str):
        hl = hashlib.md5()
        hl.update(str.encode("utf-8"))
        return hl.hexdigest()

    root = tk.Toplevel();
    root.title('重科抢课帮bate版——专业抢课20年')
    root.geometry('500x300')
    kami = tk.StringVar()
    kami.set('')

    lablename = tk.Label(root, text='请输入卡密:', justify=tk.RIGHT, width=80)
    lablename.place(x=10, y=50, width=100, height=20)

    jihuo = tk.Text(root, width=50)
    jihuo.place(x=130, y=50, width=300, height=100)

    myreg = register()
    msql = Mysql()
    # login = Loginm()
    checkcode = myreg.get_CPU_info()

    def check():
        input_code = jihuo.get(0.0, tk.END)
        temp = ''
        temp2 = ''
        for i in checkcode:
            temp = temp + i['Serial Number']
        # print(temp)
        get_input = msql.select2judge(MD5(input_code))
        if get_input:
            tk.messagebox.showinfo(message='激活成功，请重启软件后使用！')

            for i in msql.mysql_select(MD5(input_code)):
                temp2 = temp2 + i
            msql.mysql_delect(MD5(input_code))
            #module_path = os.path.dirname(__file__)
            path = app_path() + '\\sys\\check.kv'
            f = open(path, 'w')
            f.write(temp2)
            tcheckcode = temp + temp2  # +login.uname
            # print(temp2)
            print(tcheckcode)
            msql.insert(tcheckcode)
        else:
            tk.messagebox.showinfo(message='激活失败，请检查你的卡密')

    buttonLogin = tk.Button(root, text='激活', command=check)
    buttonLogin.place(x=400, y=230, width=80, height=30)
    root.mainloop()

formmain = tk.Tk()
formmain.title('重科抢课帮bate版——专业抢课20年')
formmain.geometry('600x500')

canvas = tk.Canvas(formmain, width=400, height=135, bg='green')
module_path = os.path.dirname(__file__)
path = app_path() + '\\ico\\load.gif'
print(path)

image_file = tk.PhotoImage(file=path)
img_label = tk.Label(formmain, image=image_file)
img_label.pack(side=tk.TOP)
text = tk.Text(formmain, width=550, height=50)
text.place(x=30,y=300,width=500,height=100)
showinfo(message= '注意：本软件只是在运行期间不断模拟你选课的行为，并不能拯救你学校的垃圾服务器，能不能捡漏就看你运气了',title='FBI WORRING:请注意')
j=0
def refrech_date():
    text.insert(1.0, '检测是否激活中.....\n')
    global j
    j=j+1
    if j == 2:
        flag =True
        return flag
    #formmain.after(1000, refrech_date)
x=0
def refrech_date2():
    text.insert(1.0, '获取硬件序列号中.....\n')
    global x
    x = x + 1
    #if x==1:
        #text.insert(tk.END, '111111\n')
    if x == 2:
        return
    #formmain.after(1000, refrech_date2)
z=0
def refrech_date3():
    text.insert(1.0, '与服务器校对中.....\n')
    global z
    z = z + 1
    if z == 2:
        return
    #formmain.after(1000, refrech_date3)
#formmain.after(500,refresh_data)

myreg = register()
msql = Mysql()
checkcode = myreg.get_CPU_info()
path = app_path() + '\\sys\\check.kv'
tmpstr = ''
temp = ''
f = open(path, 'r')
for i in f:
    tmpstr = i
for i in checkcode:
    temp = temp + i['Serial Number']
checkresult=msql.checkmain(temp+tmpstr)


formmain.after(0,refrech_date())
formmain.after(0, refrech_date2())
formmain.after(0, refrech_date3())
text.insert(1.0, '检测完成！\n')
def next():
    #formmain.destroy()
    nextstart()
def next2():
    next2start()
if checkresult:
    text.insert(1.0, '软件已激活！谢谢哥哥姐姐们给口饭吃！\n')
    buttonCancel = tk.Button(formmain, text='启动',command=next)
    buttonCancel.place(x=450, y=450, width=80, height=30)
else:

    text.insert(1.0, '开发不容易，写了五天，还通宵了三晚上，希望各位哥哥姐姐们体谅一下！帮忙测试获取激活码,有钱任性也可以这里直接购买->'
                        'http://www.xsfaka.com/liebiao/70FD78F1BA393F09\n\n')
    showinfo(message='欧，这该死的作者怎么可以为了讨口饭吃而这样！文本框中有个饥渴的链接，请不要打开他！',title='警告：软件未激活')
    buttonCancel = tk.Button(formmain, text='激活', command=next2)
    buttonCancel.place(x=450, y=450, width=80, height=30)
formmain.mainloop()