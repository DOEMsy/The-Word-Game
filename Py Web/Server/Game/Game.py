import json
import os
import random
from copy import deepcopy
import socket

from ExternalLibrary.MsySocket import Connet
from Game.Player import Player


class Game(object):
    def __init__(self):
        self.Players = [Player('Player1', 0), Player('Player2', 1)]  # [Player,Player] 玩家们
        self.Players[0].OpPlayer = self.Players[1]
        self.Players[1].OpPlayer = self.Players[0]
        self.Players[0].ThisGame = self.Players[1].ThisGame = self
        self.GlobalEffect = []  # [Card...] 全局效果
        self.PlayCardQueue = []  # [Card...] 出牌队列
        self.DayOrNight = random.choice([True, False])  # 白天？晚上？
        self.NumberOfBoard = 0  # 场次

        # server
        self.Host = 0  # str server host
        self.Port = 0  # [int,int] server port
        self.comServer = 0  # socket 指令服务端
        self.scrServer = 0  # socket 屏显服务端
        self.PComClient = []  # socket_conn 指令客户端
        self.PScrClient = []  # socket_conn 屏显客户端

    # 开启游戏服务器
    def StartServer(self) -> bool:
        # P2 Socket
        self.Host = "192.168.1.101"  # socket.gethostname()
        self.Port = [27015, 27016]
        self.comServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.scrServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comServer.bind((self.Host, self.Port[0]))
        self.scrServer.bind((self.Host, self.Port[1]))
        self.comServer.listen(2)
        self.scrServer.listen(2)
        print("服务启动于", self.Host + ':', self.Port)
        print("等待P1连接...")
        self.PComClient.append(Connet(self.comServer.accept()))
        self.PScrClient.append(Connet(self.scrServer.accept()))
        print("P1已经连接: ", self.PComClient[0].addr)
        self.PComClient[0].Send({
            "ins": "prt",
            "para": ["成功连接到服务器，等待p2"]
        })
        print("等待P2连接...")
        self.PComClient.append(Connet(self.comServer.accept()))
        self.PScrClient.append(Connet(self.scrServer.accept()))
        print("P2已经连接: ", self.PComClient[1].addr)
        print("游戏开始")
        self.PComClient[1].Send({
            "ins": "prt",
            "para": ["成功连接到服务器"]
        })
        self.PComClient[0].Send({
            "ins": "prt",
            "para": ["游戏开始"]
        })
        self.PComClient[1].Send({
            "ins": "prt",
            "para": ["游戏开始"]
        })
        return True

    # 场替
    def SettlementToNextTurn(self) -> bool:
        minCombat = min(self.Players[0].TolCombat, self.Players[1].TolCombat)
        for player in self.Players:
            if (player.TolCombat == minCombat):
                player.Health -= 1

        for NO in range(2):
            player = self.Players[NO]
            player.IsAbstain = False
            for i in range(3):
                tmp = []
                line = player.Lines[i]
                for card in line:
                    if (not card.ToNextTurn()):
                        tmp.append(card)
                player.Lines[i] = deepcopy(tmp)

        tmp = []
        for card in self.GlobalEffect:
            if (not card.ToNextTurn()):
                tmp.append(card)
        self.GlobalEffect = deepcopy(tmp)

        self.NumberOfBoard += 1
        self.DayOrNight = not self.DayOrNight
        return True

    # 死亡检测
    def DeathDetection(self) -> bool:
        for NO in range(2):
            player = self.Players[NO]
            for i in range(3):
                tmp = []
                line = player.Lines[i]
                for card in line:
                    # 0 濒死 <0 死亡
                    if not (card.Combat() < 0 and card.Dead()):
                        tmp.append(card)
                player.Lines[i] = deepcopy(tmp)
        return True

    # 结算轮
    def SettlementRound(self) -> bool:
        tmp = []
        for effect in self.GlobalEffect:
            effect.Round()
            if (not effect.Finish()):
                tmp.append(effect)
        self.GlobalEffect = deepcopy(tmp)
        return True

    # 结算战斗力
    def CalculateCombat(self):
        self.Players[0].CalculateCombat()
        self.Players[1].CalculateCombat()

    # 输出屏幕
    def PrintScreen(self, NO, POPONE=False) -> bool:
        player = self.Players[NO]
        opPlayer = player.OpPlayer
        oup = ""
        for i in range(3)[::-1]:
            oup += "{}: ".format(i + 1)
            for card in opPlayer.Lines[i]:
                oup += "{},".format(card.sstr())
            oup += "\n"
        oup += "-----------NA:{} CO:{}, HE:{} GV:{} CP:{} ----------\n".format(opPlayer.Name, opPlayer.TolCombat,
                                                                               opPlayer.Health, opPlayer.IsAbstain,
                                                                               len(opPlayer.HandCards))
        oup += "{}\n".format("Day" if (self.DayOrNight) else "Night")
        oup += "Gl: "
        for gl in self.GlobalEffect:
            oup += "{},".format(gl.sstr())
        oup += '\n'
        oup += "-----------NA:{} CO:{}, HE:{} GV:{} CP:{} ----------\n".format(player.Name, player.TolCombat,
                                                                               player.Health,
                                                                               player.IsAbstain, len(player.HandCards))
        for i in range(3):
            oup += "{}: ".format(i + 1)
            for card in player.Lines[i]:
                oup += "{},".format(card.sstr())
            oup += "\n"
        if (POPONE):
            oup += "It's you turn\n"
        else:
            oup += "It's NOT you turn,you can't move\n"

        oup += "You are Player{} now，Board {}\n".format(NO + 1, self.NumberOfBoard)
        oup += "HandCards:\n"
        card_i = 0
        for card in player.HandCards:
            oup += "{}. {},\n".format(card_i, card.lstr())
            card_i += 1

        self.PComClient[NO].Send({
            "ins": "scr",
            "para": []
        })
        self.PScrClient[NO].Send(
            {"scr": oup}
        )

        return True

    # 获取玩家行动
    def GetAndCROInstructions(self, NO) -> bool:
        player = self.Players[NO]
        msg = "请输入指令:"
        while (True):
            try:
                self.PComClient[NO].Send({
                    "ins": "inp",
                    "para": [msg]
                })
                inp = self.PComClient[NO].GetRev()
                ins = inp["ins"]
                if (ins == "giveup"):
                    player.IsAbstain = True
                    break
                elif (ins == "pop"):
                    '''
                        {
                            "ins":"pop",
                            "para":[
                                card_i,
                                card_type,
                                to...
                            ]
                        }
                    '''
                    if (player.PopCard(inp["para"])):
                        break
                    else:
                        pass
                # elif (ins[0] == "get"):
                #    if (len(ins) >= 2):
                #        player.GetCards(int(ins[1]))
                #        break
            except:
                pass
            msg = "指令错误，请重新输入:"

        return True
