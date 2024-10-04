import tkinter
import tkinter.messagebox
from tkinter import *
from functools import partial
from Pillow import Image, ImageTk
import tkinter.scrolledtext
from tkinter.scrolledtext import ScrolledText
import socket
import threading
import time

global chatlist

def recvMess(conn):
	while True:
		indata = conn.recv(1024)
		indata = indata.decode()
		chatlist.insert(tkinter.INSERT,indata)





HOST = '192.168.1.107'
PORT = 7000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect((HOST, PORT))




def login_window():

	#window
	tkWindow = Tk()
	tkWindow.geometry('600x800')
	tkWindow.title('Tkinter Login Form - pythonexamples.org')

	img = Image.open("spy.jpg")
	resize_img = img.resize((400, 500), Image.ANTIALIAS)
	tk_img = ImageTk.PhotoImage(resize_img)

	def validateLogin(username):
		playername = username.get()
		tkWindow.destroy()
		print("username entered :", playername)
		client.connect((HOST, PORT))
		client.send(playername.encode())
		print("123")
		gamewindow()
		return

	titlelabel = Label(tkWindow, text="誰  是  臥  底" ,font=("思源黑體", 50)) #標題設定
	titlelabel.place(x=100,y=5)

	#username label and text entry box 玩家姓名輸入設定
	usernameLabel = Label(tkWindow, text="player Name:", font=("思源黑體", 12))
	usernameLabel.place(x=100, y=630)
	username = StringVar()
	usernameEntry = Entry(tkWindow, textvariable=username) #姓名輸入框設定
	usernameEntry.place(x=190, y=630, width=150, height=50)

	imagelabel = tkinter.Label(tkWindow, image=tk_img)
	imagelabel.place(x=100, y=85)
	validateLogin = partial(validateLogin, username)

	#login button
	loginButton = Button(tkWindow, text="遊戲開始", command=validateLogin, font=("思源黑體", 12))
	loginButton.place(x=345 ,y=630, width=150, height=50)

	tkWindow.mainloop()

def gamewindow(): #主遊戲視窗

	def sendtext():
		line = chatbar.get()
		client.send(line.encode())
		chatbar.set('')
		chatlist.insert(tkinter.END,line)

	gwindow = Tk()
	gwindow.maxsize(650, 400)
	gwindow.minsize(650, 400)
	gwindow.title("遊戲視窗")


	chatlist = ScrolledText(gwindow)    #聊天室主視窗
	chatlist.place(x=5, y=0, width=650, height=300)
	pnum = client.recv(1024)
	pnum = pnum.decode()
	pMess = pnum +"  等待其他玩家連入......"
	chatlist.insert(tkinter.INSERT,pMess)

	'''player = client.recv(1024)
	player = player.decode()
	chatlist.insert(tkinter.INSERT, player)

	start = "遊戲開始"
	chatlist.insert(tkinter.INSERT, start)

	question = client.recv(1024)
	chatlist.insert(tkinter.INSERT, question.decode())

	while True:
		recvthread = threading.Thread(target=recvMess, args=(client,))
		recvthread.start()'''


	chatbar = StringVar()
	chatbar.set('')
	entryinput = Entry(gwindow, width = 140, textvariable=chatbar)
	entryinput.place(x=5, y=305, width=500, height=25)

	sendbutton = Button(gwindow, text="發言/投票",command=sendtext())  #發言及投票按鈕
	sendbutton.place(x=500, y=305, width=150, height=95)

	gwindow.mainloop()

login_window()
