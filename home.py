from tkinter import *
from operate.add import *
from operate.delete import *
from operate.update import *
from operate.query import *
from database import *


# 导入自定义的模块,实现主界面的功能(增删改查)


class Home:
    def __init__(self, master=None):
        self.window = master
        self.window.title('学生信息管理系统主界面')
        super().__init__()
        width = 1000  # 窗口宽
        height = 600  # 窗口高
        screen_width = self.window.winfo_screenwidth()  # 获取屏幕宽
        screen_height = self.window.winfo_screenheight()  # 获取屏幕高
        x = (screen_width - width) / 2  # 设置窗口x坐标
        y = (screen_height - height) / 2  # 设置窗口y坐标
        self.window.geometry('%dx%d+%d-%d' % (width, height, x, y))# 设置窗口大小及坐标,居中显示
        self.window.resizable(False, False)  # 禁止改变窗口大小

        self.main_page()

    def main_page(self,*data):
        """创建主窗口"""

        # 左边：按钮区域，创建一个容器
        self.Pane_left = PanedWindow(width=200, height=600, cursor='hand2')
        self.Pane_left.place(x=10)
        self.Pane_right = PanedWindow(width=800, height=600, cursor='hand2')
        self.Pane_right.place(x=210)

        self.LabelFrame_query = Label(self.Pane_right, text="学生信息管理系统",anchor=CENTER, font=('宋体', 30), width=20, height=2)
        self.LabelFrame_query.place(x=200, y=10)

        # 添加左边功能按钮
        text = ['显示全部', '添加信息', '查询信息', '修改信息', '删除信息', '退出系统']
        for i in range(len(text)):
            self.btn = Button(self.Pane_left, text=text[i], font=('宋体', 15), width=15, height=2)
            self.btn.place(x=40, y=60 + i * 80)
            self.btn.bind('<Button-1>', self.btn_click)

        # 添加右边Treeview,显示学生信息
        columns = ['学号', '姓名', '性别', '年龄', '学院', '班级', '专业']
        self.table = Treeview(self.Pane_right, height=20, columns=columns,
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
        self.table.heading('学号', text='学号')
        self.table.heading('姓名', text='姓名')
        self.table.heading('性别', text='性别')
        self.table.heading('年龄', text='年龄')
        self.table.heading('学院', text='学院')
        self.table.heading('专业', text='班级')
        self.table.heading('班级', text='专业')
        # 给表格加上竖向滚动条,并且设置滚动条的宽度
        vbar = Scrollbar(self.Pane_right, orient=VERTICAL, command=self.table.yview)
        vbar.place(x=730, y=80, height=450)
        self.table.configure(yscrollcommand=vbar.set)
        self.table.place(x=10, y=80, width=700)
        self.table.bind('<ButtonRelease-1>', self.treeviewClick)


    def treeviewClick(self, event):  # 单击事件
        if self.table.selection():
            for item in self.table.selection():
                item_text = self.table.item(item, "values")
            # print(item_text[0])  # 输出所选行的第一列的值
            messagebox.showinfo('提示', '你选择了：%s' % item_text[1])


    def show_all(self):
        """显示全部学生信息"""
        con1 = Database()
        data = con1.query_all()
        self.table.delete(*self.table.get_children())  # 清空表格
        for i in data:
            self.table.insert('', 0, values=i)

    def btn_click(self, event):
        """按钮点击事件"""
        # 调用模块中的类，实现功能
        if event.widget['text'] == '显示全部':
            self.show_all()
        if event.widget['text'] == '添加信息':
            # self.frame2.destroy() # 必须销毁主界面,否则会出现重叠,甚至出现无法获取添加界面的数据(未解决)
            Add()
            # add.add_window()
            pass
        elif event.widget['text'] == '查询信息':
            # self.frame2.destroy()
            # Query(self.window)
            # self.query_window()
            self.query_window()
        elif event.widget['text'] == '修改信息':
            # self.frame2.destroy()
            # Update(self.window)
            # self.update_window()
            self.update_info()
        elif event.widget['text'] == '删除信息':
            # self.frame2.destroy()
            # dele=Delete(self.window)
            # dele.delete_window()
            self.delete_window()
        elif event.widget['text'] == '退出系统':
            self.window.quit()
            # self.frame2.quit()

    def delete_window(self):
        """删除学生信息"""
        # 连接数据库,创建DataBase对象实例
        conn = Database()
        # 判断是否选中行
        if len(self.table.selection()) == 0:
            messagebox.showwarning('警告', '请选择要删除的学生信息')
            return
        # 获取所选行的学号
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            # print(item_text[0])  # 输出所选行的第一列的值
            # 删除学生信息
            if messagebox.askyesno('提示', '确定删除学号为%s的学生信息吗?' % item_text[0]):
                conn.delete_id(item_text[0])
                self.show_all()

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

