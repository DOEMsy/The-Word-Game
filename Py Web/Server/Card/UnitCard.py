from Card.Card import *


class UnitCard(Card):
    def __init__(self, name, desc, combat, level, label):
        super().__init__(name, desc)
        self.SelfCombat = combat
        self.Level = level
        self.Label = label
        self.Type = "UnitCard"
        self.Status = []

    # ins =  [card_type,to...]
    # 对于普通单位牌，to 只有一项
    def Play(self, player, ins):
        try:
            card_type = ins[0]
            to = list(map(int,ins[1:]))
            if(card_type!=self.Type):   return False
            if (3 >= to[0] > 0):
                player.Lines[to[0] - 1].append(self)
                self.Debut()
            elif (-3 <= to[0] < 0):
                player.OpPlayer.Lines[-1 - to[0]].append(self)
                self.Debut()
            else:
                return False
            return True
        except:
            return False

    def Combat(self):
        res = self.SelfCombat
        for se in self.Status:
            res += se.CombatAmend()
        return res

    def Debut(self):
        return True

    def OnCourt(self):
        return True

    def Round(self):
        return True

    def ToNextTurn(self):
        return True

    def Dead(self):
        return True

    def lstr(self):
        return "[{},{},{},{},{}]".format(self.Type, self.Name, self.Combat(), self.Level, self.Desc)

    def sstr(self):
        return "[{},{},{}]".format(self.Name, self.Combat(), self.Level)
