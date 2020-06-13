# -*- coding: utf-8 -*-
# # 邮件
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error
import os

class Email:
    def __init__(self, server, sender, password, receiver, title, message = None, path = None):
        """
        初始化邮件：
        server: smtp服务器
        sender: 发件人
        password: 发件人密码
        receiver: 收件人 多个收件人用;隔开
        title: 邮件标题
        message: 正文内容
        paht: 可传入list或者str 发送一个或多个附件
        """
        self.server = server
        self.sender = sender
        self.password = password
        self.receiver = receiver
        self.title = title
        self.msg = MIMEMultipart('related')
        self.files = path

        self.message = message

    def _attach_file(self, att_file):
        """将单个文件添加到附件列表中"""
        att = MIMEText(open('%s' % att_file, 'rb').read(), 'plain', 'utf-8')
        att['Content-Type'] = 'application/octet-stream'
        file_name = re.split(r'[\\|/]', att_file)
        att['Content-Disposition'] = 'attachment; filename = "%s"' % file_name[-1]
        self.msg.attach(att)
        print('attach file {}'.format(att_file))

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # 邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message))

        # 添加附件
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)
        
        # 连接服务器在发送
        try:    
            smtp_server = smtplib.SMTP_SSL(self.server)  # 这里会读取计算机名，计算机名不能为中文，否则解码失败
            # smtp_server = smtplib.SMTP_SSL('smtp.qq.com')
            smtp_server.connect(self.server, 465)
        except (error) as e:
            print('smtp connect error. %s' % e)
        # except Exception as e:
        #     print(e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                print("用户名或密码验证失败！%s" % e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())
            finally:
                smtp_server.quit()
                print('''发送成功！
                邮件：{0}
                收件人：{1}
                文件: {2}
                '''.format(self.title, self.receiver, [os.path.split(f)[1] for f in self.files] if isinstance(self.files, list) else os.path.split(self.files)[1]))
            
        

if __name__ == "__main__":
    # os.path.isfile 和 isdir要使用绝对路径
    file = [os.path.join(os.path.abspath('./20200613'), f) for f in os.listdir('./20200613/') if os.path.isfile(os.path.join(os.path.abspath('./20200613'), f))]
    print([os.path.split(f)[1] for f in file])

    # 单个文件
    file = file[0]
    print(file)
    e = Email(server='smtp.qq.com',
              sender='linhao175@qq.com',
              password='********',
              receiver='linhao175@gmail.com',
              title="mail test",
              message="this is a test msg",
              path=file
    )
    e.send()


    