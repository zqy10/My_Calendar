from tkinter import *
import time
import sqlite3

color = {'thistle'      : '#D8BFD8',
         'plum'         : '#DDA0DD',
         'lavenderblush': '#FFF0F5',
         'purple'       : '#800080',
         'pink'         : '#FFC0CB',
         'darkmagenta'  : '#8B008B',
         'silver'       : '#C0C0C0',
         'darkviolet'   : '#9400D3'}

class mainroot:
    def __init__(self):
        #主窗口
        self.main = Tk()
        self.main.title('Calendar')
        self.main.geometry('235x330+200+190')
        self.main.protocol('WM_DELETE_WINDOW',self.close_all)
        self.main_on = True
        #窗口框架
        self.root1 = Frame(self.main,bd=3,width=220,height=300,\
                           highlightbackground=color['thistle'],highlightcolor=color['plum'],highlightthickness=5)
        self.root1.grid()
        self.root1_on = True
        #小窗口
        self.add = []      #小窗口存储
        self.num_win = 0   #小窗口计数
    def add_win(self,name,position):  #添加小窗口
        win = Tk()
        win.title(name)
        win.geometry(position)
        win.protocol('WM_DELETE_WINDOW',self.clear_win)
        self.add.append([win,True])   # win_on=True
        self.num_win += 1
    def del_win(self,number):     #清除指定小窗口
        self.add[number][1]=False
        self.add[number][0].destroy()
        del self.add[number]
        self.num_win -= 1
    def close_all(self):     #清除所有窗口
        for i in self.add:
            if i[1] == True:
                i[0].destroy()
        self.root1.destroy()
        self.root1_on = False
        self.main.destroy()
        self.main_on = False
    def clear_win(self):    #清除所有小窗口
        for i in range(len(self.add)):
            if self.add[i][1] == True:
                self.add[i][0].destroy()
                self.num_win-=1
                del self.add[i]

class button:  
    def __init__(self,main_root,k,m,y,i,j,h):  #k:day , h:add color , i,j:position
        root = main_root.root1
        self.day=str(k)
        self.month=str(m)
        self.year=str(y)
        if k==0:
            self.bt = Button(root,text='',bg=color['lavenderblush'],height=1,width=2)
        else:
            self.bt = Button(root,text=str(k),command = self.enter,fg='#800080',bg='#FFF0F5',height=1,width=2)
        if h==1:
            self.bt.config(text=str(k),command=self.enter,fg='#800080',bg='#FFC0CB',height=1,width=2)
        self.bt.grid(row=i,column=j,sticky=E)
    def enter(self):
        #删除上一个小窗口
        if main_root.num_win != 0:
            main_root.del_win(main_root.num_win-1)
        print(self.day,self.month,self.year)  #终端测试点
        #新建小窗口
        main_root.add_win('Schedule','270x300+440+190')
        #数据库操作
        database = sqlite3.connect('data.db')
        cur = database.cursor()
        if len(self.day)==1:
            self.day = '0'+self.day
        if len(self.month)==1:
            self.month = '0'+self.month
        sql = 'select * from schedule where date = '+self.year+self.month+self.day
        sche = cur.execute(sql).fetchall()
        print(sche)    #终端测试点
        show_sche(main_root.add[main_root.num_win-1][0],sche,self.year+self.month+self.day)
        cur.close()
        database.commit()
        database.close()

def gettime(): #时钟
    timestr = time.strftime('%Y-%m-%d %H:%M:%S')
    lb2.configure(text=timestr)
    root.after(1000,gettime)   #每隔1秒调用一次gettime
    
def isrun(y): #闰年判定
    if((y%4==0 and y%100!=0) or y%400==0):
        return 1
    else:
        return 0

def getcal():   #月历输出
    main_root.clear_win()
    if en1.get() == '':
        date = time.strftime('%Y.%m.%d').split('.')
    else:
        date = en1.get().split('.')
    year = date[0]
    month = date[1]
    print(year,month,date)
    md=[31,28,31,30,31,30,31,31,30,31,30,31]
    week=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    mo=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    yd=365
    year = int(year)
    month = int(month)
    w=0
    for y in range(1900,year+1):
        if isrun(y):
            md[1] = 29
            yd=366
        else:
            md[1]=28
            yd=365
        if y!=year:
            w+=yd%7
    for m in range(month-1):
        w+=md[m]%7
    w%=7
    Label(root,text='',height=1,width=3).grid(row=4,column=0)
    for k in range(7):
        Label(root,text=week[k],height=1,width=3,fg='#8B008B').grid(row=4,column=k+1)
    for k in range(3):
        Label(root,text=mo[month-1][k],height=1,width=2,fg='#8B008B',font=('',14)).grid(row=6+k,column=0)
    for k in range(w):
        button(main_root,0,0,0,5,k+1,0)
    for k in range(md[month-1]):
        if k+1==int(date[2]):
            button(main_root,k+1,month,year,5+(k+w)//7,(k+w)%7+1,1)
        else:
            button(main_root,k+1,month,year,5+(k+w)//7,(k+w)%7+1,0)
    for k in range(w+md[month-1],42):
        button(main_root,0,0,0,5+k//7,k%7+1,0)

'''
structure of database.db:
    Schedule:
        date: 19000101
        time: 1530
        txt : text
        addition: blob
'''       
def show_sche(win,sche,date):  #小窗口展示函数
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    term_num=0
    lb4 = Label(win,text=year+'.'+month+'.'+day,relief=RAISED,width=38)
    lb4.grid(row=0,column=0,columnspan=2)
    win1 = Frame(win,bd=3,width = 110,height=150,\
                 highlightcolor = color['plum'],highlightbackground=color['thistle'],highlightthickness=5)
    win1.grid(row=1,column=0,sticky=N)
    win2 = Frame(win,bd=3,width = 158,height = 200,\
                highlightcolor = color['plum'],highlightbackground=color['plum'],highlightthickness=5)
    win2.grid(row=1,column=1,sticky=W)
    if sche == []:
        pass
    else:
        k=1
        sb = Scrollbar(win)
        sb.grid(row = 0 ,column=2,sticky=S+W+E+N,rowspan=3)
        for term in sche:
            term_num+=1
            strtime = str(term[1])[0:2]+':'+str(term[1])[2:4]
            while k<=term_num:
                Label(win,width=10,height = 2,text='Schedule '+str(k),\
                      fg = color['darkviolet'],font=('',12)).grid(row=k,column=0)
                k+=1
            txt1 = Text(win,width=19,height=1)
            txt1.insert('insert',strtime)
            txt1.grid(row=1,column=1)
            txt2 = Text(win,width = 19 ,height = 15)
            txt2.insert('insert',term[2])
            txt2.grid(row=2,column=1)
        
if __name__ =='__main__':
    #主窗口实例化
    main_root = mainroot()
    root = main_root.root1
    #标题栏
    lb1 = Label(root,text='CALENDAR',font=('',15),relief=RAISED,width=10,fg=color['darkviolet'],bg=color['silver'])
    lb1.grid(row=0,column=0,columnspan=8)
    #时钟栏
    lb2 = Label(root,text='',relief = RAISED,width=30)
    gettime()
    lb2.grid(row=1,column=0,sticky=W,columnspan=8)
    #输入窗
    lb3 = Label(root,text='DATE:',width=10)
    lb3.grid(row=2,column=0,columnspan=4,sticky=E)
    en1 = Entry(root,width=10)
    en1.grid(row=2,column=4,columnspan=4,sticky=W)
    #提交按钮
    bt1 = Button(root,text='submit',command=getcal,bg='#C0C0C0')
    bt1.grid(row=3,columnspan=8)
    main_root.main.mainloop()