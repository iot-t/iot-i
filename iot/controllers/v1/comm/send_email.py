import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
           Header(name, 'utf-8').encode(), \
           addr.encode('utf-8') if isinstance(addr, unicode) else addr))

class send_email(object):
    FROM_ADDR = 'XXX@126.com'
    FROM_PASSWD = '123456'
    SMTP_SERVER = 'XXXX'

    def __init__(self, verify_key, to_addr):
        urls = '127.0.0.1:8080/account?verify_key='+verify_key
        texts = "<html><body>Welcom! Please to active you account by follow links! <a>%s</a> </body></html>" % urls
        
        self.to_addr = to_addr
        self.msg = MIMEText(texts, 'plain', 'utf-8')
        self.msg['From'] = _format_addr(u'IoTAdmin <%s>' % self.FROM_ADDR)
        self.msg['To'] = _format_addr(u'yous <%s>' % to_addr)
        self.msg['Subject'] = Header(u'Welcom registe', 'utf-8').encode()

    def send_email(self):
        server = smtplib.SMTP(self.SMTP_SERVER, 25)
        server.set_debuglevel(1)
        server.login(self.FROM_ADDR, self.PASSWD)
        server.sendmail(self.FROM_ADDR, [self.to_addr], self.msg.as_string())
        server.quit()
