from Card.Card import *


class SkillCard(Card):
    def __init__(self, name, desc, level, attr):
        super().__init__(name, desc)
        self.Level = level
        self.Attr = attr
        self.Type = "SkillCard"

    def Play(self, player, to):
        return True

    def OnCourt(self):
        return True

    def Round(self):
        return True

    def Finish(self):
        return True

    def lstr(self):
        return ""

    def sstr(self):
        return ""
