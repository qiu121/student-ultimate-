from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter.ttk import Combobox
from database import *
import tkinter.simpledialog as simpledialog
# 简单的对话框，用于获取用户输入


class Update:
    def __init__(self, master):
        self.window = master
        super().__init__()
        self.update_info()

    # def update_window(self):
    #     """更新学生信息"""



    def update_info(self):
        # 修改学生信息
        self.window=Tk()
        self.window.title('修改学生信息')
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry('%dx%d+%d+%d' % (600, 500, screen_width / 2 - 300, screen_height / 2 - 250))
        # self.window.geometry('600x500')
        self.window.resizable(False, False)
        self.window.configure(background='white')
        self.frame4 = Frame(self.window, bg='#F0F0F0')
        self.frame4.place(x=0, y=0, width=800, height=500)

        # 添加四行按钮，每行两个按钮
        text=['修改学号','修改姓名','修改性别','修改年龄','修改学院','修改专业','修改班级','全部修改']
        for i in range(4):
            for j in range(2):
                self.btn_uptate=Button(self.frame4, text=text[i*2+j], width=10, height=1)
                self.btn_uptate.place(x=180+j*140, y=80+i*100, width=100, height=40)
                # 点击修改按钮前，先判断是否选中行
                self.btn_uptate.bind('<Button-1>', self.update_click)

    def update_click(self,event):
        # 判断是否选中表格中的某一行
        if self.table.selection():
            # 获取选中行的行号
            row = self.table.selection()[0]
            # 获取选中行的学号,姓名,性别,年龄,学院,专业,班级,为后续修改提供预选信息
            self.id = self.table.item(row, 'values')[0]
            self.name = self.table.item(row, 'values')[1]
            self.gender = self.table.item(row, 'values')[2]
            self.age = self.table.item(row, 'values')[3]
            self.college = self.table.item(row, 'values')[4]
            self.major = self.table.item(row, 'values')[5]
            self.class_ = self.table.item(row, 'values')[6]
            if event.widget.cget('text') == '修改学号':
                self.update_id()
            elif event.widget.cget('text') == '修改姓名':
                self.update_name()
            elif event.widget.cget('text') == '修改性别':
                self.update_gender()
            elif event.widget.cget('text') == '修改年龄':
                self.update_age()
            elif event.widget.cget('text') == '修改学院':
                self.update_college()
            elif event.widget.cget('text') == '修改专业':
                self.update_major()
            elif event.widget.cget('text') == '修改班级':
                self.update_class()
            elif event.widget.cget('text') == '全部修改':
                self.update_all()
        else:
            messagebox.showinfo('提示', '请选中表格中的一行')


    def update_id(self):
        # 修改学号,设置为获取字符串类型
        # 获取所选择的行的学生信息
        result=simpledialog.askstring('修改学号', '请输入新的学号',
                                       initialvalue=self.id,
                                       parent=self.window,
                                       )
        # print(result)
        # 判断是否输入了新的学号，如果没有输入，则不修改
        if result:
            # 连接数据库,创建DataBase对象实例
            conn = Database()
            # 调用数据库类Database的update_id方法，修改学号
            conn.update_id(result, self.id) # 修改学号
            self.show_all() # 显示修改后的信息


    def update_name(self):
        # 修改姓名
        result=simpledialog.askstring('修改姓名', '请输入新的姓名',
                                       initialvalue=self.name,
                                       parent=self.window,
                                       )
        if result:
            # 连接数据库,创建DataBase对象实例
            conn = Database()
            conn.update_name(result, self.id) # 修改姓名
            self.show_all()

    def update_gender(self):
        # 修改性别
        result = simpledialog.askstring('修改性别', '请输入新的性别',
                                        initialvalue=self.gender,
                                        parent=self.window,
                                        )
        if result:
            # 连接数据库,创建DataBase对象实例
            conn = Database()
            # 获取选中的行，并获取其中的学号作为查询条件
            conn.update_age(result, self.id)  # 修改年龄
            self.show_all()

    def update_age(self):
        # 修改年龄
        result=simpledialog.askstring('修改年龄', '请输入新的年龄',
                                       initialvalue=self.age,
                                       parent=self.window,
                                       )
        if result:
            # 连接数据库,创建DataBase对象实例
            conn = Database()
            # 获取选中的行，并获取其中的学号作为查询条件
            conn.update_age(result, self.id) # 修改年龄
            self.show_all()

    def update_college(self):
        # 修改学院
        result=simpledialog.askstring('修改学院', '请输入新的学院',
                                       initialvalue=self.college,
                                       parent=self.window,
                                       )
        if result:
            # 连接数据库,创建DataBase对象实例
            conn = Database()
            # 获取选中的行，并获取其中的学号作为查询条件
            conn.update_college(result, self.id) # 修改学院
            self.show_all()

    def update_major(self):
        # 修改专业
        result=simpledialog.askstring('修改专业', '请输入新的专业',
                                       initialvalue=self.major,
                                       parent=self.window,
                                       )
        if result:
            # 连接数据库,创建DataBase对象实例
            conn = Database()
            # 获取选中的行，并获取其中的学号作为查询条件
            conn.update_major(result, self.id) # 修改专业
            self.show_all()

    def update_class(self):
        # 修改班级
        result=simpledialog.askstring('修改班级', '请输入新的班级',
                                       initialvalue=self.class_,
                                       parent=self.window,
                                       )
        if result:
            # 连接数据库,创建DataBase对象实例
            conn = Database()
            conn.update_class(result, self.id) # 修改班级
            self.show_all()

    def update_all(self):
        # 修改全部
        text=[self.id,self.name, self.gender,self.age, self.college, self.major, self.class_]
        text2=['学号','姓名','性别','年龄','学院','专业','班级']
        result=[0]*7
        for i in range(7):
            result[i]=simpledialog.askstring('修改个人信息', '请输入新的'+text2[i],
                                           initialvalue=text[i],
                                           parent=self.window,
                                           )
        if result:
            # 连接数据库,创建DataBase对象实例
            conn = Database()
            conn.update_all(result[0],result[1],result[2],result[3],result[4],result[5],result[6],self.id) # 修改全部
            self.show_all()

