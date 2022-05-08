from tkinter import *
from operate.add import *
from operate.delete import *
from operate.update import *
from operate.query import *
# 导入自定义的模块,实现主界面的功能(增删改查)


class Home:
    def __init__(self, master=None):
        self.window = master
        self.window.title('学生信息管理系统主界面')
        self.window.geometry('800x500+500+200')
        self.window.resizable(False, False) # 禁止改变窗口大小
        self.frame2 = Frame(self.window, width=800, height=500, bg='#F0F0F0')
        self.frame2.pack(fill=BOTH, expand=1)
        self.main_page()

    def main_page(self):
        """创建主窗口"""
        # 将标签放到窗口左右居中
        Label(self.frame2, text='学生信息管理系统主界面', font=('隶书', 20),
              justify=CENTER).pack(side=TOP, fill=X, padx=10, pady=50)
        # 创建主菜单按钮
        btn_text = ['添加学生信息', '删除学生信息', '修改学生信息', '查询学生信息', '退出系统']
        for i in range(5):
            self.btn = Button(self.frame2, text=btn_text[i], font=('黑体', 12), width=15, height=1)
            self.btn.place(x=320, y=140 + i * 60, width=150, height=40)
            self.btn.bind('<Button-1>', self.btn_click)

    def btn_click(self, event):
        """按钮点击事件"""
        # 调用模块中的类，实现功能
        if event.widget['text'] == '添加学生信息':
            self.frame2.destroy() # 必须销毁主界面,否则会出现重叠,甚至出现无法获取添加界面的数据(未解决)
            Add(self.window)
            # add.add_window()
        elif event.widget['text'] == '查询学生信息':
            # self.frame2.destroy()
            Query(self.window)
            # self.query_window()
        elif event.widget['text'] == '修改学生信息':
            # self.frame2.destroy()
            Update(self.window)
            # self.update_window()
        elif event.widget['text'] == '删除学生信息':
            # self.frame2.destroy()
            Delete(self.window)
            # self.delete_window()
        elif event.widget['text'] == '退出系统':
            self.window.quit()
            # self.frame2.quit()


