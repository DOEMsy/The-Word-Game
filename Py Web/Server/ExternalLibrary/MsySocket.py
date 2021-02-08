import json
import asyncio
import _thread
from threading import Lock

from time import sleep


# TCPConn通道类(socket.accept())
class Connet(object):
    def __init__(self, para: []):
        self.conn = para[0]  # tcp_conn
        self.addr = para[1]  # (host,port)
        self.toChan = []  # 发送消息channel
        self.bkChan = []  # 接收消息channel
        self.toChanLock = Lock()  # 发送消息队列线程锁
        self.bkChanLock = Lock()  # 接收消息队列线程锁
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete([self.send(), self.rev()])
        # loop.close()
        _thread.start_new_thread(self.send, ())  # 轮询监听发送消息
        _thread.start_new_thread(self.rev, ())  # 轮询监听接收消息

    # 获取消息
    # 从接收channel中获取一位数据，未获取则挂起，直到获取
    def GetRev(self):
        while (True):
            res = None
            self.bkChanLock.acquire()
            try:
                res = self.bkChan.pop(0)
            except IndexError:
                pass
            self.bkChanLock.release()
            if (res != None):
                print("#提取指令：", res)
                return res
            else:
                sleep(0.05)

    # 推送消息
    # 向发送channel推入一位数据，要求字典格式：
    #    msg = {
    #        "ins":"",
    #        "para":[
    #            "",
    #        ]
    #    }
    def Send(self, msg: dict):
        self.toChanLock.acquire()
        self.toChan.append(msg)
        self.toChanLock.release()
        print("#推入指令：", msg)

    # 从 channel 推出并发送一位数据至conn
    def send(self):
        while (True):
            msg = None
            self.toChanLock.acquire()
            try:
                msg = self.toChan.pop(0)
            except IndexError:
                pass
            self.toChanLock.release()
            if (msg != None):
                self.conn.send(
                    bytes(
                        # json 不允许出现 set
                        json.dumps(msg),
                        encoding="utf-8")
                )
                # print("#发送队列指令：", msg)
            sleep(0.05)

    # 监听接收一位数据从conn，推入channel
    def rev(self):
        while (True):
            rev = self.conn.recv(1024).decode("utf-8")
            self.bkChanLock.acquire()
            self.bkChan.append(json.loads(rev))
            self.bkChanLock.release()
            # print("#接收队列指令：",rev)
