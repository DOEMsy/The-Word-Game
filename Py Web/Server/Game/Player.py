from random import randint


class Player(object):

    def __init__(self, Name, NO):
        self.OpPlayer = None
        self.ThisGame = None

        self.HandCards = []
        self.RawPile = []
        self.UnitGrave = []
        self.Lines = [[] for _ in range(3)]
        self.IsAbstain = False

        self.Name = Name
        self.NO = NO
        self.Health = 3
        self.TolCombat = 0

    def PopCard(self,ins):
        try:
            card_i = int(ins[0])
            if (len(self.HandCards) <= card_i): return False
            card = self.HandCards[card_i]
            if (card.Play(self, ins[1:])):
                #历史出牌队列
                self.ThisGame.PlayCardQueue.append(card)
                del self.HandCards[card_i]
                return True
            else:
                return False
        except:
            return False

    def GetCards(self, num):
        ct = 0
        rawPileSize = len(self.RawPile)
        while (ct < num and rawPileSize > 0):
            p = randint(0, rawPileSize - 1)
            card = self.RawPile[p]
            self.HandCards.append(card)
            del card
            rawPileSize -= 1
            ct += 1
        return ct

    def ThrowCards(self, card_is):
        if (len(card_is) == 0): return True
        card_is = list(set(card_is))
        if (card_is[0] > len(self.HandCards) - 1):
            return False
        else:
            i = 0
            for card_i in card_is:
                del self.HandCards[card_i - i]
                i += 1
            return True

    def CalculateCombat(self):
        self.TolCombat = 0
        for Line in self.Lines:
            for card in Line:
                if (card.Type == "UnitCard"):
                    self.TolCombat += card.Combat()
        return True

    def SettlementOnCourtSkill(self):
        for line in self.Lines:
            for card in line:
                card.OnCourt()
        return True
