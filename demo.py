import tkinter as tk
from tkinter import messagebox


# 登录窗口
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.label = None
        self.username_label = None
        self.username_entry = None
        self.password_label = None
        self.password_entry = None
        self.login_button = None
        self.title("登录窗口")
        self.geometry("300x300")
        self.create_widgets()

    def create_widgets(self):
        # 登录界面组件
        self.label = tk.Label(self, text="登录界面", font=('Helvetica', 18, 'bold'))
        self.label.pack(pady=10)

        self.username_label = tk.Label(self, text="用户名:")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="密码:")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self, text="登录", command=self.check_login)
        self.login_button.pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "password":
            messagebox.showinfo("提示", "登录成功!")
            self.destroy()  # 销毁当前窗口
            MainWindow()  # 打开主窗口
        else:
            messagebox.showerror("错误", "用户名或密码错误!")


# 主窗口
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.label = None
        self.logout_button = None
        self.title("系统主界面")
        self.geometry("300x200")

        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        # 主界面组件
        self.label = tk.Label(self, text="系统主界面", font=('Helvetica', 18, 'bold'))
        self.label.pack(pady=10)

        self.logout_button = tk.Button(self, text="注销", command=self.logout)
        self.logout_button.pack(pady=10)

    def logout(self):
        self.destroy()  # 销毁主窗口
        LoginWindow()  # 返回到登录窗口


if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
