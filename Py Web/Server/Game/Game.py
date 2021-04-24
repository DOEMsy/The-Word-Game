import json
import os
import random
from copy import deepcopy
import socket
import _thread
from threading import Lock
from time import sleep

from ExternalLibrary.ExternalLibrary import GetUID, Throw_VisualizationError
from ExternalLibrary.MsyEvent import EventMonitoring
from ExternalLibrary.MsySocket import Connet
from Game.Console import Console
from Game.Player import Player


class Game(object):
    def __init__(self):
        self.Players = [Player('Player1', 0), Player('Player2', 1)]  # [Player,Player] 玩家们
        self.Players[0].OpPlayer = self.Players[1]
        self.Players[1].OpPlayer = self.Players[0]
        self.Players[0].ThisGame = self.Players[1].ThisGame = self
        self.GlobalEffect = []  # [Card...] 全局效果
        self.PlayCardQueue = []  # [Card...] 出牌队列

        self.RealDayOrNight = random.choice([True, False])  # 真实的 白天？晚上？
        self.DayOrNight = self.RealDayOrNight  # 表现的 白天？晚上？

        self.NumberOfInnings = 0  # 场次
        self.UID = 1166  # 唯一识别ID
        self.UIDCardDict = dict()  # 根据UID快速获取场上卡牌，但是无法用来从战场删除该卡
        self.UIDCardDict_GlobalEffect = dict()  # 根据UID快速获取场上全局效果，但是无法用来从战场删除该效果

        # server
        self.Host = 0  # str server host
        self.Port = 0  # [int,int] server port
        self.comServer = 0  # socket 指令服务端
        self.scrServer = 0  # socket 屏显服务端
        self.PComClient = []  # socket_conn 指令客户端
        self.PScrClient = []  # socket_conn 屏显客户端

        # 事件处理
        self.gameLock = Lock()  # 游戏锁
        self.eventMonitoring = EventMonitoring()  # 总线
        self.eventMonitoring.ThisGame = self
        self.eventMonitoring.BundledTrigger("Death", self)  # 绑定game的死亡触发器

        # 控制台
        self.console = Console(self)

    # 开启游戏服务器
    def StartServer(self) -> bool:
        # Console Socket
        _thread.start_new_thread(self.console.StartServer,())

        # P2 Socket
        self.gameLock.acquire()
        self.Host = "192.168.1.116"  # socket.gethostname()
        self.Port = [27018, 27019]
        # 长时间连接会断开？
        self.comServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.scrServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 要求长时间保持存活
        self.comServer.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.comServer.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))  # 每60秒发送探测包

        self.scrServer.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.scrServer.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))  # 每60秒发送探测包

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
            "para": {"msg":"成功连接到服务器，等待p2",}
        })
        print("等待P2连接...")
        self.PComClient.append(Connet(self.comServer.accept()))
        self.PScrClient.append(Connet(self.scrServer.accept()))
        print("P2已经连接: ", self.PComClient[1].addr)
        print("游戏开始")
        self.PComClient[1].Send({
            "ins": "prt",
            "para": {"msg":"成功连接到服务器"}
        })
        # 开始游戏
        for comClient in self.PComClient:
            comClient.Send({
                "ins": "game_start",
                "mode": "normal",
                "players":[
                    self.Players[0].pack(),
                    self.Players[1].pack(),
                ],
                "para":[],
            })
        self.gameLock.release()
        return True

    # 结算局
    def SettlementToNextInnings(self) -> bool:
        self.gameLock.acquire()
        minCombat = min(self.Players[0].TolCombat, self.Players[1].TolCombat)
        for player in self.Players:
            if (player.TolCombat == minCombat):
                player.Health -= 1
                player.GetCards(3)  # 失败者获取3张牌
            else:
                player.GetCards(5)  # 胜利者获取5张牌

        self.InningsReplacement()

        self.NumberOfInnings += 1
        self.RealDayOrNight = not self.RealDayOrNight
        self.gameLock.release()
        return True

    # 场替，上层调用函数一定被加锁
    def InningsReplacement(self) -> bool:
        tmp_UIDCardDict = dict()
        for NO in range(2):
            player = self.Players[NO]
            player.IsAbstain = False
            tmp_pUIDCardDict = dict()
            tmp_lines = [[], [], []]
            for i in range(3):
                line = player.Lines[i]
                for card in line:
                    # 每个卡场替的操作只执行了一次
                    if (not card.ToNextTurn()):
                        tmp_lines[i].append(card)
                        tmp_pUIDCardDict[card.UID] = card
                        tmp_UIDCardDict[card.UID] = card
                    else:
                        self.Players[NO].UnitGrave.append(card)
            player.Lines = tmp_lines
            player.UIDCardDict = tmp_pUIDCardDict
        self.UIDCardDict = tmp_UIDCardDict

        tmp_GloalEffect = []
        tmp_UIDGlabalEffect = dict()
        for card in self.GlobalEffect:
            if (not card.ToNextTurn()):
                tmp_GloalEffect.append(card)
        self.GlobalEffect = tmp_GloalEffect
        self.UIDCardDict_GlobalEffect = tmp_UIDGlabalEffect
        return True

    # 死亡检测（0.2.0+ 弃用）
    # def DeathDetection(self) -> bool:
    #   for NO in range(2):
    #       player = self.Players[NO]
    #       for i in range(3):
    #           tmp = []
    #           line = player.Lines[i]
    #           for card in line:
    #               # 0 濒死 <0 死亡
    #               if not (card.Combat() < 0 and card.Dead()):
    #                   tmp.append(card)
    #           player.Lines[i] = deepcopy(tmp)
    #   return True

    # 死亡处理处理由死亡事件调用，已加锁
    #   死亡event = {
    #       "type" : "Death",
    #       "para" : [UID,OwnNO]
    #   }
    def DeathProcessing(self, event) -> bool:
        UID = event['para'][0]
        OwnNO = event['para'][1].OwnPlayer.NO
        for line in self.Players[OwnNO].Lines:
            try:
                for i in range(len(line)):
                    try:
                        card = line[i]
                        if (card.UID == UID):
                            line.pop(i)
                            self.Print_Message(
                                self.Players[OwnNO].Name + " 的单位 " + self.UIDCardDict[UID].Name + "(" + str(
                                    UID) + ")" + " 死亡")
                    except:
                        pass
            except:
                pass
        try:
            self.UIDCardDict.pop(UID)
        except:
            pass
        try:
            self.Players[OwnNO].UnitGrave.append(self.Players[OwnNO].UIDCardDict[UID])
            self.Players[OwnNO].UIDCardDict.pop(UID)
        except:
            pass

        # for i in range(len(self.Players[OwnNO].Lines)):
        #    for j in range(len(self.Players[OwnNO].Lines[i])):
        #        if (self.Players[OwnNO].Lines[i][j].UID == UID):
        #            self.Players[OwnNO].Lines[i].pop(j)
        # 随后发送死亡信号向客户端？暂定

        return True

    def AddCardToLine(self, player, li, card):
        if (not card.visualization):
            # 没有具象化，不允许使用
            Throw_VisualizationError(card)
        card.OwnNO = player.NO
        card.OwnPlayer = player
        card.Location = li
        card.ThisGame = self
        # 对没有存入牌库的卡牌，赋予UID
        if (card.UID == -1):   card.UID = GetUID()
        player.Lines[li].append(card)
        player.UIDCardDict[card.UID] = card
        self.UIDCardDict[card.UID] = card

    def AddCardToGlobal(self, card):
        card.Location = 3
        self.GlobalEffect.append(card)
        self.UIDCardDict_GlobalEffect[card.UID] = card

    # 结算轮
    def SettlementRound(self) -> bool:
        self.gameLock.acquire()
        self.DayOrNight = self.RealDayOrNight
        tmp = []
        for effect in self.GlobalEffect:
            effect.Round()
            if (not effect.Finish()):
                tmp.append(effect)
        self.GlobalEffect = tmp
        self.gameLock.release()
        return True

    # 结算战斗力
    def CalculateCombat(self):
        self.eventMonitoring.WaitingForEventsEmpty()
        self.gameLock.acquire()
        self.Players[0].CalculateCombat()
        self.Players[1].CalculateCombat()
        self.gameLock.release()

    # 输出屏幕
    def PrintScreen(self, NO, POPONE=False) -> bool:
        self.gameLock.acquire()
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

        oup += "You are Player{} now，Board {}\n".format(NO + 1, self.NumberOfInnings)
        oup += "HandCards:\n"
        card_i = 0
        for card in player.HandCards:
            oup += "{}. {},\n\n".format(card_i, card.lstr())
            card_i += 1

        dic = {
            "GlobalEffect": [],
            "DayOrNight": self.DayOrNight,
            "NumberOfBoard": self.NumberOfInnings,
            "PlayCardQueue": [],
            "Players": [
                self.Players[0].dict(),
                self.Players[1].dict(),
            ],
            "YourNum": NO,
        }

        self.PComClient[NO].Send({
            "ins": "scr",
            "para": []
        })
        self.PScrClient[NO].Send({
            "scr": oup,
            "dic": dic,
        })

        self.gameLock.release()

        return True

    # 获取玩家行动
    def GetAndCROInstructions(self, NO) -> bool:
        self.gameLock.acquire()
        player = self.Players[NO]
        msg = "请输入指令:"
        ct = 0
        while (True):
            try:
                self.PComClient[NO].Send({
                    "ins": "inp",
                    "para": [
                        msg,
                        str(ct)
                    ]
                })
                if (ct == 0):
                    self.PComClient[abs(NO - 1)].Send({
                        "ins": "prt",
                        "para": ["等待对手出牌..."]
                    })
                inp = self.PComClient[NO].GetRev()
                ins = inp["ins"]
                if (ins == "giveup"):
                    player.IsAbstain = True
                    self.Print_Message(player.Name + " 弃权了 ")
                    break
                elif (ins == "pop"):
                    '''
                        0.2.1+
                        {
                            "ins":"pop",
                            "para":[
                                card_i,
                                card_uid,
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
            ct += 1
        self.gameLock.release()
        return True

    def Print_Message(self, msg: str):
        self.PComClient[0].Send({
            "ins": "prtQ",
            "para": [msg]
        })
        self.PComClient[1].Send({
            "ins": "prtQ",
            "para": [msg]
        })
        return True

    def NormalEnd(self):
        os.system("pause")
        return True

    def com_card_pump(self,card):
        self.PScrClient[card.OwnNO].Send({
            "ins":"card_pump",
            "card":card.pack(),
        })