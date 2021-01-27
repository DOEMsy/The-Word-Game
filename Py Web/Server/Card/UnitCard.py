from Card.Card import *


class UnitCard(Card):
    def __init__(self, name: str, desc: str, combat: int, level: int, label: []):
        super().__init__(name, desc)
        self.SelfCombat = combat  # 基础战斗力
        self.Level = level  # 等级
        self.Label = label  # 标签
        self.Type = "UnitCard"  # 卡牌类型
        self.Status = []  # 卡牌状态

    # 出牌
    # ins =  [card_type,to...]
    # 对于普通单位牌，to 只有一项
    def Play(self, player, ins) -> bool:
        try:
            card_type = ins[0]
            to = list(map(int, ins[1:]))
            if (card_type != self.Type):   return False
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

    # 战斗力
    def Combat(self) -> int:
        res = self.SelfCombat
        for se in self.Status:
            res += se.CombatAmend()
        return res

    # 出牌效果
    def Debut(self) -> bool:
        return True

    # 单位在场效果，打入战区，玩家回合结束结算
    def OnCourt(self) -> bool:
        return True

    # 全局效果，打入全局效果区，每轮结束结算
    def Round(self) -> bool:
        return True

    # 场替
    def ToNextTurn(self) -> bool:
        return True

    # 死亡
    def Dead(self) -> bool:
        return True

    # 转换长字串
    def lstr(self) -> str:
        return "[{},{},{},{},{}]".format(self.Type, self.Name, self.Combat(), self.Level, self.Desc)

    # 转换短字串
    def sstr(self) -> str:
        return "[{},{},{}]".format(self.Name, self.Combat(), self.Level)

    # 转换dict
    def dict(self) -> dict:
        res = {
            "Name":self.Name,
            "Desc":self.Desc,
            "Type":self.Type,
            "Combat":self.Combat(),
            "Label":self.Label,
            "Level":self.Level,
            "SelfCombat":self.SelfCombat,
            "Status":self.Status,
        }
        return res
