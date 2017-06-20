# -*- coding: cp949 -*-
import spam
from xmlbook import *
from map import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

##global
conn = None
#regKey = '73ee2bc65b*******8b927fc6cd79a97'
regKey="OXXjaTQGa3JB1n%2FGAHg36TeRaj9xX6w9mFXFgnP9j37rk%2BYpnbRD9s%2BUim7T0fESZampjBGuLZzcbstVAeNjVA%3D%3D"

# ���̹� OpenAPI ���� ���� information
#server = "openapi.naver.com"
server="open.ev.or.kr:8080"


# smtp ����
host = "smtp.gmail.com" # Gmail SMTP ���� �ּ�.
port = "587"

def userURIBuilder(server,**user):
    str = "http://" + server + "/openapi/services/rest/EvChargerService" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)

def getChargerDataFromstatid(type,addr):
    global server, regKey, conn
    if conn == None :
        connectOpenAPIServer()
    #uri = userURIBuilder(server, key=regKey, query='%20', display="1", start="1", target="book_adv", d_isbn=isbn)
    uri = userURIBuilder(server, serviceKey=regKey,output="xml")
    conn.request("GET", uri)

    req = conn.getresponse()
    print (req.status)
    if int(req.status) == 200 :
        print("Charger data downloading complete!")
        #return extractChargerData(req.read().decode('utf-8'))
        if(type==7):
            return SearchChargerMap(req.read().decode('utf-8'), addr, type)
        else:
            return SearchChargerData(req.read().decode('utf-8'),addr,type)
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None

def SearchChargerMap(strxml,keyword,type):
    from xml.etree import ElementTree
    retlist = []
    try:
        tree = ElementTree.fromstring(strxml)
        # print(strxml)
    except Exception:
        print("Element Tree parsing Error : maybe the xml document is not corrected.")
        return None

        # get Book Element
    chargerElements = tree.getiterator("body")  # return list type
    for data in chargerElements:
        for item in data:
            for i in item:
                strid = i.find("statId")
                exid=str(strid.text)
                strlat = i.find("lat")
                strlng = i.find("lng")
                intlat = float(strlat.text)
                intlng = float(strlng.text)
                if(spam.strcmp(exid, keyword)==0):
                    # retlist.append((strNm.text))
                    # retlist.append((strTitle.text))
                    # retlist.append((strtime.text))
                            retlist.append(intlat)
                            retlist.append(intlng)
                            print(retlist)
    GetMap(retlist)


def SearchChargerData(strxml,keyword,type):
    from xml.etree import ElementTree
    retlist = []
    try:
        tree = ElementTree.fromstring(strxml)
        #print(strxml)
    except Exception:
            print("Element Tree parsing Error : maybe the xml document is not corrected.")
            return None

                # get Book Element
    chargerElements = tree.getiterator("body")  # return list type
    for data in chargerElements:
        for item in data:
                for i in item:
                        strTitle = i.find("addrDoro")
                        strNm=i.find("statNm")
                        strtime=i.find("useTime")
                        strtype=i.find("chgerType")
                        strid=i.find('statId')
                        inttype=int(strtype.text)
                        if (strTitle.text.find(keyword) >= 0):
                                #retlist.append((strNm.text))
                                #retlist.append((strTitle.text))
                                #retlist.append((strtime.text))
                                if(inttype>=type):
                                    if strtime != None:
                                        print ({"�̸�": strNm.text , "�ּ�": strTitle.text , "�̿�ð�" : strtime.text})
                                        retlist.append((strNm.text))
                                        retlist.append((strTitle.text))
                                        retlist.append((strtime.text))
                                        retlist.append((strid.text))
                                    else:
                                        print({"�̸�": strNm.text, "�ּ�": strTitle.text})
                                        retlist.append((strNm.text))
                                        retlist.append((strTitle.text))
                                        retlist.append((strid.text))

        return retlist

    # for item in chargerElements:
    #             print("test")
    #             strTitle = item.find("addrDoro")
    #             strNm=item.find("statNm")
    #             strtime=item.find("useTime")
    #             if (strTitle.text.find(keyword) >= 0):
    #                     retlist.append((strNm.text))
    #                     retlist.append((strTitle.text))
    #                     retlist.append((strtime.text))
    # return retlist

def extractChargerData(strXml,keyword):
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print (strXml)
    # Charger ������Ʈ�� �����ɴϴ�.
    itemElements = tree.getiterator("item")  # return list type
    print(itemElements)
    for item in itemElements:
        straddr = item.find("addrDoro")
        strstatNm = item.find("statNm")
        print (strstatNm)
        if len(strstatNm.text) > 0 :
           return {"addrDoro":straddr.text,"statNm":strstatNm.text}

def sendMain(recipientAddr,type,keyword):
    global host, port
    html = ""
    title = "������ �������Դϴ�."
    senderAddr = "chuda235@gmail.com"
    msgtext = "�����ҵ������Դϴ�."
    passwd = "tkdgh2558"
    html = MakeHtmlDoc(getChargerDataFromstatid(type,keyword))
        #html = MakeHtmlDoc(SearchChargerData(waterhead,keyword))
    
    import mysmtplib
    # MIMEMultipart�� MIME�� �����մϴ�.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container�� �����մϴ�.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # �޼����� ������ MIME ������ ÷���մϴ�.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # �α��� �մϴ�. 
    s.sendmail(senderAddr , [recipientAddr], msg.as_string())
    s.close()
    
    print ("Mail sending complete!!!")

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        from urllib.parse import urlparse
        import sys
      
        parts = urlparse(self.path)
        keyword, value = parts.query.split('=',1)

        if keyword == "title" :
            html = MakeHtmlDoc(SearchBookTitle(value)) # keyword�� �ش��ϴ� å�� �˻��ؼ� HTML�� ��ȯ�մϴ�.
            ##��� �κ��� �ۼ�.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8')) #  ����( body ) �κ��� ��� �մϴ�.
        else:
            self.send_error(400,' bad requst : please check the your url') # �� ���� ��û��� ������ �����Ѵ�.


def startWebService():
    try:
        server = HTTPServer( ('localhost',8080), MyHandler)
        print("started http server....")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print ("shutdown web server")
        server.socket.close()  # server �����մϴ�.

def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True
