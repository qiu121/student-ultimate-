from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from database import *


class Query:
    def __init__(self, master=None):
        self.window = master
        self.window = Tk()
        super().__init__()
        self.window.geometry('1000x600')
        self.window.resizable(False, False)
        self.window.title('查询学生信息')
        self.window.config(bg='#F0F0F0')
        self.frame3 = Frame(self.window, width=900, height=550, bg='#F0F0F0')
        self.frame3.pack()
        self.query_window()

    def query_window(self):
        """查询窗口"""
        Label(self.frame3, text='查询学生信息', font=('隶书', 20), bg='white',
              justify=CENTER).place(x=240, y=30, width=300, height=30)

        columns = ['学号', '姓名', '性别', '年龄', '学院', '班级', '专业']
        self.table = Treeview(self.frame3, height=20, columns=columns,
                              selectmode='browse',
                              show='headings',
                              displaycolumns=columns,
                              )

        # 定义各列宽度和对齐方式
        self.table.column('学号', width=110, minwidth=110, anchor='center')
        self.table.column('姓名', width=100, minwidth=100, anchor='center')
        self.table.column('性别', width=50, minwidth=50, anchor='center')
        self.table.column('年龄', width=50, minwidth=50, anchor='center')
        self.table.column('学院', width=110, minwidth=110, anchor='center')
        self.table.column('专业', width=100, minwidth=100, anchor='center')
        self.table.column('班级', width=180, minwidth=180, anchor='center')
        # 设置表头
        self.table.heading('学号', text='学号',command=lambda: messagebox.showinfo('提示', '学号'))
        self.table.heading('姓名', text='姓名')
        self.table.heading('性别', text='性别')
        self.table.heading('年龄', text='年龄')
        self.table.heading('学院', text='学院')
        self.table.heading('专业', text='班级')
        self.table.heading('班级', text='专业')
        # 给表格加上竖向滚动条,并且设置滚动条的宽度
        vbar = Scrollbar(self.frame3, orient=VERTICAL, command=self.table.yview)
        vbar.place(x=890, y=60, height=480)
        self.table.configure(yscrollcommand=vbar.set)
        self.table.place(x=10, y=80, width=700)
        # self.table.delete(*table.get_children())  # 清空表格

        Button(self.frame3, text='查询所有', width=10, height=1, command=self.query_all) \
            .place(x=760, y=130, width=100, height=40)
        # 将查询按钮写为类方法,便于在其他类中调用
        self.btn_id = Button(self.frame3, text='学号查询', width=10, height=1, command=self.query_id)
        self.btn_id.place(x=760, y=220, width=100, height=40)
        self.btn_name = Button(self.frame3, text='姓名查询', width=10, height=1, command=self.query_name)
        self.btn_name.place(x=760, y=310, width=100, height=40)
        Button(self.frame3, text='退出', width=10, height=1, command=self.window.quit) \
            .place(x=760, y=400, width=100, height=40)

    def query_all(self):
        # 查询全部学生信息
        self.btn_id.config(state=NORMAL)  # 将查询按钮可用,解决自行关闭查询窗口后按钮未恢复可用的问题
        self.btn_name.config(state=NORMAL)
        with open('config.ini', 'r') as f:
            db_info = f.readlines()
        db_info = [i.strip() for i in db_info]
        # 连接数据库,创建DataBase对象实例
        con = Database(db_info[0],
                       int(db_info[1]),
                       db_info[2],
                       db_info[3],
                       )
        data = con.query_all()  # DataBase类中的query_all方法,返回查询结果，以二维元组的形式返回
        # 将查询结果插入表格,以显示在表格中,每次操作前先清空表格
        self.table.delete(*self.table.get_children())
        for i in data:
            self.table.insert('', 'end', values=i)

    def query_id(self):
        """学号查询"""
        # 设置查询按钮点击之后禁用，防止重复点击出现多个窗口
        self.btn_id["state"] = DISABLED
        self.window = Tk()
        self.window.title('学号查询')
        self.window.geometry('600x400')
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
        self.btn_name["state"] = DISABLED
        self.window = Tk()
        self.window.title('姓名查询')
        self.window.geometry('600x400')
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
        pass
        """精准查询学生信息"""
        # 获取输入的姓名
        self.entry_name.focus()
        info = self.entry_name.get()
        # 获取配置文件中的数据库信息
        with open('config.ini', 'r') as f:
            db_info = f.readlines()
        db_info = [i.strip() for i in db_info]
        # 连接数据库,创建DataBase对象实例
        con1 = Database(db_info[0],
                        int(db_info[1]),
                        db_info[2],
                        db_info[3],
                        )

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
                self.window.destroy()
                self.btn_id["state"] = NORMAL
                self.table.delete(*self.table.get_children())
                self.table.insert('', 'end', values=data)

    def query_exact_id(self):
        """精准查询学生信息"""
        # 获取输入的学号
        self.entry_id.focus()
        info = self.entry_id.get()
        # 获取配置文件中的数据库信息
        with open('config.ini', 'r') as f:
            db_info = f.readlines()
        db_info = [i.strip() for i in db_info]
        # 连接数据库,创建DataBase对象实例
        con1 = Database(db_info[0],
                        int(db_info[1]),
                        db_info[2],
                        db_info[3],
                        )

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
        # 获取配置文件中的数据库信息
        with open('config.ini', 'r') as f:
            db_info = f.readlines()
        db_info = [i.strip() for i in db_info]
        # 连接数据库,创建DataBase对象实例
        con2 = Database(db_info[0],
                        int(db_info[1]),
                        db_info[2],
                        db_info[3],
                        )
        # 判断输入是否为空
        if info == '':
            messagebox.showinfo('提示', '请输入学号片段')
        else:
            # 查询为空时，将父窗口的查询button状态改为可用
            data, num = con2.query_id_regexp(info)  # DataBase类中的query_id_regexp方法,，以二维元组的形式返回返回多条查询结果,并返回查询条数
            if data:  # 查询成功,将查询到的数据显示在界面
                # 每次操作前先清空表格
                self.window.destroy()
                self.btn_id["state"] = NORMAL
                self.table.delete(*self.table.get_children())
                for i in range(num):
                    self.table.insert('', 'end', values=data[i])
