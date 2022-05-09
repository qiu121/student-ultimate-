import pymysql
from tkinter import messagebox


class Database:

    def __init__(self):
        with open('config.ini', 'r') as f:
            data = f.readlines()  # 读取文件中的所有行,返回字符串列表
            self.host = data[0].strip()  # 字符串方法, 去掉每行的首尾空格
            self.port = int(data[1].strip())
            self.user = data[2].strip()
            self.pwd = data[3].strip()
        self.connect()

    def connect(self):
        # 读取文件中的数据库信息,用列表存储
        # 初步连接数据库,创建新的数据库
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, charset='utf8')
        cursor = db.cursor()
        # 创建新的数据库，如果不存在
        sql = "CREATE DATABASE IF NOT EXISTS studb"
        cursor.execute(sql)
        db.close()

        # 数据库二次连接，创建新的表存储学生信息,如果表已存在，则不创建
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
                        major VARCHAR(50)  NOT NULL ,
                        class VARCHAR(15) NOT NULL ,
                        PRIMARY KEY (id) # 设置学号为主键,唯一存在
                        )'''
            cursor1.execute(sql1)
            db1.commit()
        except Exception as e:
            db1.rollback()
            messagebox.showerror('错误', '数据表创建失败\n' + str(e))
        finally:
            db1.close()

    def insert(self, *data):
        """
        参数data对应为学生数据表studb的字段数据,接受一个元组
        id, name, gender,age,college,major，class
        """
        db1 = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                              charset='utf8')
        cursor1 = db1.cursor()
        # a = ((data[0]), data[1], data[2], (data[3]), data[4], data[5], data[6])
        try:
            sql1 = '''INSERT INTO student(id,name,gender,age,college,major,class)
            values (%s,%s,%s,%s,%s,%s,%s)'''
            cursor1.execute(sql1, data)
            db1.commit()
            messagebox.showinfo('提示', '添加成功')
        # 学号为唯一，不能重复添加
        except pymysql.err.IntegrityError as e:
            db1.rollback()
            messagebox.showerror('添加失败', '学号已存在\n' + str(e))
        except Exception as e:
            db1.rollback()
            messagebox.showerror('警告', '添加失败\n' + str(e))
        finally:
            db1.close()

    def update_id(self, *data):
        """更新学号数据"""
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                               charset='utf8')
        cursor = conn.cursor()
        update_id = '''UPDATE student SET id = %s where id = %s'''
        try:
            cursor.execute(update_id, data)
            conn.commit()
            messagebox.showinfo('提示', '修改成功')
        except Exception as e:
            conn.rollback()
            messagebox.showerror('错误', '修改失败\n' + str(e))
        finally:
            conn.close()

    def update_name(self, *data):
        """更新姓名数据"""
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                               charset='utf8')
        cursor = conn.cursor()
        update_name = '''UPDATE student SET name = %s where id = %s'''
        try:
            cursor.execute(update_name, data)
            conn.commit()
            messagebox.showinfo('提示', '修改成功')
        except Exception as e:
            conn.rollback()
            messagebox.showerror('错误', '修改失败\n' + str(e))
        finally:
            conn.close()

    def update_gender(self, *data):
        """更新性别"""
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                               charset='utf8')
        cursor = conn.cursor()
        update_name = '''UPDATE student SET gender = %s where id = %s'''
        try:
            cursor.execute(update_name, data)
            conn.commit()
            messagebox.showinfo('提示', '修改成功')
        except Exception as e:
            conn.rollback()
            messagebox.showerror('错误', '修改失败\n' + str(e))
        finally:
            conn.close()

    def update_age(self, *data):
        """更新年龄"""
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                               charset='utf8')
        cursor = conn.cursor()
        update_age = '''UPDATE student SET age = %s where id = %s'''
        try:
            cursor.execute(update_age, data)
            conn.commit()
            messagebox.showinfo('提示', '修改成功')
        except Exception as e:
            conn.rollback()
            messagebox.showerror('错误', '修改失败\n' + str(e))
        finally:
            conn.close()

    def update_college(self, *data):
        """更新学院"""
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                               charset='utf8')
        cursor = conn.cursor()
        update_college = '''UPDATE student SET college = %s where id = %s'''
        try:
            cursor.execute(update_college, data)
            conn.commit()
            messagebox.showinfo('提示', '修改成功')
        except Exception as e:
            conn.rollback()
            messagebox.showerror('错误', '修改失败\n' + str(e))
        finally:
            conn.close()

    def update_major(self, *data):
        """更新专业"""
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                               charset='utf8')
        cursor = conn.cursor()
        update_major = '''UPDATE student SET major = %s where id = %s'''
        try:
            cursor.execute(update_major, data)
            conn.commit()
            messagebox.showinfo('提示', '修改成功')
        except Exception as e:
            conn.rollback()
            messagebox.showerror('错误', '修改失败\n' + str(e))
        finally:
            conn.close()

    def update_class(self, *data):
        """更新班级"""
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                               charset='utf8')
        cursor = conn.cursor()
        update_class = '''UPDATE student SET class = %s where id = %s'''
        try:
            cursor.execute(update_class, data)
            conn.commit()
            messagebox.showinfo('提示', '修改成功')
        except Exception as e:
            conn.rollback()
            messagebox.showerror('错误', '修改失败\n' + str(e))
        finally:
            conn.close()

    def update_all(self, *data):
        """更新全部"""
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                               charset='utf8')
        cursor = conn.cursor()
        update_name = '''UPDATE student SET id=%s,
                                            name = %s,
                                            gender=%s,
                                            age = %s, 
                                            college = %s,
                                            major = %s,
                                            class = %s
                                            where id = %s'''
        try:
            cursor.execute(update_name, data)
            conn.commit()
            messagebox.showinfo('提示', '修改成功')
        except Exception as e:
            conn.rollback()
            messagebox.showerror('错误', '修改失败\n' + str(e))
        finally:
            conn.close()

    def query_all(self):
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                             charset='utf8')
        cursor = db.cursor()
        sql_all = '''SELECT * FROM student ORDER BY id DESC '''  # 查询全部，按照id升序
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

    def query_id_exact(self, id_):
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                             charset='utf8')
        cursor = db.cursor()
        sql_exact = '''SELECT * FROM student WHERE id = %s'''
        cursor.execute(sql_exact, id_)
        data = cursor.fetchone()  # 查询到的数据为空，返回None
        cursor.close()
        if not data:
            messagebox.showinfo('提示', '没有查询到数据')
        else:
            messagebox.showinfo('提示', '查询成功')
        db.close()
        return data

    def query_id_regexp(self, id_):
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                             charset='utf8')
        cursor = db.cursor()
        sql_regexp = '''SELECT * FROM student WHERE id REGEXP '%s' '''
        # 学号在数据库中的数据类型为整型数字，应先转换为整型再查询
        num = cursor.execute(sql_regexp, int(id_))  # 返回查询到的数据条数
        data = cursor.fetchall()  # 查询到的数据为空，返回空元组，值为False
        cursor.close()
        if not data:
            messagebox.showinfo('提示', '没有查询到数据')
        else:
            messagebox.showinfo('查询成功', '查询到 ' + str(num) + ' 条数据')
        db.close()
        return data, num  # 返回查询到的数据，和查询到的数据条数

    def query_name_exact(self, name_):
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                             charset='utf8')
        cursor = db.cursor()
        sql_exact = '''SELECT * FROM student WHERE name = %s'''
        n = cursor.execute(sql_exact, name_)
        data = cursor.fetchone()  # 查询到的数据为空，返回None
        cursor.close()
        if not data:
            messagebox.showinfo('提示', '没有查询到数据')
        else:
            messagebox.showinfo('查询成功', '查询到' + str(n) + '条数据')
        db.close()
        return data

    def delete_id(self, id_):
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db='studb',
                             charset='utf8')
        cursor = db.cursor()
        sql_delete = '''DELETE FROM student WHERE id = %s'''
        n = cursor.execute(sql_delete, id_)  # 返回删除的数据条数
        db.commit()
        cursor.close()
        if n == 0:
            messagebox.showwarning('提示', '没有查询到数据')
        else:
            messagebox.showinfo('提示', '删除成功')
        db.close()


if __name__ == '__main__':
    # 测试
    con = Database()
    # con.insert(0, '张三', '男', 18, '计算机学院', '计算机1801', '计算机科学与技术')
    con.query_id_regexp(20)
