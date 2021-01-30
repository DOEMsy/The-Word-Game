from Card.Card import Card
from ExternalLibrary.ExternalLibrary import GetUID


class StatusEffect(Card):

    def __init__(self, name: str, desc: str, basisCombatAmend: int, label: [], acctingOnWho=None):
        super().__init__(name, desc)

        self.Type = "StatusEffect"
        self.BasisCombatAmend = basisCombatAmend  # 战力偏移值
        self.Label = label  # 标签
        self.AcctingOnWho = acctingOnWho  # 作用目标

        #出场作用就有UID
        self.UID = GetUID()


    # 对战力作用
    def CombatAmend(self) -> int:
        return self.BasisCombatAmend

    #字典化
    def dict(self)->dict:
        return{
            "Name": self.Name,
            "Desc": self.Desc,
            "CombatAmend": self.CombatAmend,
            "Label": self.Label,
            "UID":self.UID
        }

    #待完善...