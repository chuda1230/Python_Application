# # -*- coding: cp949 -*-
# import mimetypes
# import mysmtplib
# from email.mime.base import MIMEBase
# from email.mime.text import MIMEText
#
# #global value
# host = "smtp.gmail.com" # Gmail STMP ���� �ּ�.
# port = "587"
# htmlFileName = "logo.html"
#
# senderAddr = "chuda235@gmail.com"     # ������ ��� email �ּ�.
# recipientAddr = "flfltkdgh@naver.com"   # �޴� ��� email �ּ�.
#
# msg = MIMEBase("multipart", "alternative")
# msg['Subject'] = "Test email in Python 3.0"
# msg['From'] = senderAddr
# msg['To'] = recipientAddr
#
# # MIME ������ �����մϴ�.
# htmlFD = open(htmlFileName, 'rb')
# HtmlPart = MIMEText(htmlFD.read(),'html', _charset = 'UTF-8' )
# htmlFD.close()
#
# # ������� mime�� MIMEBase�� ÷�� ��Ų��.
# msg.attach(HtmlPart)
#
# # ������ �߼��Ѵ�.
# s = mysmtplib.MySMTP(host,port)
# #s.set_debuglevel(1)        # ������� �ʿ��� ��� �ּ��� Ǭ��.
# s.ehlo()
# s.starttls()
# s.ehlo()
# s.login("chuda235@gmail.com","tkdgh2558")
# s.sendmail(senderAddr , [recipientAddr], msg.as_string())
# s.close()
import os
import time
from selenium import webdriver

delay=5
fn='testmap.html'
tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
m.save(fn)

browser = webdriver.Firefox()
browser.get(tmpurl)
#Give the map tiles some time to load
time.sleep(delay)
browser.save_screenshot('map.png')
browser.quit()