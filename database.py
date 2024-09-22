import configparser
from tkinter import messagebox

import pymysql


class Database:

    def __init__(self):
        # 使用 configparser 解析配置文件
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.host = config.get('database', 'host')
        self.port = config.getint('database', 'port')
        self.user = config.get('database', 'user')
        self.pwd = config.get('database', 'pwd')
        self.db_name = 'studb'
        self.charset = 'utf8'

        # 初始化数据库和表
        self.connect()
        self.create_table()

    def _get_connection(self, db_name=None):
        """获取数据库连接"""
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.pwd,
            db=db_name if db_name else None,
            charset=self.charset
        )

    def connect(self):
        """连接数据库，创建数据库（如果不存在）"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            conn.commit()

    def create_table(self):
        """创建学生信息表（如果不存在）"""
        create_table_sql = f'''
        CREATE TABLE if NOT EXISTS `student`
(
    `id`         BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
    `student_no` VARCHAR(15)  NOT NULL,
    `name`       VARCHAR(20)      NOT NULL,
    `gender`     VARCHAR(10)      NOT NULL,
    `age`        TINYINT UNSIGNED NOT NULL,
    `college`    VARCHAR(50)      NOT NULL,
    `major`      VARCHAR(50)      NOT NULL,
    `class`      VARCHAR(15)      NOT NULL,
    PRIMARY KEY (id)
)'''
        with self._get_connection(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                print(cursor.mogrify(create_table_sql))  # 打印创建表的 SQL 语句
                cursor.execute(create_table_sql)
                conn.commit()
            except Exception as e:
                conn.rollback()
                messagebox.showerror('错误', f'数据表创建失败\n{str(e)}')

    def insert(self, *data):
        """插入一条学生记录"""
        insert_sql = '''
        INSERT INTO `student`(`student_no`, `name`, `gender`, `age`, `college`, `major`, `class`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        with self._get_connection(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                print(cursor.mogrify(insert_sql, data))  # 打印插入的 SQL 语句
                cursor.execute(insert_sql, data)
                conn.commit()
                messagebox.showinfo('提示', '添加成功')
            except pymysql.IntegrityError as e:
                conn.rollback()
                messagebox.showerror('添加失败', f'学号已存在\n{str(e)}')
            except pymysql.MySQLError as e:
                conn.rollback()
                messagebox.showerror('数据库错误', f'数据库操作失败\n{str(e)}')
            except Exception as e:
                conn.rollback()
                messagebox.showerror('错误', f'未知错误\n{str(e)}')

    def bulk_insert(self, students_data):
        """批量插入学生记录"""
        insert_sql = '''
        INSERT INTO `student`(`student_no`, `name`, `gender`, `age`, `college`, `major`, `class`)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        with self._get_connection(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                for student in students_data:
                    print(cursor.mogrify(insert_sql, student))  # 打印每个学生插入的 SQL 语句
                cursor.executemany(insert_sql, students_data)
                conn.commit()
                messagebox.showinfo('提示', '批量添加成功')
            except Exception as e:
                conn.rollback()
                messagebox.showerror('错误', f'批量添加失败\n{str(e)}')

    def update(self, field, value, student_id):
        """通用的更新函数"""
        update_sql = f"UPDATE `student` SET {field} = %s WHERE `id` = %s"
        with self._get_connection(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                print(cursor.mogrify(update_sql, (value, student_id)))  # 打印更新的 SQL 语句
                cursor.execute(update_sql, (value, student_id))
                conn.commit()
                messagebox.showinfo('提示', f'{field} 更新成功')
            except Exception as e:
                conn.rollback()
                messagebox.showerror('错误', f'{field} 更新失败\n{str(e)}')

    def update_all(self, student_data, _id):
        """更新学生的所有信息"""
        update_sql = '''
        UPDATE `student` SET
            `student_no` = %s,
            `name` = %s,
            `gender` = %s,
            `age` = %s,
            `college` = %s,
            `major` = %s,
            `class` = %s
        WHERE `id` = %s
        '''
        with self._get_connection(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                print(cursor.mogrify(update_sql, (*student_data[:], _id)))  # 打印更新全部信息的 SQL 语句
                cursor.execute(update_sql, (*student_data[:], _id))
                conn.commit()
                messagebox.showinfo('提示', '全部信息更新成功')
            except Exception as e:
                conn.rollback()
                messagebox.showerror('错误', f'更新失败\n{str(e)}')

    def query(self, field=None, value=None, exact=True):
        """通用的查询函数"""
        if field and value is not None:
            operator = '=' if exact else 'REGEXP'
            query_sql = f"SELECT * FROM `student` WHERE {field} {operator} %s ORDER BY `student_no` DESC"
            param = value if exact else f"{value}"
        else:
            query_sql = "SELECT * FROM `student` ORDER BY `student_no` DESC"
            param = None

        with self._get_connection(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                if param:
                    print(cursor.mogrify(query_sql, (param,)))  # 打印查询的 SQL 语句
                    cursor.execute(query_sql, (param,))
                else:
                    print(query_sql)  # 打印查询所有的 SQL 语句
                    cursor.execute(query_sql)
                data = cursor.fetchall()
                if not data:
                    messagebox.showinfo('提示', '没有查询到数据')
                else:
                    messagebox.showinfo('查询成功', f'查询到 {len(data)} 条数据')
                return data
            except Exception as e:
                messagebox.showerror('错误', f'查询失败\n{str(e)}')
                return None

    def delete(self, student_id):
        """根据学号删除学生记录"""
        delete_sql = "DELETE FROM student WHERE `student_no` = %s"
        with self._get_connection(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                print(cursor.mogrify(delete_sql, (student_id,)))  # 打印删除的 SQL 语句
                n = cursor.execute(delete_sql, (student_id,))
                conn.commit()
                if n == 0:
                    messagebox.showwarning('提示', '没有找到要删除的数据')
                else:
                    messagebox.showinfo('提示', '删除成功')
            except Exception as e:
                conn.rollback()
                messagebox.showerror('错误', f'删除失败\n{str(e)}')

    def close(self):
        """关闭数据库连接（如果有需要）"""
        pass  # 当前的实现中，连接在 with 语句中自动关闭，无需额外处理


if __name__ == '__main__':
    # 测试
    db = Database()
    # 插入一条数据
    db.insert(1, '张三', '男', 20, '计算机学院', '计算机科学与技术', '1801班')
    # 批量插入数据
    students = [
        (2, '李四', '女', 19, '电子学院', '电子信息工程', '1802班'),
        (3, '王五', '男', 21, '机械学院', '机械设计制造及其自动化', '1803班'),
    ]
    db.bulk_insert(students)
    # 更新数据
    db.update('age', 22, 1)
    # 查询所有数据
    all_students = db.query()
    print(all_students)
    # 精确查询
    student = db.query(field='name', value='张三', exact=True)
    print(student)
    # 模糊查询
    students_like = db.query(field='name', value='李', exact=False)
    print(students_like)
    # 删除数据
    db.delete(1)
