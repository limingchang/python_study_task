# -*- coding: utf-8 -*-
__author__ = 'Mc.Lee'
import sys, os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path)

from multiprocessing import Process
from core import client_class
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import tkinter.simpledialog
import hashlib,time

class Application(object):
    def __init__(self,):
        #Frame.__init__(self, master)
        #self.pack()
        #self.grid()
        self.master = Tk()
        self.master['bg']='#F0FFFF'#设置背景颜色
        self.master.title('FTP-Client')
        self.center_window(self.master)#设置窗口大小并居中
        self.master.resizable(False, False)#禁止改变窗口大小

        self.Is_Login = False
        self.User_Info = {}
        self.Login_Form()
        if self.Is_Login:
            self.SubForm.withdraw()
        else:
            #pass
            self.master.withdraw()


    def Create_Client_Process(self):
        '''
        创建客户端进程
        :return:
        '''
        def Client():
            self.Client = client_class.Ftp_Client()
        server_process = Process(target=Client)  # 创建进程
        server_process.daemon = True
        server_process.start()


    def Auth(self):
        '''
        登录验证
        :return:
        '''
        username = self.Username_Entry.get()
        password = self.Password_Entry.get()
        password = hashlib.sha1(password.encode("utf8")).hexdigest()
        if username =='' or password == '':
            self.Message('错误','用户名/密码不能为空！',type='error')
        else:
            Client = client_class.Ftp_Client()
            auth_res = Client.Auth(username,password)
            if auth_res['auth']:
                self.User_Info = auth_res['info']
                self.SubForm.withdraw()
                self.SubForm.destroy()
                self.master.update()
                self.master.deiconify()
                self.CreateWidgets()#验证成功才创建主窗体框架
                self.Is_Login = True
                #print('验证通过')
            else:
                self.Message('登录失败',auth_res['info'],type='error')
            del Client



    def Login_Form(self):
        self.SubForm = Toplevel(self.master)
        self.SubForm.title('用户登录')
        username_label = Label(self.SubForm,text='用户名:',font=("宋体", 12, "bold"))
        username_label.place(in_=self.SubForm,relx=0, rely=0,x=5,y=20, width=80, height=35, anchor=W)
        #user_label.grid(row=0,column=0)
        self.Username_Entry = Entry(self.SubForm,font=("宋体", 12, "bold"))
        self.Username_Entry.place(in_=self.SubForm,relx=0, rely=0,x=90,y=20, width=200, height=35, anchor=W)
        pass_label = Label(self.SubForm, text='密  码:',font=("宋体", 12, "bold"))
        pass_label.place(in_=self.SubForm,relx=0, rely=0,x=5,y=60, width=80, height=35, anchor=W)
        self.Password_Entry = Entry(self.SubForm,show = '*',font=("宋体", 12, "bold"))
        self.Password_Entry.place(in_=self.SubForm,relx=0, rely=0,x=90,y=60, width=200, height=35, anchor=W)
        login_button = Button(self.SubForm,text='登录',anchor=CENTER,command=self.Auth,font=("宋体", 12, "bold"))
        login_button.place(in_=self.SubForm,relx=0, rely=0,x=75,y=100, width=50, height=35, anchor=W)
        cancle_button = Button(self.SubForm,text='取消',anchor=CENTER,command=self.close,font=("宋体", 12, "bold"))
        cancle_button.place(in_=self.SubForm,relx=0, rely=0,x=170,y=100, width=50, height=35, anchor=W)
        self.center_window(self.SubForm,295,120)
        self.SubForm.resizable(False, False)
        self.SubForm.protocol("WM_DELETE_WINDOW", self.close)#绑定关闭按钮事件


    def close(self):
        exit()

    def CreateWidgets(self):
        # 创建提示栏UI框架
        self.Create_Tips_Frame()
        #创建上传文件UI框架
        self.Create_UploadFile_Frame()
        #创建下载文件UI框架
        self.Create_DownloadFile_Frame()
        #检测连接和服务器平台
        Client = client_class.Ftp_Client()
        Client.handle()
        if Client.Chk_Platform == 'nt':
             self.Tips_Label['text']='服务器[基于Windows]连接正常'
        else:
             self.Tips_Label['text'] = '服务器[基于Linux]连接正常'
        Client.client.close()


    def Create_Tips_Frame(self):
        '''
        创建提示栏UI框架
        :return:
        '''
        frame_width = 500
        frame_height = 35
        Tips_Frame = Frame(self.master ,bg='#87CEFF')
        Tips_Frame.place(x=5, y=390, height=frame_height, width=frame_width)
        self.Tips_Label = Label(Tips_Frame,text='提示信息',anchor=W,bg='#87CEFF',fg='#FCFCFC',font=("宋体", 12, "bold"))
        self.Tips_Label.place(in_=Tips_Frame,relx=0, rely=0,x=5,y=20, width=490, height=25, anchor=W)


    def Create_DownloadFile_Frame(self):
        '''
        创建下载文件UI框架
        :return:
        '''
        frame_width = 500
        frame_height = 250
        DownloadFile_Frame = Frame(self.master, bg='#87CEFF')
        DownloadFile_Frame.place(x=5, y=135, height=frame_height, width=frame_width)
        name_label = Label(DownloadFile_Frame,text='下载文件：',bg='#87CEFF',fg='#FF4040',font=("宋体", 12, "bold"))
        name_label.place(in_=DownloadFile_Frame,relx=0, rely=0,x=5,y=15, width=100, height=25, anchor=W)
        tips_label = Label(DownloadFile_Frame,text='双击进入下层目录，双击顶层目录返回.',bg='#87CEFF',fg='#4169E1',font=("宋体", 10, "bold"))
        tips_label.place(in_=DownloadFile_Frame,relx=0, rely=0,x=500,y=15, width=320, height=25, anchor=E)
        self.Create_FileList(DownloadFile_Frame)#创建文件列表控件
        #创建新建目录控件模块
        dir_name_label = Label(DownloadFile_Frame,text='新目录名：',bg='#87CEFF',fg='#FF4040',font=("宋体", 10, "bold"))
        dir_name_label.place(in_=DownloadFile_Frame,relx=0, rely=0,x=210,y=50, width=100, height=25, anchor=W)
        self.new_dir_entry = Entry(DownloadFile_Frame)
        self.new_dir_entry.place(in_=DownloadFile_Frame,relx=0, rely=0,x=295,y=50, width=120, height=25, anchor=W)
        self.new_dir_button = Button(DownloadFile_Frame, text='新建目录', command=self.Create_Dir,bg='#CD69C9',fg='#FCFCFC',font=("宋体", 10, "bold"))
        self.new_dir_button.place(in_=DownloadFile_Frame,relx=0, rely=0,x=210,y=90, width=100, height=25, anchor=W)
        name_label = Label(DownloadFile_Frame, text='已选择：', anchor=W,bg='#87CEFF', fg='#B23AEE',font=("宋体", 10, "bold"))
        name_label.place(in_=DownloadFile_Frame, relx=0, rely=0, x=210, y=130, width=250, height=25, anchor=W)
        self.download_filename_label = Label(DownloadFile_Frame, text='双击选中列表框中要下载的文件', bg='#87CEFF', fg='#B23AEE', font=("宋体", 10, "bold"),anchor=W)
        self.download_filename_label.place(in_=DownloadFile_Frame, relx=0, rely=0, x=210, y=160, width=280, height=25, anchor=W)

        self.download_button = Button(DownloadFile_Frame, text='点击下载', command=self.get_file,bg='#CD69C9',fg='#FCFCFC',font=("宋体", 10, "bold"))
        self.download_button.place(in_=DownloadFile_Frame, relx=0, rely=0, x=210, y=200, width=280, height=25, anchor=W)
        # 进度条标签
        self.get_blok_lable = Label(DownloadFile_Frame, text='')  # 进度条标签
        self.get_blok_lable.place(in_=DownloadFile_Frame, relx=0, rely=0, x=5, y=220, width=1, height=25)


    def Create_UploadFile_Frame(self):
        '''
        创建上传文件UI框架
        :return:
        '''
        frame_width = 500
        frame_height = 125
        UploadFile_Frame = Frame(self.master,bg='#87CEFF')
        UploadFile_Frame.place(x=5,y=5,height=frame_height,width=frame_width)
        name_label = Label(UploadFile_Frame, text="上传文件：",bg='#87CEFF',fg='#FF4040',font=("宋体", 12, "bold"))
        name_label.place(in_=UploadFile_Frame,relx=0, rely=0,x=5,y=15, width=100, height=25, anchor=W)
        chose_file_button = Button(self.master, text='1.选择文件',font=("宋体", 12, "bold"), command=self.get_filename,bg='#FFA500',fg='#FCFCFC')
        chose_file_button.place(in_=UploadFile_Frame,relx=0, rely=0,x=200,y=15, width=120, height=25, anchor=W)
        self.filename_label = Label(UploadFile_Frame,text="请单击按钮选择文件...",anchor=W,bg='#87CEFF',fg='#FF4040',font=("宋体", 12, "bold"))
        self.filename_label.place(in_=UploadFile_Frame,relx=0, rely=0,x=5,y=70, width=490, height=25)
        self.put_file_button = Button(UploadFile_Frame, text='2.上传文件',command=self.put_file,fg='#FCFCFC', bg='lightgreen',font=("宋体", 12, "bold"))
        self.put_file_button.place(in_=UploadFile_Frame,relx=0, rely=0,x=375,y=10, width=120, height=60)
        #进度条标签
        self.put_blok_lable = Label(UploadFile_Frame, text='')  # 进度条标签
        self.put_blok_lable.place(in_=UploadFile_Frame,relx=0, rely=0,x=5,y=95,width=1, height=25)



    def Create_FileList(self,DownloadFile_Frame):
        Client = client_class.Ftp_Client()
        self.file_list = Listbox(DownloadFile_Frame, selectmode="browse",bg='#BFEFFF',fg='#8A2BE2',font=("宋体", 12, "bold"))
        #个人家目录,和路径分割符
        self.home_path,self.home_sep = Client.Get_HomePath(self.User_Info['username'])
        #print('个人家目录', self.home_path)
        #系统家目录名
        self.home_name = os.path.basename(os.path.dirname(self.home_path))
        #系统顶层目录
        self.sys_top_dir = os.path.dirname(os.path.dirname(self.home_path))
        #print('系统顶层目录',self.sys_top_dir)
        #个人顶层目录
        self.user_top_dir = self.home_path
        self.DownLoad_File_Path =''
        #print('homepath:',self.home_path)
        del Client
        #Client = client_class.Ftp_Client()

        def add_item(list_path):
            Client = client_class.Ftp_Client()
            #print('add_item:',list_path)
            self.file_list.delete(0, END)
            list1 = Client.Dir_List(list_path)
            #print(type(list_path),'|',list_path)
            top_dir = list_path.replace(self.sys_top_dir+self.home_sep,'')
            self.Tips_Label['text']='当前目录：%s'%top_dir
            list1.insert(0,top_dir)
            for item in list1:
                if list1.index(item) != 0: item = ' ' * 5 + item
                self.file_list.insert(END, item)
            del Client

        add_item(self.home_path)
        self.file_list.place(in_=DownloadFile_Frame,relx=0, rely=0,x=5,y=30, width=200, height=185)

        def printList(event):
            select_item = self.file_list.get(self.file_list.curselection()).strip()
            #print('select_item', select_item)
            Client = client_class.Ftp_Client()
            now_top_dir = self.file_list.get(0).strip()
            if select_item == now_top_dir:
                #如果选的是顶层目录
                select_path = os.path.join(self.sys_top_dir,select_item)
                #print('顶层选择：',select_path)
                #print('-系统顶层目录', self.sys_top_dir)
                if select_path == self.user_top_dir:#如果到达个人顶层目录
                    self.home_path = self.user_top_dir
                    tips_str =os.path.join(self.home_name,self.User_Info['username'])
                    self.Message('提示','您已处于顶层目录：%s'%tips_str,type='info')
                else:
                    self.home_path = os.path.dirname(select_path)
            else:
                select_path = os.path.join(self.sys_top_dir,now_top_dir ,select_item)
                if not Client.Chk_File(select_path):
                    self.home_path = select_path
                    #print('jion:', self.home_path)
                else:
                    self.DownLoad_File_Path = select_path
                    #print('您选择了一个文件:', select_item)
                    self.download_filename_label['text'] = select_item
            #print('select_path',select_path)
            add_item(self.home_path)
            del Client

        self.file_list.bind('<Double-Button-1>', printList)


    def Create_Dir(self):
        will_create_dir = self.file_list.get(0).strip()
        dir_name = self.new_dir_entry.get().strip()
        if dir_name == '':
            self.Message('错误','请输入文件夹名',type='error')
        else:
            msg_str = '将在%s下创建%s'%(will_create_dir,dir_name)
            msg = tkinter.messagebox.askokcancel("确认？", msg_str)
            #print(msg)
            if msg:
                Client = client_class.Ftp_Client()
                res = Client.Create_Dir(will_create_dir,dir_name)
                self.Message('提示',res)
                del Client
            else:
                self.Tips_Label['text'] = '用户取消创建'



    def get_file(self):
        self.download_button['state'] = DISABLED
        self.get_blok_lable['bg'] = '#FCFCFC'
        self.get_blok_lable.place(width=1)
        self.master.update_idletasks()
        if self.DownLoad_File_Path == '':
            self.Message('错误', '您没有选择任何文件！', type='error')
        else:
            Client = client_class.Ftp_Client()
            res = Client.DownLoad_File(self.DownLoad_File_Path,self.master,self.get_blok_lable,490)
            self.Message('提示', res)
            del Client
        self.download_button['state'] = NORMAL

    def put_file(self):
        self.put_file_button['state']=DISABLED
        self.put_blok_lable['bg'] = '#FCFCFC'
        self.put_blok_lable.place(width =1)
        self.master.update_idletasks()
        if self.UpLoad_File_Path == '':
            self.Message('错误','您没有选择任何文件！',type='error')
        else:
            Client = client_class.Ftp_Client()
            save_path = self.file_list.get(0)
            ############################################
            chk_size = Client.Chk_Space(self.User_Info['username'],self.User_Info['space'],self.UpLoad_File_Path)
            if chk_size:
                res = Client.UpLoad_File(self.UpLoad_File_Path,save_path,self.master,self.put_blok_lable,490)
                self.Message('提示',res)
            else:
                self.Message('警告','您的空间配额不足！',type='warning')
            del Client
        self.put_file_button['state']=NORMAL


    def get_filename(self):
        #name = tkinter.simpledialog.askstring('test','123')
        filename = tkinter.filedialog.askopenfilename(filetypes=( ("All files", "*.*"),("Text file", "*.txt*")))
        #print(type(filename))
        if filename == '':
            self.UpLoad_File_Path = ''
            self.filename_label['text'] = '请单击按钮选择文件...'
            self.Tips_Label['text'] = '请选择文件.'
        else:
            self.UpLoad_File_Path = filename
            self.filename_label['text'] = filename
            self.Tips_Label['text'] = '文件将上传到:',self.file_list.get(0)


    def center_window(self,window, width=510, height=430):
        # get screen width and height
        window['width']=width
        window['height']=height
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height/ 2)
        window.geometry('%dx%d+%d+%d' % (width , height, x, y))

    def Message(self,title,tips,type='info'):
        if type == 'info':
            msg = tkinter.messagebox.showinfo(title,tips)
        elif type == 'error':
            msg = tkinter.messagebox.showerror(title, tips)
        elif type == 'warning':
            msg = tkinter.messagebox.showwarning(title, tips)





if __name__ == '__main__':
    app = Application()
    # 设置窗口标题:

    #app.center_window()
    #print(dir(Label()))
    #app.master.
    # 主消息循环:
    app.master.mainloop()
