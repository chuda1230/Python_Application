# -*- coding: cp949 -*-
loopFlag = 1
from internetbook import *

#### Menu  implementation
def printMenu():
    print("\n충전소위치 현황")
    print("========Menu==========")
    print("프로그램 종료:   q")
    print("충전소데이터 불러오기: g")
    print("메일 보내기 : i")
    print("========Menu==========")
    
def launcherFunction(menu):
    if menu ==  'l':
        LoadXMLFromFile()
    elif menu == 'q':
        QuitBookMgr()
    elif menu == 'p':
        PrintDOMtoXML()
    elif menu == 'b':
        PrintBookList(["title",])
    elif menu == 'a':
        ISBN = str(input ('insert ISBN :'))
        title = str(input ('insert Title :'))
        AddBook({'ISBN':ISBN, 'title':title})
    elif menu == 'e':
        keyword = str(input ('input keyword to search :'))
        printBookList(SearchBookTitle(keyword))
    elif menu == 'g': 
        addr = str(input ('장소입력 :'))
        #isbn = 11110003
        #11110006
        #11200003
        getChargerDataFromstatid(addr)
        #AddBook(ret)
        #print(ret)
    elif menu == 'm':
        keyword = str(input ('input keyword code to the html  :'))
        html = MakeHtmlDoc(SearchBookTitle(keyword))
        print("-----------------------")
        print(html)
        print("-----------------------")
    elif menu == 'i':
        sendMain()
    elif menu == "t":
        startWebService()
    else:
        print ("error : unknow menu key")

def QuitBookMgr():
    global loopFlag
    loopFlag = 0
    BooksFree()
    
##### run #####
while(loopFlag > 0):
    printMenu()
    menuKey = str(input ('select menu :'))
    launcherFunction(menuKey)
else:
    print ("Thank you! Good Bye")
