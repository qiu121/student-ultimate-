from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from database import *
from home import *


class Query:
    def __init__(self, master=None):
        self.window = master
        super().__init__()
        self.query_window()

    def query_window(self):
        # 创建查询窗口
        self.window = Tk()
        self.window.title('查询')
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry('%dx%d+%d-%d' % (250, 200, (screen_width - 250) / 2, (screen_height - 200) / 2))
        # self.window.geometry('250x200')
        self.window.resizable(False, False)
        self.frame4 = Frame(self.window)
        self.frame4.place(x=0, y=0, width=600, height=400)
        # 创建两个按钮
        self.btn_id = Button(self.frame4, text='学号查询', width=10, height=1, command=self.query_id)
        self.btn_id.place(x=70, y=40, width=100, height=40)
        self.btn_name = Button(self.frame4, text='姓名查询', width=10, height=1, command=self.query_name)
        self.btn_name.place(x=70,y=100, width=100, height=40)


    def query_id(self):
        """学号查询"""
        # 设置查询按钮点击之后禁用，防止重复点击出现多个窗口
        self.frame4.destroy()
        self.window.title('学号查询')
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry('%dx%d+%d-%d' % (600, 400, (screen_width - 600) / 2, (screen_height - 400) / 2))
        self.window.resizable(False, False)
        self.window.configure(background='white')
        self.frame4 = Frame(self.window, bg='#F0F0F0')
        self.frame4.place(x=0, y=0, width=800, height=500)
        # 创建查询窗口的标题
        Label(self.frame4, text='学号查询', font=('仿宋', 20), bg='#F0F0F0').place(x=250, y=10)
        Label(self.frame4, text='请输入学号', font=('微软雅黑', 12), bg='#F0F0F0').place(x=100, y=80)
        # 创建查询窗口的输入框
        self.entry_id = Entry(self.frame4, font=('微软雅黑', 12), width=20)
        self.entry_id.place(x=230, y=80)
        # 创建查询窗口的查询按钮
        Button(self.frame4, text='模糊查询', width=10, height=1, command=self.query_regexp_id) \
            .place(x=250, y=190, width=100, height=40)
        Button(self.frame4, text='精准查询', width=10, height=1, command=self.query_exact_id) \
            .place(x=250, y=250, width=100, height=40)
        # 创建查询窗口的重置按钮
        Button(self.frame4, text='重置', width=10, height=1,
               command=lambda: self.entry_id.delete(0, END)) \
            .place(x=250, y=310, width=100, height=40)
        self.window.mainloop()


    def query_name(self):
        """姓名查询"""
        # 设置查询按钮点击之后禁用，防止重复点击出现多个窗口
        self.frame4.destroy()
        self.window.title('姓名查询')
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry('%dx%d+%d-%d' % (600, 400, (screen_width - 600) / 2, (screen_height - 400) / 2))
        self.window.resizable(False, False)
        self.window.configure(background='white')
        self.frame4 = Frame(self.window, bg='#F0F0F0')
        self.frame4.place(x=0, y=0, width=800, height=500)

        # 创建查询窗口的标题
        Label(self.frame4, text='姓名查询', font=('仿宋', 20), bg='#F0F0F0').place(x=250, y=10)
        Label(self.frame4, text='请输入姓名', font=('微软雅黑', 12), bg='#F0F0F0').place(x=100, y=80)

        # 创建查询窗口的输入框
        self.entry_name = Entry(self.frame4, font=('微软雅黑', 12), width=20)
        self.entry_name.place(x=230, y=80)

        # 创建查询窗口的查询按钮
        Button(self.frame4, text='查询', width=10, height=1, command=self.query_exact_name) \
            .place(x=250, y=200, width=100, height=40)

        # 创建查询窗口的重置按钮
        Button(self.frame4, text='重置', width=10, height=1,
               command=lambda: self.entry_name.delete(0, END)) \
            .place(x=250, y=280, width=100, height=40)
        self.window.mainloop()

    def query_exact_name(self):
        """精准查询学生信息"""
        # 获取输入的姓名
        self.entry_name.focus()
        info = self.entry_name.get()
        # 调用database模块，使用其中的Database类，连接数据库
        con1 = Database()
        # 先判断是否输入为空，如果为空，则提示用户输入
        if info == '':
            messagebox.showinfo('提示', '请输入姓名')
        # 如果输入不为空，则判断是否查有此数据
        else:
            # 查询为空时，将父窗口的查询button状态改为可用
            data = con1.query_name_exact(info)  # DataBase类中的query_name_exact方法,返回一条查询结果，以元组的形式返回
            # if not data:  # 查询为空，返回False
            #     self.btn_id["state"] = NORMAL
            if data:  # 查询成功,将查询到的数据显示在界面
                # 每次操作前先清空表格

                self.table.delete(*self.table.get_children())
                self.table.insert('', 'end', values=data)
                # with open('query.txt','w') as f:
                #     f.write(str(data))


    def query_exact_id(self):
        """精准查询学生信息"""
        # 获取输入的学号
        self.entry_id.focus()
        info = self.entry_id.get()
        # 连接数据库,创建DataBase对象实例
        con1 = Database()
        # 先判断是否输入为空，如果为空，则提示用户输入
        if info == '':
            messagebox.showinfo('提示', '请输入学号')
        # 如果输入不为空，则判断是否查有此数据
        else:
            # 查询为空时，将父窗口的查询button状态改为可用
            data = con1.query_id_exact(info)  # DataBase类中的query_id_exact方法,返回一条查询结果，以元组的形式返回
            # if not data:  # 查询为空，返回False
            #     self.btn_id["state"] = NORMAL
            if data:  # 查询成功,将查询到的数据显示在界面
                # 每次操作前先清空表格
                self.window.destroy()
                self.btn_id["state"] = NORMAL
                self.table.delete(*self.table.get_children())
                self.table.insert('', 'end', values=data)

    def query_regexp_id(self):
        """模糊查询学生信息"""
        # 获取输入的学号
        self.entry_id.focus()
        info = self.entry_id.get()
        # 连接数据库,创建DataBase对象实例
        con2 = Database()
        # 判断输入是否为空
        if info == '':
            messagebox.showinfo('提示', '请输入学号片段')
        else:
            # 查询为空时，将父窗口的查询button状态改为可用
            data, num = con2.query_id_regexp(info)  # DataBase类中的query_id_regexp方法,，以二维元组的形式返回返回多条查询结果,并返回查询条数
            if data:  # 查询成功,将查询到的数据显示在界面
                # 每次操作前先清空表格
                # self.window.destroy()
                # self.table.delete(*self.table.get_children())
                # 得到的是二维元组，一个元组元素就是一条学生信息
                for i in range(num):
                    self.table.insert('', 'end', values=data[i])

