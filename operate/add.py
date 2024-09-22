from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

from config.college_major import mapping
from database import Database

# 常量定义
DEFAULT_SEX = '男'
DEFAULT_AGE = '17'
TITLE_FONT = ('隶书', 20)
LABEL_FONT = ('隶书', 15)
BUTTON_FONT = ('黑体', 14)


class Add:
    def __init__(self, master=None):
        # 创建一个新的 Toplevel 窗口
        self.window = Toplevel(master)
        self.create_window()

    def create_window(self):
        """设置窗口布局及内容"""
        self.frame = Frame(self.window, width=800, height=600, bg='#F0F0F0')
        self.frame.pack()

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f'800x600+{int(screen_width / 2 - 400)}+{int(screen_height / 2 - 300)}')
        self.window.resizable(False, False)
        self.window.title("添加学生信息")

        Label(self.frame, text='添加学生信息', font=TITLE_FONT, justify=CENTER).place(x=250, y=40, width=310, height=40)

        # 定义字段标题及变量
        add_title = ['学号', '姓名', '性别', '年龄', '学院', '专业', '班级']
        self.get_values = [StringVar() for _ in range(7)]

        # 初始化学院-专业字典
        self.major_dict = mapping

        # 创建输入字段
        for i, title in enumerate(add_title):
            Label(self.frame, text=title, font=LABEL_FONT, justify=CENTER).place(x=260, y=100 + i * 50, width=100,
                                                                                 height=30)
            self.create_input_field(i)

        # 设置按钮
        self.create_buttons()

        # 设置初始焦点
        self.entry_list[0].focus()

    def create_input_field(self, i):
        """根据字段索引创建对应的输入控件"""
        self.entry_list = []

        if i == 2:  # 性别选择单选框
            Radiobutton(self.frame, text='男', variable=self.get_values[i], value='男', font=LABEL_FONT,
                        justify=CENTER).place(x=350, y=100 + i * 50, width=50, height=30)
            Radiobutton(self.frame, text='女', variable=self.get_values[i], value='女', font=LABEL_FONT,
                        justify=CENTER).place(x=450, y=100 + i * 50, width=50, height=30)
            self.get_values[i].set(DEFAULT_SEX)
        elif i == 3:  # 年龄选择器
            Spinbox(self.frame, from_=17, to=24, width=10, font=LABEL_FONT, state='readonly', justify=CENTER,
                    textvariable=self.get_values[i]).place(x=350, y=100 + i * 50, width=160, height=30)
            self.get_values[i].set(DEFAULT_AGE)
        elif i == 4:  # 学院下拉框
            self.college_combobox = Combobox(self.frame, textvariable=self.get_values[i], state='readonly',
                                             font=('宋体', 12), justify=CENTER)
            self.college_combobox['values'] = list(self.major_dict.keys())
            self.college_combobox.place(x=350, y=100 + i * 50, width=160, height=30)
            self.college_combobox.bind("<<ComboboxSelected>>", self.update_major_combobox)
        elif i == 5:  # 专业下拉框
            self.major_combobox = Combobox(self.frame, textvariable=self.get_values[i], state='readonly',
                                           font=('宋体', 12), justify=CENTER)
            self.major_combobox['values'] = []  # 初始化为空，选择学院后更新
            self.major_combobox.place(x=350, y=100 + i * 50, width=160, height=30)
        else:  # 普通文本输入框
            entry = Entry(self.frame, textvariable=self.get_values[i], font=('宋体', 15), justify=CENTER)
            entry.place(x=350, y=100 + i * 50, width=160, height=30)
            self.entry_list.append(entry)

    def update_major_combobox(self, event):
        """根据选择的学院更新专业下拉框"""
        selected_college = self.get_values[4].get()
        if selected_college in self.major_dict:
            self.major_combobox['values'] = self.major_dict[selected_college]
            self.major_combobox.current(0)  # 默认选择第一个专业
        else:
            self.major_combobox['values'] = []

    def create_buttons(self):
        """创建添加和重置按钮"""
        Button(self.frame, text='添加', width=15, height=1, cursor='hand2', font=BUTTON_FONT,
               command=self.add_student).place(x=300, y=450, width=200, height=40)
        Button(self.frame, text='重置', width=15, height=1, cursor='hand2', font=BUTTON_FONT,
               command=self.reset_fields).place(x=300, y=500, width=200, height=40)

    def add_student(self):
        """添加学生信息到数据库，校验输入并保存"""
        if not self.validate_inputs():
            return

        # 连接数据库并插入数据
        con = Database()
        con.insert(*[value.get() for value in self.get_values])

        # 提示是否继续添加
        if messagebox.askyesno('提示', '是否继续添加？'):
            self.reset_fields()
        else:
            self.window.destroy()

    def validate_inputs(self):
        """校验输入字段的合法性"""
        warnings = ('学号不能为空！',
                    '姓名不能为空！',
                    '性别不能为空！',
                    '年龄不能为空！',
                    '学院不能为空！',
                    '专业不能为空！',
                    '班级不能为空！'
                    )
        for i, value in enumerate(self.get_values):
            if value.get().strip() == '':
                messagebox.showwarning('提示', warnings[i])
                return False
            if i == 0 and (len(value.get()) not in (10, 11) or not value.get().isdigit()):  # 校验学号格式
                messagebox.showwarning('提示', '学号格式错误！')
                return False
        return True

    def reset_fields(self):
        """重置输入字段为默认值"""
        for i in range(7):
            self.get_values[i].set(DEFAULT_SEX if i == 2 else DEFAULT_AGE if i == 3 else '')
        self.entry_list[0].focus()  # 设置焦点
