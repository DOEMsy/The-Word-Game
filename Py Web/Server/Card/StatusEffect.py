from Card.Card import Card
from ExternalLibrary.ExternalLibrary import GetUID


class StatusEffect(Card):

    def __init__(self, name: str, desc: str, label: set, combatAmend = 0, isHalo=False, acctingOnWho=None):
        super().__init__(name, desc)

        self.Type = "StatusEffect"
        self.Label = label  # 标签
        self.AcctingOnWho = acctingOnWho  # 作用目标
        self.IsHalo = isHalo  # 是否是光环
        self.basicCombatAmend = combatAmend
        # 出场作用就有UID,同一个效果作用在不同单位上UID是相同的?
        self.UID = GetUID()

    # 对战力作用
    def CombatAmend(self) -> int:
        return self.basicCombatAmend

    # 字典化
    def dict(self) -> dict:
        return {
            "Name": self.Name,
            "Desc": self.Desc,
            "CombatAmend": self.CombatAmend,
            "Label": list(self.Label), #json 不允许出现 set
            "UID": self.UID
        }

    # 待完善...
