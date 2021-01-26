from Card.Card import *


class SkillCard(Card):
    def __init__(self, name: str, desc: str, level: int, label: []):
        super().__init__(name, desc)
        self.Level = level  # 等级
        self.Label = label  # 标签
        self.Type = "SkillCard"  # 卡牌类型

    # 出牌
    def Play(self, player, to) -> bool:
        return True

    # 单位在场效果，打入战区，玩家回合结束结算
    def OnCourt(self) -> bool:
        return True

    # 全局效果，打入全局效果区，每轮结束结算
    def Round(self) -> bool:
        return True

    # 持续结束？待定
    def Finish(self) -> bool:
        return True

    # 场替
    def ToNextTurn(self)->bool:
        return True

    # 转换长字串，待完善
    def lstr(self) -> str:
        return ""

    # 转换短字串，待完善
    def sstr(self) -> str:
        return ""
