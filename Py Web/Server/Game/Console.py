import _thread
import os
import socket

from ExternalLibrary.ExternalLibrary import GetAllCardSstrList, GetCardWithUID
from ExternalLibrary.MsySocket import Connet


class Console(object):
    def __init__(self,game):
        self.game = game

    def StartServer(self):
        self.Host = socket.gethostname()
        self.Port = 27126

        self.comServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comServer.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.comServer.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))  # 每60秒发送探测包
        self.comServer.bind((self.Host, self.Port))
        self.comServer.listen(1)

        self.ComClient = Connet(self.comServer.accept(),False)

        _thread.start_new_thread(self.handle, ())  # 处理命令的线程
        return True

    # 处理指令
    def handle(self):
        while(True):
            try:
                cmd = self.ComClient.GetRev()
                ins = cmd["ins"]
                para = cmd["para"]
                if(ins=="test"):
                    self.ComClient.Send({0:["test is ok"]})
                elif(ins=="show"):
                    self.show(para)
                else:
                    self.ComClient.Send({0:"wrong command!"})
            except Exception as e:
                self.ComClient.Send({0:repr(e)})

    def show(self,para):
        if(para[0]=="cardlist"):
            if(para[1]=="all"):
                # 传输数据过大，去世了 2021.3.3 21:48
                self.ComClient.Send({0:GetAllCardSstrList()})
        elif(para[0]=="card"):
            UID = int(para[1])
            self.ComClient.Send({0:GetCardWithUID(UID).lstr()})