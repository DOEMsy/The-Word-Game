import asyncio
import os
import socket
import re
import json
import _thread
from threading import Lock
from time import sleep

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from idl.game import GameServer
from idl.game.ttypes import Req, Base


class GameClient():
    def __init__(self):
        print("请输入服务器 host")
        self.host = ""
        self.port = 0

        while True:
            # host = input()
            self.host = "127.0.0.1"
            if re.match(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$', self.host):
                self.port = 27018
                self.tsocket = TSocket.TSocket(self.host, self.port)
                self.transport = TTransport.TBufferedTransport(self.tsocket)
                self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
                self.client = GameServer.Client(self.protocol)
                print("连接至服务器", self.host)
                # serverSocket.send('ok'.encode('utf-8'))
                break
            else:
                print("请输入正确的服务器 host")

        self.player_NO = int(input("NO 0 or 1 ？"))# 0 # 1
        self.prt_que = []
        self.base_cnt = 0
        self.transport.open()



    def c_s_interactive(self):
        req = Req(
            player_NO=self.player_NO,
            ins="init_player",
            base=Base(
                status_code=1,
                status_message="ok",
                cnt=self.base_cnt,
            )
        )
        while (True):
            resp = self.client.what_should_I_do(req)
            req = self.do_com(resp)

    def do_com(self, resp):
        self.base_cnt = resp.base.cnt
        req = Req(
            player_NO=self.player_NO,
            ins="done", # 无用指令，同步用
            base=Base(
                status_code=1,
                status_message="ok",
                cnt=self.base_cnt,
            )
        )

        ins = resp.ins

        if (ins == 'prt'):
            msg = resp.msg
            print(msg)
        elif (ins == 'scr'):
            os.system('cls')
            screen = resp.screen
            print(screen)
            can = len(self.prt_que) > 0
            if (can):    print("-------------------------------------------")
            while (len(self.prt_que) > 0):
                print(self.prt_que.pop(0) + "\n")
            if (can):    print("-------------------------------------------")
        elif (ins == 'prtQ'):
            msg = resp.msg
            self.prt_que.append(msg)
        elif (ins == 'end'):
            msg = resp.msg
            print(msg)
        elif (ins == 'inp'):
            msg = resp.msg
            print(msg)
            inp = []
            while (len(inp) == 0):
                inp = input().split()
            req.ins = inp[0]
            req.para = inp[1:]
        elif (ins=='done'):
            pass

        return req


if __name__ == "__main__":
    game_client = GameClient()
    # _thread.start_new_thread(game_client.c_s_interactive, ())
    game_client.c_s_interactive()
    os.system('pause>nul')
