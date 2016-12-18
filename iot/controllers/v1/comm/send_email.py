import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from pecan import render

class send_email(object):
    FROM_ADDR = 'iot_i_team@126.com'
    PASSWD = '123456abc'
    SMTP_SERVER = 'smtp.126.com'

    def __init__(self, to_addr, render_template='welcome_register'):
        self.to_addr = to_addr
        self.template = render_template + '.jinja2'

    def send_email(self, render_context):
        render_context['custom_email'] = self.to_addr
        server = smtplib.SMTP(self.SMTP_SERVER, 25)
        server.set_debuglevel(1)
        server.login(self.FROM_ADDR, self.PASSWD)
        email_body = render(self.template, render_context)
        server.sendmail(self.FROM_ADDR, [self.to_addr], email_body.encode('utf-8'))
        server.quit()
