from random import randint

from ExternalLibrary.ExternalLibrary import toDict


class Player(object):

    def __init__(self, Name, NO):
        self.OpPlayer = None  # Player 对手玩家
        self.ThisGame = None  # Game 当前游戏

        self.HandCards = []  # list[card...] 手牌
        self.RawPile = []  # list[card...] 抽牌堆
        self.UnitGrave = []  # list[card...] 墓地
        self.Lines = [[] for _ in range(3)]  # list[list[card...]...] 战区
        self.IsAbstain = False  # bool 放弃？

        self.Name = Name  # str 玩家名
        self.NO = NO  # int 玩家编号
        self.Health = 3  # int 玩家生命值
        self.TolCombat = 0  # int 玩家总战力

    # 出牌
    def PopCard(self, ins) -> bool:
        try:
            card_i = int(ins[0])
            if (len(self.HandCards) <= card_i): return False
            card = self.HandCards[card_i]
            if (card.Play(self, ins[1:])):
                # 历史出牌队列
                self.ThisGame.PlayCardQueue.append(card)
                del self.HandCards[card_i]
                return True
            else:
                return False
        except:
            return False

    # 抽牌
    def GetCards(self, num) -> int:
        ct = 0
        rawPileSize = len(self.RawPile)
        while (ct < num and rawPileSize > 0):
            p = randint(0, rawPileSize - 1)
            card = self.RawPile[p]
            card.Pump()
            self.HandCards.append(card)
            del card
            rawPileSize -= 1
            ct += 1
        return ct

    # 弃牌
    def ThrowCards(self, card_is) -> bool:
        if (len(card_is) == 0): return True
        card_is = list(set(card_is))
        if (card_is[0] > len(self.HandCards) - 1):
            return False
        else:
            i = 0
            for card_i in card_is:
                self.HandCards[card_i - i].Aban()
                del self.HandCards[card_i - i]
                i += 1
            return True

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
        for line in self.Lines:
            for card in line:
                card.OnCourt()
        return True

    def dict(self):
        return {
            "HandCards":toDict(self.HandCards),
            "RawPile":toDict(self.RawPile),
            "UnitGrave":toDict(self.UnitGrave),
            "Lines":[
                toDict(self.Lines[0]),
                toDict(self.Lines[1]),
                toDict(self.Lines[2]),
            ],
            "Name":self.Name,
            "NO":str(self.NO),
            "Health":str(self.Health),
            "TolCombat":str(self.TolCombat),
        }
