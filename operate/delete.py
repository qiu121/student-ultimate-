from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from database import *


class Delete:
    def __init__(self, master=None):
        self.window = master
        self.window = Tk()
        super().__init__()
        self.window.geometry('1000x600')
        self.window.title('删除学生信息')
        self.window.config(bg='#F0F0F0')
        self.window.resizable(False, False)
        self.frame = Frame(self.window, width=900, height=550, bg='#F0F0F0')
        self.frame.pack()

        self.delete_window()

    def delete_window(self):
        """删除窗口"""
        Label(self.frame, text='删除学生信息', font=('隶书', 24), bg='white',
              justify=CENTER).place(x=240, y=25, width=300, height=30)
        Label(self.frame, text='(直接点击记录进行删除)', font=('仿宋', 15),
              justify=CENTER).place(x=550, y=30, width=200, height=30)

        columns = ['学号', '姓名', '性别', '年龄', '学院', '班级', '专业']
        self.table = Treeview(self.frame, height=20, columns=columns,
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
        self.table.heading('学号', text='学号', command=lambda: messagebox.showinfo('提示', '学号'))
        self.table.heading('姓名', text='姓名')
        self.table.heading('性别', text='性别')
        self.table.heading('年龄', text='年龄')
        self.table.heading('学院', text='学院')
        self.table.heading('专业', text='班级')
        self.table.heading('班级', text='专业')

        # 给表格加上竖向滚动条,并且设置滚动条的宽度
        vbar = Scrollbar(self.frame, orient=VERTICAL, command=self.table.yview)
        vbar.place(x=890, y=60, height=480)
        self.table.configure(yscrollcommand=vbar.set)
        self.table.place(x=10, y=80, width=700)
        # self.table.delete(*table.get_children())  # 清空表格

        Button(self.frame, text='显示所有', width=10, height=1, command=self.show_all) \
            .place(x=760, y=130, width=100, height=40)
        # 将删除按钮写为类方法,便于在其他类中调用
        self.btn_del = Button(self.frame, text='点击删除', width=10, height=1, command=self.delete_id)
        self.btn_del.place(x=760, y=220, width=100, height=40)

        Button(self.frame, text='退出', width=10, height=1, command=self.window.quit) \
            .place(x=760, y=310, width=100, height=40)

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

    # self.table.bind('<ButtonRelease-1>', self.treeviewClick)
    # def treeviewClick(self, event):  # 单击事件
    #     for item in self.table.selection():
    #         item_text = self.table.item(item, "values")
            # print(item_text[0])  # 输出所选行的第一列的值
            # self.btn_del.config(command=lambda: self.del_student(item_text[0]))
        # 绑定单击离开事件===========

    def delete_id(self):
        # 删除学生信息
        with open('config.ini', 'r') as f:
            db_info = f.readlines()
        db_info = [i.strip() for i in db_info]
        # 连接数据库,创建DataBase对象实例
        conn = Database(db_info[0],
                        int(db_info[1]),
                        db_info[2],
                        db_info[3],
                        )
        # 获取所选行的学号
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            # print(item_text[0])  # 输出所选行的第一列的值
            # 删除学生信息
            if messagebox.askyesno('提示', '确定删除学号为%s的学生信息吗?' % item_text[0]):
                conn.delete_id(item_text[0])
                self.show_all()
