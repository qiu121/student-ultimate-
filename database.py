import pymysql
from tkinter import messagebox


# with open('config.ini', 'r') as f:
#     data = f.readlines()  # 读取文件中的所有行,返回字符串列表
#     host = data[0].strip()  # 字符串方法, 去掉每行的首尾空格
#     port = int(data[1].strip())
#     user = data[2].strip()
#     pwd = data[3].strip()
# print("============test===========")
# print(host, port, user, pwd, sep='\n')
# print("============test===========")
#

class Database:
    def __init__(self, host, port, user, pwd):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.connect()

    def connect(self):
        # 读取文件中的数据库信息,用列表存储
        # 初步连接数据库,创建新的数据库
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, charset='utf8')
        cursor = db.cursor()
        sql = "CREATE DATABASE IF NOT EXISTS studb"
        cursor.execute(sql)
        db.close()

        # 数据库二次连接
        db1 = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                              charset='utf8')
        cursor1 = db1.cursor()
        try:
            sql1 = '''CREATE TABLE IF NOT EXISTS student(
                        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(20) NOT NULL,
                        gender VARCHAR(10) NOT NULL ,
                        age TINYINT UNSIGNED NOT NULL,
                        college VARCHAR(20) NOT NULL ,
                        class VARCHAR(15) NOT NULL ,
                        major VARCHAR(50)  NOT NULL ,
                        PRIMARY KEY (id)
                        )'''
            cursor1.execute(sql1)
            db1.commit()
        except Exception as e:
            db1.rollback()
            messagebox.showerror('错误', '数据表创建失败')
        finally:
            db1.close()

    def insert(self, *data):
        """
        参数data对应为学生数据表studb的字段数据,接受一个元组
        id, name, gender,age,college,class,major
        """
        db1 = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                              charset='utf8')
        cursor1 = db1.cursor()
        # a = ((data[0]), data[1], data[2], (data[3]), data[4], data[5], data[6])
        try:
            sql1 = '''INSERT INTO student(id,name,gender,age,college,class,major)
            values (%s,%s,%s,%s,%s,%s,%s)'''
            cursor1.execute(sql1, data)
            db1.commit()
            messagebox.showinfo('提示', '添加成功')
        # 学号为唯一，不能重复添加
        except pymysql.err.IntegrityError as e:
            db1.rollback()
            messagebox.showerror('警告', '学号已存在\n' + str(e))
        except Exception as e:
            db1.rollback()
            messagebox.showerror('警告', '添加失败\n' + str(e))
        finally:
            db1.close()

    def delete(self):
        pass

    def update(self):
        pass

    def query_all(self):
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                             charset='utf8')
        cursor = db.cursor()
        sql_all = '''SELECT * FROM student'''
        n = cursor.execute(sql_all)  # 返回查询到的数据条数
        data = cursor.fetchall()  # 查询到的数据为空，返回空元组，值为False
        cursor.close()
        if not data:
            messagebox.showinfo('提示', '数据为空')
        else:
            messagebox.showinfo('查询成功', '查询到 ' + str(n) + ' 条数据')
        # for i in range(n):
        #     print(data[i])
        db.close()
        return data

    def query_id(self, id_):
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                             charset='utf8')
        cursor = db.cursor()
        sql_one = '''SELECT * FROM student WHERE id = %s'''
        cursor.execute(sql_one, id_)
        data = cursor.fetchone()
        cursor.close()
        if not data:
            messagebox.showwarning('提示', '没有查询到数据')
        else:
            messagebox.showinfo('提示', '查询成功')
        db.close()
        return data


if __name__ == '__main__':
    # 测试
    con = Database('localhost', 3306, 'root', 'qiu18279664933')
    # con.insert(0, '张三', '男', 18, '计算机学院', '计算机1801', '计算机科学与技术')
    con.query_id()
