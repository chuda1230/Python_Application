from tkinter import *
from tkinter import font
from internetbook import *
import tkinter.messagebox

g_Tk = Tk()
g_Tk.geometry("1300x700+750+200")
DataList = []
TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
Text2 = Label(g_Tk, font = TempFont, text="찾을주소")
Text2.pack()
Text2.place(x=20,y=105)
InputLabel = Entry(g_Tk, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge')
InputLabel.pack()
InputLabel.place(x=110, y=105)

Text4 = Label(g_Tk, font = TempFont, text="위치검색(충전소id입력)")
Text4.pack()
Text4.place(x=550,y=105)

MapLabel = Entry(g_Tk, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge')
MapLabel.pack()
MapLabel.place(x=810, y=105)

def MapButtonAction():
    id = MapLabel.get()
    type=7
    getChargerDataFromstatid(type, id)

MapButton = Button(g_Tk, font = TempFont, text="검색",  command=MapButtonAction)
MapButton.pack()
MapButton.place(x=1130, y=105)

photo = PhotoImage(file="SearchMap.gif")
Mapimage=Label(g_Tk,image=photo)
Mapimage.pack()
Mapimage.place(x=510,y=205)

ListBoxScrollbar = Scrollbar(g_Tk)
ListBoxScrollbar.pack()
ListBoxScrollbar.place(x=245, y=50)
#-----------------------라벨1
Text1 = Label(g_Tk, font = TempFont, text="충전타입")
Text1.pack()
Text1.place(x=20,y=60)
#-------------------------------------------------------리스트 박스
TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                        width=10, height=1, borderwidth=12, relief='ridge',
                        yscrollcommand=ListBoxScrollbar.set)

SearchListBox.insert(1, "DC차데모")
SearchListBox.insert(2, "AC3상")
SearchListBox.insert(3, "DC콤보")
SearchListBox.pack()
SearchListBox.place(x=110, y=50)
ListBoxScrollbar.config(command=SearchListBox.yview)



def SearchButtonAction():
    RenderText.configure(state='normal')
    tag = InputLabel.get()
    RenderText.delete('1.0', END)  # ?댁쟾 異쒕젰 ?띿뒪??紐⑤몢 ??젣
    #RenderText.insert(INSERT, "test")
    iSearchIndex = SearchListBox.curselection()[0]  # 由ъ뒪?몃컯???몃뜳??媛?몄삤湲?
    print(iSearchIndex)
    if iSearchIndex == 0:  # ?꾩꽌愿
        type = 1
        DataList=getChargerDataFromstatid(type,tag)
    elif iSearchIndex == 1:  # 紐⑤쾾?뚯떇
        type = 3
        DataList = getChargerDataFromstatid(type, tag)
    elif iSearchIndex == 2:  # 留덉폆
        type = 6
        DataList = getChargerDataFromstatid(type, tag)
    elif iSearchIndex == 3:
        pass#SearchCultural()
    #RenderText.insert(INSERT, "test")
    q=1
    for i in range(0,len(DataList),4):
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, q)
        RenderText.insert(INSERT, "] ")
        RenderText.insert(INSERT, "충전소명: ")
        RenderText.insert(INSERT, DataList[i])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "주소: ")
        RenderText.insert(INSERT, DataList[i+1])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "이용시간: ")
        RenderText.insert(INSERT, DataList[i+2])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, "충전소ID: ")
        RenderText.insert(INSERT, DataList[i+3])
        RenderText.insert(INSERT, "\n\n")
        q=q+1

#-------------------------------------------------------검색버튼
TempFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
MainText = Label(g_Tk, font = TempFont, text="[전국 전기자동차 충전소 App]")
MainText.pack()
MainText.place(x=20)
SearchButton = Button(g_Tk, font = TempFont, text="검색",  command=SearchButtonAction)
SearchButton.pack()
SearchButton.place(x=430, y=110)
#-------------------------------------------------------검색창

#-------------------------------------------------------텍스트
TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
RenderTextScrollbar = Scrollbar(g_Tk)
RenderTextScrollbar.pack()
RenderTextScrollbar.place(x=375, y=200)
TempFont = font.Font(g_Tk, size=10, family='Consolas')
RenderText = Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
RenderText.pack()
RenderText.place(x=110, y=215)
RenderTextScrollbar.config(command=RenderText.yview)
RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

#------------------------------------메일 보내기
def MailButtonAction():
    tag = InputLabel.get()
    recipient = MailLabel.get()
    iSearchIndex = SearchListBox.curselection()[0]  # 由ъ뒪?몃컯???몃뜳??媛?몄삤湲?
    print(iSearchIndex)
    if iSearchIndex == 0:  # ?꾩꽌愿
        type = 1
        sendMain(recipient,type,tag)
    elif iSearchIndex == 1:  # 紐⑤쾾?뚯떇
        type = 3
        sendMain(recipient,type, tag)
    elif iSearchIndex == 2:  # 留덉폆
        type = 6
        sendMain(recipient,type, tag)

TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
Text3 = Label(g_Tk, font = TempFont, text="이메일전송")
Text3.place(x=20,y=605)
MailLabel = Entry(g_Tk, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge')
MailLabel.pack()
MailLabel.place(x=110, y=605)
MailButton = Button(g_Tk, font = TempFont, text="보내기",  command=MailButtonAction)
MailButton.pack()
MailButton.place(x=380, y=605)

g_Tk.mainloop()