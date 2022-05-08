from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter.ttk import Combobox
from database import *
import tkinter.simpledialog as simpledialog


class Update:
    def __init__(self, master):
        self.window = master
        self.window = Tk()
        super().__init__()
        self.window.geometry('1000x600')
        self.window.resizable(False, False)
        self.window.title('修改学生信息')
        self.window.config(bg='#F0F0F0')
        self.frame3 = Frame(self.window, width=900, height=550, bg='#F0F0F0')
        self.frame3.pack()
        self.update_window()

    def update_window(self):
        """更新学生信息"""
        Label(self.frame3, text='修改学生信息', font=('隶书', 20), bg='white',
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
        self.table.heading('学号', text='学号')
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

        Button(self.frame3, text='刷新显示', width=10, height=1,command=self.show_all) \
            .place(x=760, y=100, width=100, height=40)
        # 将查询按钮写为类方法,便于在其他类中调用
        self.btn_name = Button(self.frame3, text='点击修改', width=10, height=1,command=self.update_info)
        self.btn_name.place(x=760, y=190, width=100, height=40)
        self.btn_name = Button(self.frame3, text='退出', width=10, height=1,command=self.window.quit)
        self.btn_name.place(x=760, y=280, width=100, height=40)
        self.show_all() # 初始化查询所有学生信息

    def show_all(self):
        # 查询全部学生信息
        with open('config.ini', 'r') as f:
            db_info = f.readlines()
        db_info = [i.strip() for i in db_info]
        # 连接数据库,创建DataBase对象实例
        conn = Database(db_info[0],
                        int(db_info[1]),
                        db_info[2],
                        db_info[3],
                        )
        data = conn.query_all()  # DataBase类中的query_all方法,返回查询结果，以二维元组的形式返回
        # 将查询结果插入表格,以显示在表格中,每次操作前先清空表格
        self.table.delete(*self.table.get_children())
        for i in data:
            self.table.insert('', 'end', values=i)

    def update_info(self):
        # 修改学生信息
        self.window=Tk()
        self.window.title('修改学生信息')
        self.window.geometry('600x500')
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
        if result:
            with open('config.ini', 'r') as f:
                db_info = f.readlines()
            db_info = [i.strip() for i in db_info]
            # 连接数据库,创建DataBase对象实例
            conn = Database(db_info[0],
                            int(db_info[1]),
                            db_info[2],
                            db_info[3],
                            )
            try:
                conn.update_id(result, item_text[0]) # 修改学号
                self.show_all() # 显示修改后的信息
            except Exception as e:
                pass


    def update_name(self):
        # 修改姓名
        result=simpledialog.askstring('修改姓名', '请输入新的姓名',
                                       initialvalue=self.name,
                                       parent=self.window,
                                       )
        if result:
            with open('config.ini', 'r') as f:
                db_info = f.readlines()
            db_info = [i.strip() for i in db_info]
            # 连接数据库,创建DataBase对象实例
            conn = Database(db_info[0],
                            int(db_info[1]),
                            db_info[2],
                            db_info[3],
                            )
            conn.update_name(result, self.id) # 修改姓名
            self.show_all()

    def update_gender(self):
        # 修改性别
        result = simpledialog.askstring('修改年龄', '请输入新的年龄',
                                        initialvalue=self.gender,
                                        parent=self.window,
                                        )
        if result:
            with open('config.ini', 'r') as f:
                db_info = f.readlines()
            db_info = [i.strip() for i in db_info]
            # 连接数据库,创建DataBase对象实例
            conn = Database(db_info[0],
                            int(db_info[1]),
                            db_info[2],
                            db_info[3],
                            )
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
            with open('config.ini', 'r') as f:
                db_info = f.readlines()
            db_info = [i.strip() for i in db_info]
            # 连接数据库,创建DataBase对象实例
            conn = Database(db_info[0],
                            int(db_info[1]),
                            db_info[2],
                            db_info[3],
                            )
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
            with open('config.ini', 'r') as f:
                db_info = f.readlines()
            db_info = [i.strip() for i in db_info]
            # 连接数据库,创建DataBase对象实例
            conn = Database(db_info[0],
                            int(db_info[1]),
                            db_info[2],
                            db_info[3],
                            )
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
            with open('config.ini', 'r') as f:
                db_info = f.readlines()
            db_info = [i.strip() for i in db_info]
            # 连接数据库,创建DataBase对象实例
            conn = Database(db_info[0],
                            int(db_info[1]),
                            db_info[2],
                            db_info[3],
                            )
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
            with open('config.ini', 'r') as f:
                db_info = f.readlines()
            db_info = [i.strip() for i in db_info]
            # 连接数据库,创建DataBase对象实例
            conn = Database(db_info[0],
                            int(db_info[1]),
                            db_info[2],
                            db_info[3],
                            )
            conn.update_class(result, self.id) # 修改班级
            self.show_all()

    def update_all(self):
        # 修改全部
        text=[self.id,self.name, self.gender,self.age, self.college, self.major, self.class_]
        text2=['学号','姓名','性别','年龄','学院','专业','班级']
        result=[0]*7
        for i in range(7):
            result[i]=simpledialog.askstring('修改全部', '请输入新的'+text2[i],
                                           initialvalue=text[i],
                                           parent=self.window,
                                           )
        if result:
            with open('config.ini', 'r') as f:
                db_info = f.readlines()
            db_info = [i.strip() for i in db_info]
            # 连接数据库,创建DataBase对象实例
            conn = Database(db_info[0],
                            int(db_info[1]),
                            db_info[2],
                            db_info[3],
                            )
            conn.update_all(result[0],result[1],result[2],result[3],result[4],result[5],result[6],self.id) # 修改全部
            self.show_all()

