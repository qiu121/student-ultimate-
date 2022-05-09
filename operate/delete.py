from tkinter import *
from tkinter import messagebox
from database import *
from home import *


class Delete():

    def __init__(self, master=None):
        self.window = master
        super().__init__()

        self.delete_window()

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
            if messagebox.askyesno('提示', '确定删除学号为%s的学生信息吗?' % item_text[1]):
                conn.delete_id(item_text[0])
                self.show_all()
