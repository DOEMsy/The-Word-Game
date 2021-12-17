from copy import deepcopy
from random import randint, sample

from ExternalLibrary import MsyEvent
from ExternalLibrary.ExternalLibrary import toDict
from Game.Label import Is


class Player(object):

    def __init__(self, Name, NO):
        self.Desc = ""
        self.OpPlayer = None  # Player 对手玩家
        self.ThisGame = None  # Game 当前游戏

        self.HandCards = []  # list[card...] 手牌
        self.RawPile = []  # list[card...] 抽牌堆
        self.UnitGrave = []  # list[card...] 墓地
        self.Lines = [[] for _ in range(3)]  # list[list[card...]...] 战区
        self.lineExisEffect = {x:dict() for x in range(3)}  # 战区存在时效果注册表
        self.IsAbstain = False  # bool 放弃？

        self.UIDCardDict = dict()  # 根据UID快速获取该玩家战场上的卡牌，由Game完全接管，但是无法用来从战场删除该卡

        self.Name = Name  # str 玩家名
        self.NO = NO  # int 玩家编号
        self.Health = 2  # int 玩家生命值
        self.TolCombat = 0  # int 玩家总战力

        self.POP_POINT_MAX = 5
        self.POP_POINT = 0
        self.POP_DONE = False
        self.ActionAttributeValue = {"禁咒":0}
        self.AI = None

    def Load_AI(self,AI):
        self.AI = AI
        AI.player = self
        AI.ThisGame = self.ThisGame
        AI.OpPlayer = self.OpPlayer
        AI.Init_Oup()

    def Reload_POP_POINT(self):
        self.POP_POINT = self.POP_POINT_MAX
        self.POP_DONE = False
        self.Sort_Hand_Card()


    def UpLevel_POP_POINT_MAX(self):
        self.POP_POINT_MAX += 2

    def Sort_Hand_Card(self):
        self.HandCards.sort(key=lambda x:x.Level)

    # 出牌 每轮可以出8点（level）
    def PopCard(self, ins:list) -> bool:
        try:
            card_i = int(ins[0])
            if (len(self.HandCards) <= card_i): return False
            card = self.HandCards[card_i]

            # 自动补全 type uid
            ins = ins[0:1] + [card.Type,card.UID] + ins[1:]

            if (card.Level<=self.POP_POINT and card.Play(self, ins[1:])):
                # 历史出牌队列
                self.ThisGame.PlayCardQueue.append(card)
                # 发送出牌消息
                self.ThisGame.Print_Message("! " + self.Name + " 打出卡牌:\n" + card.lstr())

                # 玩家累计属性
                if(Is("禁咒",card)): self.ActionAttributeValue["禁咒"]+=1


                # 卡牌在操作过程中有可能改变卡牌顺序，要使用UID删除
                # del self.HandCards[card_i]
                for i in range(len(self.HandCards)):
                    if (self.HandCards[i].UID == card.UID):
                        self.HandCards.pop(i)
                        break

                self.POP_POINT -= card.Level

                # 出牌事件
                event = MsyEvent.Pop(
                    card=card,
                    player=self
                )
                self.ThisGame.eventMonitoring.Occurrence(event)
                return True
            else:
                return False
        except Exception as e:
            print("player pop error:", repr(e))
            return False

    # # 出牌
    # def PopCard(self, ins) -> bool:
    #     try:
    #         card_i = int(ins[0])
    #         if (len(self.HandCards) <= card_i): return False
    #         card = self.HandCards[card_i]
    #
    #         # 自动补全 type uid
    #         ins = ins[0:1] + [card.Type,card.UID] + ins[1:]
    #
    #         if (card.Play(self, ins[1:])):
    #             # 历史出牌队列
    #             self.ThisGame.PlayCardQueue.append(card)
    #             # 发送出牌消息
    #             self.ThisGame.Print_Message("! " + self.Name + " 打出卡牌:\n" + card.lstr())
    #
    #             # 玩家累计属性
    #             if(Is("禁咒",card)): self.ActionAttributeValue["禁咒"]+=1
    #
    #
    #             # 卡牌在操作过程中有可能改变卡牌顺序，要使用UID删除
    #             # del self.HandCards[card_i]
    #             for i in range(len(self.HandCards)):
    #                 if (self.HandCards[i].UID == card.UID):
    #                     self.HandCards.pop(i)
    #                     break
    #             # 出牌事件
    #             event = MsyEvent.Pop(
    #                 card=card,
    #                 player=self
    #             )
    #             self.ThisGame.eventMonitoring.Occurrence(event)
    #             return True
    #         else:
    #             return False
    #     except Exception as e:
    #         print("player pop error:", repr(e))
    #         return False

    # 获取卡牌
    def Pump(self, card):
        card.Pump(self)
        return True

    # 抽牌
    def GetCards(self, num) -> int:
        ct = 0
        rawPileSize = len(self.RawPile)
        while (ct < num and rawPileSize > 0):
            p = randint(0, rawPileSize - 1)
            card = self.RawPile.pop(p)
            card.Pump(self)
            # self.HandCards.append(card)
            rawPileSize -= 1
            ct += 1
        self.ThisGame.Print_Message(
            self.Name + " 抽取了 " + str(ct) + " 张卡牌")
        return ct

        # 抽牌，从对方卡堆

    def GetCards_FromOp(self, num) -> int:
        ct = 0
        RawPile = self.OpPlayer.RawPile
        rawPileSize = len(RawPile)
        while (ct < num and rawPileSize > 0):
            p = randint(0, rawPileSize - 1)
            card = RawPile.pop(p)
            card.Pump(self)
            # self.HandCards.append(card)
            rawPileSize -= 1
            ct += 1
        self.ThisGame.Print_Message(
            self.Name + " 从对方的牌堆中抽取了 " + str(ct) + " 张卡牌")
        return ct

    # 弃牌
    def ThrowCards_withIlist(self, card_is) -> bool:
        if (len(card_is) == 0): return True
        card_is = list(set(card_is))[::-1]
        if (card_is[0] > len(self.HandCards) - 1):
            return False
        else:
            for card_i in card_is:
                self.HandCards[card_i].Aban()
                self.HandCards.pop(card_i)
            return True

    def ThrowCards_withUID(self, UID) -> bool:
        for card_i in range(len(self.HandCards)):
            if (self.HandCards[card_i].UID == UID):
                self.HandCards[card_i].Aban()
                self.HandCards.pop(card_i)
                return True
        return False

    def ThrowCards_withUIDList(self, UIDList) -> bool:
        for UID in UIDList:
            self.ThrowCards_withUID(UID)
        # 一定返回True
        return True

    def ThrowCards_ALL(self) -> bool:
        self.ThrowCards_withIlist(range(len(self.HandCards)))
        return True

    # 返回实际丢弃卡牌数目
    def ThrowCards_RandForNum(self, num) -> int:
        num = min(num, len(self.HandCards))
        self.ThrowCards_withIlist(sample(range(len(self.HandCards)), num))
        return num

    # 计算战力
    def CalculateCombat(self) -> bool:
        self.TolCombat = 0
        for Line in self.Lines:
            for card in Line:
                if (card.Type == "UnitCard"):
                    self.TolCombat += card.Combat()
        return True

    # 结算场上技能
    def SettlementOnCourtSkill(self) -> bool:
        self.ThisGame.gameLock.acquire()
        for card in self.UIDCardDict.values():
            card.OnCourt()
        self.ThisGame.gameLock.release()
        return True

    # 注册 战区存在时效果
    def RegisterLineExisEffect(self,card,li):
        try:
            self.lineExisEffect[li][card.UID] = card
        except Exception as e:
            print("player register card line exisEffect error.","playerNO:",self.NO,",cardUID:",card.UID,",",repr(e))

    # 注销 战区存在时效果
    def UnRegisterLineExisEffect(self,card,li):
        try:
            self.lineExisEffect[li].pop(card.UID)
        except Exception as e:
            print("player unregister card line exisEffect error.","playerNO:",self.NO,",cardUID:",card.UID,",",repr(e))

    # 字典化
    def dict(self):
        return{
            "NO": self.NO,
            "Name": self.Name,
            "Desc": self.Desc,
            "Health": self.Health,
            "HandCards":toDict(self.HandCards),
        }

    def pack(self):
        return {
            "NO": self.NO,
            "Name": self.Name,
            "Desc": self.Desc,
            "Health": self.Health,
        }
