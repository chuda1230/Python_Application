# -*- coding: cp949 -*-
from xmlbook import *
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

##global
conn = None
#regKey = '73ee2bc65b*******8b927fc6cd79a97'
regKey="OXXjaTQGa3JB1n%2FGAHg36TeRaj9xX6w9mFXFgnP9j37rk%2BYpnbRD9s%2BUim7T0fESZampjBGuLZzcbstVAeNjVA%3D%3D"

# 네이버 OpenAPI 접속 정보 information
#server = "openapi.naver.com"
server="open.ev.or.kr:8080"


# smtp 정보
host = "smtp.gmail.com" # Gmail SMTP 서버 주소.
port = "587"

def userURIBuilder(server,**user):
    str = "http://" + server + "/openapi/services/rest/EvChargerService" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str

def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)

def getChargerDataFromstatid(addr):
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
        return SearchChargerData(req.read().decode('utf-8'),addr)
    else:
        print ("OpenAPI request has been failed!! please retry")
        return None

def SearchChargerData(strxml,keyword):
    from xml.etree import ElementTree
    retlist = []
    try:
        tree = ElementTree.fromstring(strxml)
        print(strxml)
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
                        if (strTitle.text.find(keyword) >= 0):
                                #retlist.append((strNm.text))
                                #retlist.append((strTitle.text))
                                #retlist.append((strtime.text))
                                if strtime != None:
                                    print ({"이름": strNm.text , "주소": strTitle.text , "이용시간" : strtime.text})
                                else:
                                    print({"이름": strNm.text, "주소": strTitle.text})
        #return retlist

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
    # Charger 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    print(itemElements)
    for item in itemElements:
        straddr = item.find("addrDoro")
        strstatNm = item.find("statNm")
        print (strstatNm)
        if len(strstatNm.text) > 0 :
           return {"addrDoro":straddr.text,"statNm":strstatNm.text}

def sendMain():
    global host, port
    html = ""
    title = str(input ('제목 :'))
    senderAddr = str(input ('보내는 사람 이메일(g메일) :'))
    recipientAddr = str(input ('받는 사람 이메일 :'))
    msgtext = str(input ('내용입력 :'))
    passwd = str(input (' 당신의 g메일 계정 비밀번호를 입력해주세요 :'))
    msgtext = str(input ('충전소 데이터를 입력할까요 (y/n):'))
    if msgtext == 'y' :
        keyword = str(input ('키워드를 입력해주세요:'))
        waterhead=1
        html = MakeHtmlDoc(getChargerDataFromstatid(waterhead,keyword))
        #html = MakeHtmlDoc(SearchChargerData(waterhead,keyword))
    
    import mysmtplib
    # MIMEMultipart의 MIME을 생성합니다.
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    #Message container를 생성합니다.
    msg = MIMEMultipart('alternative')

    #set message
    msg['Subject'] = title
    msg['From'] = senderAddr
    msg['To'] = recipientAddr
    
    msgPart = MIMEText(msgtext, 'plain')
    bookPart = MIMEText(html, 'html', _charset = 'UTF-8')
    
    # 메세지에 생성한 MIME 문서를 첨부합니다.
    msg.attach(msgPart)
    msg.attach(bookPart)
    
    print ("connect smtp server ... ")
    s = mysmtplib.MySMTP(host,port)
    #s.set_debuglevel(1)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(senderAddr, passwd)    # 로긴을 합니다. 
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
            html = MakeHtmlDoc(SearchBookTitle(value)) # keyword에 해당하는 책을 검색해서 HTML로 전환합니다.
            ##헤더 부분을 작성.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8')) #  본분( body ) 부분을 출력 합니다.
        else:
            self.send_error(400,' bad requst : please check the your url') # 잘 못된 요청라는 에러를 응답한다.


def startWebService():
    try:
        server = HTTPServer( ('localhost',8080), MyHandler)
        print("started http server....")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print ("shutdown web server")
        server.socket.close()  # server 종료합니다.

def checkConnection():
    global conn
    if conn == None:
        print("Error : connection is fail")
        return False
    return True
