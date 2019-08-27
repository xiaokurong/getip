import urllib.request
import json

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import  time

sender ='liuyanjie@dealeasy.com'
receiver = 'liuyanjie@dealeasy.com'
mail_host = 'smtp.mxhichina.com'
mail_user = 'liuyanjie@dealeasy.com'
mail_pass = 'xxxxxxx'

'''
  add description for test
'''
def getIpPage():
    url = 'https://api.ipify.org/?format=json'
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    return html

def getRealIp(html):
    jsonData = json.loads(html)
    return jsonData['ip']

realIp = getRealIp(getIpPage())
timeId=int(time.time())

mail_text = '公司的公网IP地址是: ' + realIp

message = MIMEText(mail_text,'plain','utf-8')
message['From'] = Header('liuyanjie@dealeasy.com','utf-8')
message['To'] = Header('liuyanjie@dealeasy.com', 'utf-8')

subject = '公司公网IP on '+str(timeId)
'''
    邮件标题增加时间戳标记，避免阿里云邮箱去重。阿里云邮箱会在检查相近时间相同的邮件主题、发件人收件人等在短时间内多次链接会判断为自动去重而发送失败，阿里企业邮箱的判断去重条件：5分钟内，会根据邮件正文中的rcptto、date、from、subject、Message-ID、mailfrom等字段来判断用户是否在发送重复的邮件，如果是重复的邮件，将会在队列中丢弃。请您检查一下您的发信模板、程序等，是否邮件正文的上述字段都是固定的，如果缺少上述字段则默认为是相同邮件，建议给发送的每封信加上不同的message-ID来解决这个问题。
'''
message['Subject'] = Header(subject,'utf-8')

try:
    smtpObj = smtplib.SMTP(mail_host,25)
    # smtpObj.set_debuglevel(1)
    # smtpObj.connect(mail_host,25)
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender,receiver,message.as_string())
    smtpObj.quit()
    print('邮件发送成功')
except smtplib.SMTPException:
    print('Error: 无法发送邮件')
