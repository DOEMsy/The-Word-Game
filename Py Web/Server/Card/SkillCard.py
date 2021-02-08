from Card.Card import *


class SkillCard(Card):
    def __init__(self, name: str, desc: str, level: int, label: set):
        super().__init__(name, desc)
        self.Level = level  # 等级
        self.Label = label  # 标签
        self.Type = "SkillCard"  # 卡牌类型

    # 出牌
    def Play(self, player, ins) -> bool:
        try:
            card_type = ins[0]
            card_uid = int(ins[1])
            if (card_uid != self.UID): return False
            to = list(map(int, ins[2:]))
            if (card_type != self.Type):   return False
            if (not self.Debut(to)): return False
            return True
        except:
            return False

    # 出牌效果
    def Debut(self, ins) -> bool:
        return True

    # 单位在场效果，打入战区，玩家回合结束结算
    def OnCourt(self) -> bool:
        return True

    # 全局效果，打入全局效果区，每轮结束结算
    def Round(self) -> bool:
        return True

    # 持续结束？待定
    def Finish(self) -> bool:
        return False

    # 场替
    def ToNextTurn(self) -> bool:
        return True

    # 转换长字串，待完善
    def lstr(self) -> str:
        return "[{},{},{},{},{}]".format(self.UID, self.Type, self.Name, self.Level, self.Desc)

    # 转换短字串，待完善
    def sstr(self) -> str:
        return "[{},{},{}]".format(self.UID, self.Name, self.Level)

        # 转换dict

    def dict(self) -> dict:
        res = {
            "Name": self.Name,
            "Desc": self.Desc,
            "Type": self.Type,
            "Label": list(self.Label),  # json 不允许出现 set
            "Level": self.Level,
            "UID": self.UID,
        }
        return res