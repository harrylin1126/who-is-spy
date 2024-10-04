import socket
import threading
import time
import random

HOST = '192.168.1.120'
PORT = 7000

player = []
# 角色身分確定
character = []
spy = []
villager = []

# 處理題目
question = [["可樂", "雪碧"], ["棒球", "羽球"]]
qu = random.choice(question)


# 投票
def voting():
    vote = []
    totalPlayer = len(player)
    for i in range(len(player)):
        global voteMess

        voteMess = "現在進行玩家" + str(i + 1) + "的投票(不用投自己)"

        for j in range(len(player)):
            if j != i:
                player[j].send(voteMess.encode())
            else:
                player[j].send("等待中不要傳東西，你傳了也沒差!".encode())

        for o in range(len(player)):
            if o != i:
                voteMessage = player[o].recv(1024)
                voteMessage = voteMessage.decode()
                print(voteMessage)
                vote.append(voteMessage)
            
        counter = vote.count("1")
        if counter > len(vote) // 2:
            for k in range(len(spy)):
                if player[i] == spy[k]:
                    spyout = "您已被淘汰，您的身分是臥底!"
                    spywait = "等待遊戲結果!!"
                    player[i].send(spyout.encode())
                    player[i].send(spywait.encode())
                    spy.remove(spy[k])
                    player.remove(player[i])
                    break

            for h in range(len(villager)):
                if player[i] == villager[h]:
                    villagerout = "您已被淘汰，您的身分是平民!"
                    villwait = "等待遊戲結果!!"
                    player[i].send(villagerout.encode())
                    player[i].send(villwait.encode())
                    villager.remove(villager[h])
                    player.remove(player[i])
                    break
        counter = 0
        vote = []


# 處裡連線&玩家名稱
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(6)

print('server start at: %s:%s' % (HOST, PORT))
print('Server waits.')

client1, addr1 = server.accept()
player.append(client1)
character.append(client1)
client1.send("你是玩家1  等待其他玩家連入......".encode())
print("One client connects.\n")
client2, addr2 = server.accept()
player.append(client2)
character.append(client2)
client2.send("你是玩家2  等待其他玩家連入......".encode())
print("Two clients connect.\n")
client3, addr3 = server.accept()
player.append(client3)
character.append(client3)
client3.send("你是玩家3  等待其他玩家連入......".encode())
print("Three clients connects.\n")
client4, addr4 = server.accept()
player.append(client4)
character.append(client4)
client4.send("你是玩家4  等待其他玩家連入......".encode())
print("Four clients connect.\n")
client5, addr5 = server.accept()
player.append(client5)
character.append(client5)
client5.send("你是玩家5  等待其他玩家連入......".encode())
print("Five clients connects.\n")
client6, addr6 = server.accept()
player.append(client6)
character.append(client6)
client6.send("你是玩家6  等待其他玩家連入......".encode())
print("Six clients connect.\n")


user = []
for i in range(6):  ##### 記得改這是測試版
    k = player[i].recv(1024)
    k = k.decode()
    user.append(k)

playerName = "玩家1: " + user[0] + " 玩家2: " + user[1] + " 玩家3: " + user[2] + " 玩家4: " + user[3] + " 玩家5: " + \
             user[4] + " 玩家6: " + user[5]
print(playerName)
for i in range(6):  ##### 記得改這是測試版
    player[i].send(playerName.encode())
    time.sleep(1)

# 傳送題目
for i in range(2):  ##### 記得改這是測試版
    spy.append(random.choice(character))
    character.remove(spy[i])
    spyqu = "題目是:" + qu[1]
    spy[i].send(spyqu.encode())
    time.sleep(1)
for i in range(4):  ##### 記得改這是測試版
    villager.append(character[i])
    villqu = "題目是:" + qu[0]
    villager[i].send(villqu.encode())
    time.sleep(1)

# 遊戲開始
print("遊戲開始")

while len(spy) > 0 and len(villager) > 2:  ##### 記得改這是測試版
    for i in range(len(player)):  # 處理接收與傳送訊息
        if player[i] in villager or player[i] in spy:
            time.sleep(1)
            player[i].send("輪到你發言: ".encode())
            inmessage = player[i].recv(1024)
            inmessage = inmessage.decode()
            print(inmessage)
        for j in range(len(player)):
            outMess = user[i] + ": " + inmessage
            player[j].send(outMess.encode())

    for i in range(len(player)):  # 進行投票
        player[i].send("準備進行投票，請對懷疑是臥底的玩家輸入1，其餘的輸入0".encode())
    voting()

# 勝負判斷
if len(spy) == 0:
    spyLose = "遊戲結束，本局由村民獲勝!!村民的題目是:" + qu[0] + "臥底的題目是:" + qu[1]
    client1.send(spyLose.encode())
    client2.send(spyLose.encode())
    client3.send(spyLose.encode())
    client4.send(spyLose.encode())
    client5.send(spyLose.encode())
    client5.send(spyLose.encode())
else:
    villLose = "遊戲結束，本局由臥底獲勝!!村民的題目是:" + qu[0] + "臥底的題目是:" + qu[1]
    client1.send(villLose.encode())
    client2.send(villLose.encode())
    client3.send(villLose.encode())
    client4.send(villLose.encode())
    client5.send(villLose.encode())
    client6.send(villLose.encode())


































