from tkinter import messagebox
from home import *

import pymysql


class Login:
    def __init__(self, master):
        self.window = master
        screenwidth = self.window.winfo_screenwidth()  # 屏幕宽度
        screenheight = self.window.winfo_screenheight()  # 屏幕高度
        # print(screenwidth, screenheight)
        width = 800  # 设置窗口宽度
        height = 500  # 设置窗口高度
        # 获取屏幕分辨率，使窗口居中显示
        x = (screenwidth - width) // 2
        y = (screenheight - height) // 2
        self.window.geometry('%dx%d+%d-%d' % (width, height, x, y))  # 设置窗口大小及坐标
        self.window.configure(background="white")  # 设置背景颜色
        self.window.title("学生信息管理系统")  # 设置窗口标题
        self.window.attributes("-alpha", 0.9)  # 设置窗口透明度
        self.window.resizable(False, False)  # 窗口大小不可变

        self.window.minsize(800, 500)
        # self.window.maxsize(800, 500)
        # self.window.overrideredirect(True)  # 去掉标题栏

        self.login_page()

    def login_page(self):
        self.frame1 = Frame(self.window)
        self.frame1.pack(fill=BOTH, expand=1)

        Label(self.frame1, text='学生管理系统数据库登录界面', font=('华文行楷', 25),  # bg='white',
              width=30, height=4, fg='blue', justify=CENTER, ).pack()  # bg='white'
        # 创建Label、Entry、Button控件，接收数据库登录的相关参数
        text = ['主机host:', '端口port:', '用户名user:', '密码pwd:']
        for i in range(4):
            if i == 2:
                # 用户名
                Label(self.frame1, text=text[i], font=('黑体', 12)).place(x=240, y=150 + i * 40)
            else:
                Label(self.frame1, text=text[i], font=('黑体', 12)).place(x=260, y=150 + i * 40)

        self.get_db = [StringVar(), IntVar(), StringVar(), StringVar()]

        # host输入框
        self.entry_host = Entry(self.frame1, textvariable=self.get_db[0], width=20, font=('Arial', 12))
        self.entry_host.place(x=340, y=150, width=200, height=28)
        self.get_db[0].set('localhost')  # 设置默认值
        # 端口输入框

        self.entry_port = Entry(self.frame1, textvariable=self.get_db[1], width=20, font=('Arial', 12))
        self.entry_port.place(x=340, y=190, width=200, height=28)
        self.get_db[1].set(3306)  # 设置默认值

        # 用户名输入框
        self.entry_user = Entry(self.frame1, textvariable=self.get_db[2], width=20, font=('Arial', 12))
        self.entry_user.place(x=340, y=230, width=200, height=28)
        self.get_db[2].set('root')  # 设置默认值

        # 密码输入框
        self.entry_pwd = Entry(self.frame1, textvariable=self.get_db[3], show='*', width=20, font=('Arial', 12))
        self.entry_pwd.place(x=340, y=270, width=200, height=28)
        self.get_db[3].set('qiu18279664933')
        self.entry_pwd.focus()

        # 确认按钮
        self.submit = Button(self.frame1, text='登录', font=('黑体', 12), width=10, height=1, activebackground='pink',
                             command=self.login,
                             cursor='hand2')
        self.submit.place(x=280, y=320, width=100, height=30)
        # 重置按钮,设置匿名函数
        self.btn_quit = Button(self.frame1, text='重置', font=('黑体', 12), width=10, height=1, cursor='hand2',
                               command=lambda: [self.entry_host.delete(0, END),
                                                self.entry_port.delete(0, END),
                                                self.entry_user.delete(0, END),
                                                self.entry_pwd.delete(0, END),
                                                self.entry_host.focus()])
        self.btn_quit.place(x=420, y=320, width=100, height=30)

        # 退出按钮
        self.btn_quit = Button(self.frame1, text="退出", font=('黑体', 12), cursor='hand2', command=self.window.quit)
        self.btn_quit.place(x=280, y=370, width=240, height=40)

    def login(self):
        # 获取输入的数据库信息
        host = self.entry_host.get()
        user = self.entry_user.get()
        pwd = self.entry_pwd.get()
        port = self.entry_port.get()
        # print(host, user, pwd, port, sep='\n')
        if host == '' or port == '' or user == '' or pwd == '':
            messagebox.showerror('错误', '请输入完整信息')
        else:
            try:
                # 创建数据库连接
                db = pymysql.connect(host=host, user=user, password=pwd, port=int(port), charset='utf8')
                # 将数据库连接的参数保存为文件,方便后续数据库连接使用
                # 若文件已存在,则覆盖,否则创建
                with open('config.ini', 'w') as f:
                    f.write(host + '\n')
                    f.write(port + '\n')
                    f.write(user + '\n')
                    f.write(pwd + '\n')
                cursor = db.cursor()
                cursor.execute("SELECT VERSION()")
                # 获取执行结果
                data = cursor.fetchone()
                # connect()  # 调用自定义模块的connect函数，连接数据库,操作数据库
                # send()  # 调用自定义模块的send函数，发送数据
                # os.remove('config.ini')  # 删除生成的配置文件

                messagebox.showinfo('提示', '数据库连接成功\n数据库版本：%s' % data)
                self.frame1.destroy()  # 销毁窗口
                Home(self.window)  # 转到home模块，引用其中的类，创建主窗口

                # 关闭数据库连接
                db.close()
            except (pymysql.err.OperationalError, ValueError, Exception) as e:
                messagebox.showerror('错误', '连接失败，请检查信息是否正确!\n' + str(e))
