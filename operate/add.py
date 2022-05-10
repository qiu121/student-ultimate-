from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
# from tkinter.ttk import Treeview
from database import *


class Add:
    def __init__(self, master=None):
        self.window = master
        # self.window = Tk()
        super().__init__()  # 调用父类的构造方法(不过这里不是必须的,好像没有什么用)

        self.add_window()

    def add_window(self):
        """添加窗口"""
        # 创建标签,显示文字标题
        # self.window=Tk()
        self.frame = Frame(self.window, width=900, height=550, bg='#F0F0F0')
        self.frame.pack()
        Label(self.frame, text='添加学生信息', font=('隶书', 20),
              justify=CENTER).place(x=250, y=40, width=310, height=40)
        # 创建标签,显示文字标题
        add_title = ['学号', '姓名', '性别', '年龄', '学院', '专业', '班级']
        add_college = ['新能源车辆学院', '商务贸易学院', '财富管理学院', '人工智能学院', '人居环境学院', '传媒设计学院', '马克思主义学院', '体育学院', '教育学院']
        # 专业较多，暂时先不写,这里只写了本科专业
        add_major = [
            ['机械设计制造及其自动化', '材料成型及控制工程', '机械电子工程(工业机器人)', '智能制造工程', '车辆工程', '汽车服务工程'],
            ['人力资源管理', '国际经济与贸易', '市场营销', '电子商务', '物流工程'],
            ['审计学', '金融工程', '会计学', '财务管理'],
            ['网络工程', '电子信息工程', '电气工程及其自动化', '数字媒体技术', '软件工程', '数据科学与大数据技术', '智能科学与技术', '自动化'],
            ['土木工程', '土木工程(装配式建筑)', '工程造价', '工程造价(BIM6D算量)', '工程管理', '工程管理(装配式建筑)', '水利水电工程', '城乡规划'],
            ['视觉传达设计', '环境设计', '产品设计', '服装与服饰设计', '播音与主持艺术', '广播电视编导'],
            ['社会工作', '思想政治教育(教师教育)'],
            ['社会体育指导与管理', '社会体育指导与管理(足球教师)'],
            ['学前教育(幼儿教师)', '秘书学', '小学教育(教师教育)', '家政学', '数学与应用数学(教师教育)', '英语(教师教育)', '汉语言文学(教师教育)']
        ]
        # 定义为全局变量,免于使用self方法，又臭又长
        global major_dirt, major_keys
        # 字典一一对应,使输入的学院与专业相关联，并且是单相关，即专业不能相关联学院
        major_dirt = {
            add_college[0]: add_major[0],
            add_college[1]: add_major[1],
            add_college[2]: add_major[2],
            add_college[3]: add_major[3],
            add_college[4]: add_major[4],
            add_college[5]: add_major[5],
            add_college[6]: add_major[6],
            add_college[7]: add_major[7],
            add_college[8]: add_major[8],
        }
        # 定义变量获取字典的键(即学院的值)
        major_keys = list(major_dirt.keys())
        # 定义列表获取获取输入的学生信息，列表元素为String()变量
        self.get = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
        global entry
        entry = [0, 0, 0, 0, 0, 0, 0] # 指定一定长度的空列表，初始化Entry个数
        for i in range(7):
            Label(self.frame, text=add_title[i], font=('隶书', 15),
                  justify=CENTER).place(x=260, y=100 + i * 50, width=100, height=30)
            # 创建性别RadioButton单选按钮
            if i == 2:
                Radiobutton(self.frame, text='男', variable=self.get[i], value='男',
                            font=('隶书', 15), justify=CENTER).place(x=350, y=100 + i * 50, width=50, height=30)
                Radiobutton(self.frame, text='女', variable=self.get[i], value='女',
                            font=('隶书', 15), justify=CENTER).place(x=450, y=100 + i * 50, width=50, height=30)
                # self.get[i].set('男')
                self.get[2].set(' ')  # 性别,默认设置为一个空格，表示预选为空格！！！！！！！！！！！！！！！！！！

            # 创建年龄Spinbox控件，指定输入范围
            elif i == 3:
                Spinbox(self.frame, from_=17, to=24, width=10, font=('隶书', 16), state='readonly', justify=CENTER,
                        textvariable=self.get[i]).place(x=350, y=100 + i * 50, width=160, height=30)
                self.get[i].set('')  # 年龄,初始化
                # self.get[i].set(17)

            # 创建学院Combobox下拉列表
            elif i == 4:
                self.add_college_combobox = Combobox(self.frame, textvariable=self.get[i], state='readonly',
                                                     font=('宋体', 12), justify=CENTER)
                self.add_college_combobox['values'] = major_keys
                self.add_college_combobox.place(x=350, y=115 + i * 50, width=160, height=30, anchor=W)
                self.get[i].set('')  # 学院,初始化
                # self.add_college_combobox.current(0)
                # print(self.get[i].get())
                # 将学院事件与专业事件绑定
                self.add_college_combobox.bind("<<ComboboxSelected>>", self.college_major)
            # 创建专业Combobox下拉列表,与学院相关联
            elif i == 5:
                self.add_major_combobox = Combobox(self.frame, textvariable=self.get[i], state='readonly',
                                                   font=('宋体', 12), justify=CENTER)
                self.add_major_combobox['values'] = add_major[0]
                self.add_major_combobox.place(x=350, y=115 + i * 50, width=160, height=30, anchor=W)
                self.get[i].set('')  # 专业,初始化
                # self.add_college_combobox.current(0)
                # print(self.get[i].get())
            # 创建其他Entry控件,接受文本
            else:
                entry[i] = Entry(self.frame, textvariable=self.get[i], font=('宋体', 15),
                                 justify=CENTER)
                entry[i].place(x=350, y=100 + i * 50, width=160, height=30)
                self.get[i].set('')  # 初始化为空
        entry[0].focus()  # 设置默认焦点
        # 创建添加按钮
        self.btn_add = Button(self.frame, text='添加', width=15, height=1, cursor='hand2', font=('黑体', 14))
        self.btn_add.place(x=300, y=450, width=200, height=40)
        self.btn_add.bind('<Button-1>', self.add_click)
        # 匿名函数,重置输入框,性别为特殊处理！！！！！！！！！！！
        self.btn_reset = Button(self.frame, text='重置', width=15, height=1, cursor='hand2', font=('黑体', 14),
                                command=lambda: [self.get[k].set(' ') if k == 2
                                                 else self.get[k].set('') for k in range(7)] + [entry[0].focus()])
        self.btn_reset.place(x=300, y=500, width=200, height=40)
        self.frame.mainloop()
        # 将获取的数据插入数据库

    def college_major(self, event):
        self.add_major_combobox['values'] = major_dirt[self.get[4].get()]
        self.add_major_combobox.current(0)  # 默认选中第一个,很关键，不然选择专业后，更改学院，专业保持之前的选择

    def add_click(self, event):
        """添加按钮点击事件"""
        # 判断输入框是否为空
        temp = ('学号不能为空！',
                '姓名不能为空！',
                '性别不能为空！',
                '年龄不能为空！',
                '学院不能为空！',
                '专业不能为空！',
                '班级不能为空！')
        for i in range(7):
            # 判断学号输入格式是否正确
            if i == 0:
                if self.get[i].get() == '':
                    messagebox.showwarning('提示', temp[i])
                    return
                else:
                    # 判断学号输入是否为有效位11位(2020级)或者10位(2020级以前？)，且为数字
                    if len(self.get[i].get()) not in (10, 11) or not self.get[i].get().isdigit():
                        messagebox.showwarning('提示', '学号格式错误！')
                        return
            else:
                # 判断性别输入框是否为空！！！！！！！！！！！！！！！！！！！性别特别处理
                if self.get[i].get() == ' ':
                    messagebox.showwarning('提示', temp[i])
                    return
                # 判断其他输入框是否为空
                if self.get[i].get() == '':
                    messagebox.showwarning('提示', temp[i])
                    return

        # 读取配置文件，获取数据库连接信息
        with open('config.ini', 'r') as f:
            db_info = f.readlines()
        db_info = [i.strip() for i in db_info]
        # 连接数据库,创建DataBase对象实例
        con = Database()
        # 调用DataBase对象实例的insert方法,插入数据
        con.insert(self.get[0].get(), self.get[1].get(), self.get[2].get(), self.get[3].get(),
                   self.get[4].get(), self.get[5].get(), self.get[6].get())
        # self.frame.destroy()
        # # 弹窗提问确认下一步操作
        # if messagebox.askyesno('提示', '是否继续添加？'):
        #     [self.get[i].set(' ') if i == 2 else self.get[i].set('') for i in range(7)]  # 将输入框内容清空
        #     entry[0].focus()  # 设置默认焦点
        # else:
        #     self.window.destroy()  # 销毁窗口
