import socket
import threading
import tkinter
import tkinter.messagebox
#import tkinter.scrolledtext
from tkinter import *
from functools import partial
from PIL import Image,ImageTk
from tkinter.scrolledtext import ScrolledText

global mainlist

HOST = "192.168.1.120"
PORT = 7000

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)




def validateLogin(username):
    playername = username.get()
    client.connect((HOST, PORT))
    print(playername)
    client.send(playername.encode())

    # 主遊戲視窗
    gamewindow = tkinter.Toplevel(loginwindow)
    gamewindow.maxsize(650,450)
    gamewindow.minsize(650,450)
    gamewindow.title('遊戲視窗')


    mainlist = ScrolledText(gamewindow)
    mainlist.place(x=5,y=0,width=650,height=300)

    word = StringVar()
    word.set('')
    wordentry = Entry(gamewindow,width=140,textvariable=word)
    wordentry.place(x=5,y=305,width=500,height=25)

    def recvMessage(conn):
        while True:
            indata = conn.recv(2048)
            indata = indata.decode()
            mainlist.insert(tkinter.INSERT, '\n' + indata+ ' \n\n ')


    recvThread = threading.Thread(target=recvMessage, args=(client,))
    recvThread.start()

    def sendword(word):
        outdata = word.get()
        print(outdata)
        mainlist.insert(tkinter.INSERT, '\n' + outdata + ' \n\n ')
        client.send(outdata.encode())
        word.set('')

    sendword = partial(sendword,word)
    sendbutton = Button(gamewindow,text="發言/投票",command=sendword)
    sendbutton.place(x=500,y=305,width=150,height=95)

loginwindow = Tk()
loginwindow.maxsize(600,800)
loginwindow.minsize(600,800)

loginwindow.title("login")

img = Image.open("spy.jpg")
resize_img = img.resize((400,500),Image.ANTIALIAS)
tk_img = ImageTk.PhotoImage(resize_img)

imagelabel = tkinter.Label(loginwindow,image=tk_img)
imagelabel.place(x=100,y=85)

titlelabel = Label(loginwindow, text="誰  是  臥  底" ,font=("思源黑體", 50)) #標題設定
titlelabel.place(x=100,y=5)

#username label and text entry box 玩家姓名輸入設定
usernameLabel = Label(loginwindow, text="player Name:", font=("思源黑體", 12))
usernameLabel.place(x=100, y=630)

username = StringVar()
usernameEntry = Entry(loginwindow, textvariable=username) #姓名輸入框設定
usernameEntry.place(x=190, y=630, width=150, height=50)

imagelabel = tkinter.Label(loginwindow, image=tk_img)
imagelabel.place(x=100, y=85)
validateLogin = partial(validateLogin, username)

#login button
loginButton = Button(loginwindow, text="遊戲開始", command=validateLogin, font=("思源黑體", 12))
loginButton.place(x=345 ,y=630, width=150, height=50)


loginwindow.mainloop()

