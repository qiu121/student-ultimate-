from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

from config.college_major import mapping
from database import Database


class Update:
    def __init__(self, master=None, data=None, tag=None):
        # 创建一个新的 Toplevel 窗口
        self.window = Toplevel(master)
        self.data = data
        self._id = tag

        # 使用类属性代替全局变量
        self.get_vars = [StringVar() for _ in range(7)]
        self.entries = [None] * 7

        self.major_dirt = mapping  # 学院与专业关联字典
        self.update_window()  # 构建窗口

    def update_window(self):
        """构建窗口，包含学号、姓名、性别、年龄、学院、专业、班级的输入项"""
        self.frame = Frame(self.window, width=800, height=600, bg='#F0F0F0')
        self.frame.pack()

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry('%dx%d+%d+%d' % (800, 600, screen_width / 2 - 400, screen_height / 2 - 300))
        self.window.resizable(False, False)
        self.window.title("修改学生信息")

        Label(self.frame, text='修改学生信息', font=('隶书', 20), justify=CENTER).place(x=250, y=40, width=310,
                                                                                        height=40)

        # 定义各个输入字段
        labels = ['学号', '姓名', '性别', '年龄', '学院', '专业', '班级']

        for i, label in enumerate(labels):
            self.create_field(i, label)

        self.entries[0].focus()  # 设置默认焦点

        # 更新按钮
        self.btn_add = Button(self.frame, text='更新', width=15, height=1, cursor='hand2', font=('黑体', 14))
        self.btn_add.place(x=300, y=450, width=200, height=40)
        self.btn_add.bind('<Button-1>', self.update_click)

        # 重置按钮，重置所有输入
        self.btn_reset = Button(self.frame, text='重置', width=15, height=1, cursor='hand2', font=('黑体', 14),
                                command=self.reset_fields)
        self.btn_reset.place(x=300, y=500, width=200, height=40)

    def create_field(self, i, label_text):
        """根据传入的索引 i 和标签文本生成相应的输入控件"""
        Label(self.frame, text=label_text, font=('隶书', 15), justify=CENTER).place(x=260, y=100 + i * 50, width=100,
                                                                                    height=30)

        # 设置初始值
        self.get_vars[i].set(self.data[i])

        if i == 2:  # 性别单选按钮
            Radiobutton(self.frame, text='男', variable=self.get_vars[i], value='男', font=('隶书', 15),
                        justify=CENTER).place(x=350, y=100 + i * 50, width=50, height=30)
            Radiobutton(self.frame, text='女', variable=self.get_vars[i], value='女', font=('隶书', 15),
                        justify=CENTER).place(x=450, y=100 + i * 50, width=50, height=30)

        elif i == 3:  # 年龄 Spinbox
            Spinbox(self.frame, from_=17, to=24, width=10, font=('隶书', 16), state='readonly', justify=CENTER,
                    textvariable=self.get_vars[i]).place(x=350, y=100 + i * 50, width=160, height=30)

        elif i == 4:  # 学院下拉框
            self.add_college_combobox = Combobox(self.frame, textvariable=self.get_vars[i], state='readonly',
                                                 font=('宋体', 12), justify=CENTER)
            self.add_college_combobox['values'] = list(self.major_dirt.keys())
            self.add_college_combobox.place(x=350, y=100 + i * 50, width=160, height=30)
            self.add_college_combobox.bind("<<ComboboxSelected>>", self.college_major)

        elif i == 5:  # 专业下拉框
            self.add_major_combobox = Combobox(self.frame, textvariable=self.get_vars[i], state='readonly',
                                               font=('宋体', 12), justify=CENTER)
            self.add_major_combobox['values'] = []
            self.add_major_combobox.place(x=350, y=100 + i * 50, width=160, height=30)

        else:  # 默认文本输入框
            self.entries[i] = Entry(self.frame, textvariable=self.get_vars[i], font=('宋体', 15), justify=CENTER)
            self.entries[i].place(x=350, y=100 + i * 50, width=160, height=30)

    def college_major(self, event):
        """根据选择的学院更新专业下拉框"""
        selected_college = self.get_vars[4].get()
        if selected_college in self.major_dirt:
            self.add_major_combobox['values'] = self.major_dirt[selected_college]
            self.add_major_combobox.current(0)  # 默认选择第一个专业
        else:
            self.add_major_combobox['values'] = []  # 若无学院选择，清空专业列表

    def update_click(self, event):
        """点击更新按钮时，校验输入并将数据写入数据库"""
        errors = ['学号不能为空！',
                  '姓名不能为空！',
                  '性别不能为空！',
                  '年龄不能为空！',
                  '学院不能为空！',
                  '专业不能为空！',
                  '班级不能为空！'
                  ]

        for i, var in enumerate(self.get_vars):
            if var.get().strip() == '':
                messagebox.showwarning('提示', errors[i])
                return
            if i == 0 and (len(var.get()) not in (10, 11) or not var.get().isdigit()):
                messagebox.showwarning('提示', '学号格式错误！')
                return

        # 获取更新后的数据并更新数据库
        updated_data = [var.get() for var in self.get_vars]
        con = Database()
        con.update_all(updated_data, self._id)

        self.window.destroy()  # 更新后关闭窗口

    def reset_fields(self):
        """重置输入框，回到传入的数据"""
        for i in range(7):
            self.get_vars[i].set(self.data[i])  # 重置回最初传入的值
        self.entries[0].focus()
