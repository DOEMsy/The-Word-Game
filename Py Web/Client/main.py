import asyncio
import os
import socket
import re
import json

print("请输入服务器 host")
host = 0
port = 0
comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scrSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    host = input()
    #host = "192.168.1.101"
    if re.match(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$', host):
        port = [27015, 27016]
        comSocket.connect((host, port[0]))
        scrSocket.connect((host, port[1]))
        print("连接至服务器", host)
        # serverSocket.send('ok'.encode('utf-8'))
        break
    else:
        print("请输入正确的服务器 host:port")

while True:
    com = json.loads(comSocket.recv(1024).decode("utf-8"))
    # inp,prt,end
    ins = com["ins"]
    para = com["para"]

    if (ins == 'inp'):
        # 要求输入
        print(para)
        inp = []
        while(len(inp)==0):
            inp = input().split()
        comSocket.send(
            bytes(
                json.dumps({
                    "ins":inp[0],
                    "para":inp[1:]
                }),
                encoding="utf-8"
            )
        )
    elif (ins == 'prt'):
        # 提示消息
        print(para)
    elif (ins == 'scr'):
        # 刷新屏幕
        os.system('cls')
        scr = json.loads(scrSocket.recv(4096).decode("utf-8"))
        print(scr["scr"])
    elif (ins == 'end'):
        print(para)
        break

os.system('pause>nul')
