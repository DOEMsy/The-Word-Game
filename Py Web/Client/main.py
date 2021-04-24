import asyncio
import os
import socket
import re
import json

print("请输入服务器 host")
host = 0
port = 0

# 长时间连接会断开？
comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scrSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 要求长时间保持存活
comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE,True)
comSocket.ioctl(socket.SIO_KEEPALIVE_VALS,(1,60*1000,30*1000)) #每60秒发送探测包

scrSocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE,True)
scrSocket.ioctl(socket.SIO_KEEPALIVE_VALS,(1,60*1000,30*1000))

while True:
    # host = input()
    host = "192.168.1.116"
    if re.match(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$', host):
        port = [27018, 27019]
        comSocket.connect((host, port[0]))
        scrSocket.connect((host, port[1]))
        print("连接至服务器", host)
        # serverSocket.send('ok'.encode('utf-8'))
        break
    else:
        print("请输入正确的服务器 host:port")

game = None
NO = None
prtQ = []
while True:
    com = json.loads(comSocket.recv(1024).decode("utf-8"))
    # inp,prt,end
    ins = com["ins"]
    para = com["para"]
    # print(ins,para)
    if (ins == 'inp'):
        # 要求输入
        print(para)
        inp = []
        while(len(inp)==0):
            inp = input().split()

        if(inp[0]=="pop"):
            try:
                cardtype = game["Players"][NO]["HandCards"][int(inp[1])]["Type"]
                cardUID = game["Players"][NO]["HandCards"][int(inp[1])]["UID"]
                inp.insert(2,cardtype)
                inp.insert(3,cardUID)
            except:
                pass

        comSocket.send(
            bytes(
                json.dumps({
                    "ins":inp[0],
                    "para":inp[1:]
                },ensure_ascii=False),
                encoding="utf-8"
            )
        )
    elif (ins == 'prt'):
        # 提示消息
        print(para)
    elif (ins == 'prtQ'):
        prtQ.append(para)
    elif (ins == 'scr'):
        # 刷新屏幕
        os.system('cls')
        tmp = scrSocket.recv(65536).decode("utf-8")
        # print(tmp)
        scr = json.loads(tmp)
        print(scr["scr"])

        game = scr["dic"]
        NO = game["YourNum"]
        can = len(prtQ)>0
        if(can):    print("-------------------------------------------")
        while(len(prtQ)>0):
            print(prtQ.pop(0)[0]+"\n")
        if(can):    print("-------------------------------------------")
        #print();print(scr["dic"])
        #open("scr.txt","w").write(str(scr["scr"]))
        #open("dic.txt","w").write(str(scr["dic"]))

    elif (ins == 'end'):
        print(para)
        break

os.system('pause>nul')
