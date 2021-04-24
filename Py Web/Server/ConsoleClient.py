import _thread
import socket

from ExternalLibrary.MsySocket import Connet


class ConsoleClient(object):
    def __init__(self):
        pass

    def Start(self):
        self.Host = socket.gethostname()
        self.Port = 27126

        self.comServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comServer.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.comServer.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))  # 每60秒发送探测包
        while(True):
            try:
                self.comServer.connect((self.Host,self.Port))
                break
            except:
                pass
        print("连接成功")
        self.ComServer = Connet([self.comServer,(self.Host,self.Port)],False)
        _thread.start_new_thread(self.printRev, ())
        _thread.start_new_thread(self.inputCmd, ())


    def printRev(self):
        while True:
            oup = self.ComServer.GetRev()['0']
            if(type(oup)=="str"):
                print(oup)
            elif(type(oup)=="list"):
                for s in oup:
                    print(s)
            else:
                print(oup)

    def inputCmd(self):
        while True:
            cmd = input().split()
            if(len(cmd)>0):
                self.ComServer.Send({"ins":cmd[0],"para":cmd[1:]})


cons = ConsoleClient()
cons.Start()
while(True):pass