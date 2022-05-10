import smtplib
from email.mime.text import MIMEText  # 邮件正文
from email.header import Header  # 邮件头


def send():
    with open('config.ini', 'r') as f:
        data = f.readlines()  # 读取文件中的所有行,返回字符串列表
        host = data[0].strip()  # 字符串方法, 去掉每行的首尾空格
        port = int(data[1].strip())
        user = data[2].strip()
        pwd = data[3].strip()
    text = "host:%s\n port:%d\n user:%s\n pwd:%s" % (host, port, user, pwd)
    message = MIMEText(text, 'plain', 'utf-8')
    message['From'] = Header('python自动邮件', 'utf-8')
    message['To'] = Header('测试')
    message['Subject'] = Header('Python SMTP 邮件测试', 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtpObj.login('qiu0089@foxmail.com', 'glharupcstpigbjb')
        smtpObj.sendmail('qiu0089@foxmail.com', ['qiu0089@foxmail.com'], message.as_string())
        print('邮件发送成功')
    except smtplib.SMTPException as e:
        print('邮件发送失败')
        print(e)
