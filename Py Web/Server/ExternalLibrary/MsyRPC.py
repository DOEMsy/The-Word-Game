import json
import asyncio
import _thread
from threading import Lock
from time import sleep

from idl.game import GameServer
from idl.game import ttypes
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from idl.game.ttypes import Resp, Base, Req


# 指令管道
class Channel(object):
    def __init__(self,islog = True):
        self.toChan = []  # 发送消息channel resp
        self.bkChan = []  # 接收消息channel req
        self.toChanLock = Lock()  # 发送消息队列线程锁
        self.bkChanLock = Lock()  # 接收消息队列线程锁
        self.islog = islog

    # 获取消息
    # 从接收channel中获取一位数据，未获取则挂起，直到获取
    def GetReq(self):
        while (True):
            res = None
            self.bkChanLock.acquire()
            try:
                res = self.bkChan.pop(0)
            except IndexError:
                pass
            self.bkChanLock.release()

            if (res != None):
                if(self.islog): print("#提取指令：", res)
                return res
            else:
                sleep(0.05)

    # 从接收channel中获取一位数据，未获取则挂起，直到获取
    def GetResp(self):
        while (True):
            res = None
            self.toChanLock.acquire()
            try:
                res = self.toChan.pop(0)
            except IndexError:
                pass
            self.toChanLock.release()
            if (res != None):
                return res
            else:
                sleep(0.05)

    # 推送消息
    # 向发送channel推入一位Resp数据
    def PushResp(self, msg: Resp):
        self.toChanLock.acquire()
        self.toChan.append(msg)
        self.toChanLock.release()
        if(self.islog and msg.ins!='scr'): print("#推入指令：", msg)

    # 推送消息
    # 向发送channel推入一位Req数据
    def PushReq(self, msg: Req):
        self.bkChanLock.acquire()
        self.bkChan.append(msg)
        self.bkChanLock.release()


class Handler(object):
    def __init__(self, game):
        self.game = game
        self.channels = game.Clients
        # 断线重连上一次屏幕暂存
        self.last_scr_resp = [
            Resp(ins='scr',screen='[等待游戏开始...]'),
            Resp(ins='scr',screen='[等待游戏开始...]'),
        ]
        self.last_prt_resp = [
            Resp(ins='prt',msg=''),
            Resp(ins='prt',msg=''),
        ]

    def what_should_I_do(self, req):
        player_NO = req.player_NO
        if(req.ins!="done"):
            self.channels[player_NO].PushReq(req)

        # 断线重连 返回上一次屏幕结果
        resp = Resp()
        if(req.ins=="init_player"):
            resp = self.last_scr_resp[player_NO]
            self.channels[player_NO].PushResp(self.last_prt_resp[player_NO])
        else:
            resp = self.channels[player_NO].GetResp()


        resp.base = Base(status_code=1,status_message="ok",cnt=req.base.cnt+1)
        if(resp.ins=='scr'):
            self.last_scr_resp[player_NO] = resp
        if(resp.ins=='prt'):
            self.last_prt_resp[player_NO] = resp
        return resp


    def get_msg(self, req):
        return Resp(
            player_NO=req.player_NO,
            ins="?error?",
            base=Base(
                status_code=-1,
                status_message="接口没有实现",
                cnt=req.base.cnt + 1,
            )
        )


class RPCServer():
    def __init__(self, game, host, port):
        self.host = host
        self.port = port
        self.game = game
        self.rpcServer = TServer.TThreadPoolServer(
            GameServer.Processor(Handler(self.game)),
            TSocket.TServerSocket(self.host, self.port),
            TTransport.TBufferedTransportFactory(),  # 传输方式，使用buffer
            TBinaryProtocol.TBinaryProtocolFactory(),  # 传输的数据类型：二进制
        )

    def start(self):
        _thread.start_new_thread(self.rpcServer.serve,())
