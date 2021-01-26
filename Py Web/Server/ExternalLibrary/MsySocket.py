import json
import asyncio
import _thread
from threading import Lock

from time import sleep


class Connet(object):
    def __init__(self, para: []):
        self.conn = para[0]
        self.addr = para[1]
        self.toChan = []
        self.bkChan = []
        self.toChanLock = Lock()
        self.bkChanLock = Lock()
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete([self.send(), self.rev()])
        # loop.close()
        _thread.start_new_thread(self.send, ())
        _thread.start_new_thread(self.rev, ())

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

    '''
        msg = {
            "ins":"",
            "para":[
                "",
            ]
        }
    '''

    def Send(self, msg: dict):
        self.toChanLock.acquire()
        self.toChan.append(msg)
        self.toChanLock.release()
        print("#推入指令：", msg)

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
                    bytes(json.dumps(msg),encoding="utf-8")
                )
                #print("#发送队列指令：", msg)
            sleep(0.05)

    def rev(self):
        while (True):
            rev = self.conn.recv(1024).decode("utf-8")
            self.bkChanLock.acquire()
            self.bkChan.append(json.loads(rev))
            self.bkChanLock.release()
            #print("#接收队列指令：",rev)