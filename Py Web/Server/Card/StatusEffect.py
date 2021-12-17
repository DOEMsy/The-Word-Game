from copy import deepcopy

from Card.Card import Card
from ExternalLibrary.ExternalLibrary import GetUID
from Game.Label import Is


class StatusEffect(Card):

    def __init__(self, name: str, desc: str, label: set, combatAmend = 0, isHalo=False, acctingOnWho=None):
        super().__init__(name, desc)

        self.Type = "StatusEffect"
        self.Label = label  # 标签
        self.AcctingOnWho = acctingOnWho  # 作用目标
        self.IsHalo = isHalo  # 是否是光环
        self.basicCombatAmend = combatAmend
        self.ThisGame = None
        # 出场作用就有UID,同一个效果作用在不同单位上UID是相同的?
        self.UID = GetUID()
        # 出场就具象化
        self.visualization = True

    # 对战力作用
    def CombatAmend(self) -> int:
        return self.basicCombatAmend

    def Apply(self,target):
        UID = self.UID
        target.Status[UID] = deepcopy(self)
        target.Status[UID].AcctingOnWho = target
        target.Status[UID].ThisGame = target.ThisGame

    def Is(self,Label):
        return Is(Label,self)

    def lstr(self):
        return "[{},{},{},\n{}]".format(self.UID, self.Type, self.Name, self.Desc)

    def sstr(self):
        return "[{},{},{}]".format(self.UID, self.Type, self.Name)

    # 字典化
    def dict(self) -> dict:
        return {
            "Name": self.Name,
            "Desc": self.Desc,
            "CombatAmend": self.CombatAmend(),
            "Label": list(self.Label), #json 不允许出现 set
            "UID": self.UID
        }

    def pack(self) -> dict:
        return {
            "Name": self.Name,
            "Desc": self.Desc,
            "CombatAmend": self.CombatAmend(),
            # 效果类型 0：未知，1：战斗力增益，2：战斗力减益，3：护盾
            "Effect": 0,
            # 作用效果值
            "Value": self.CombatAmend(),
            "Label": list(self.Label),  # json 不允许出现 set
            "UID": self.UID
        }
    # 待完善...
