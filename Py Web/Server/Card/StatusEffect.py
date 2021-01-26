class StatysEffect(object):
    def __init__(self, name: str, desc: str, basisCombatAmend: int, label: [], acctingOnWho=None):
        self.Name = name  # 名称
        self.Desc = desc  # 介绍
        self.BasisCombatAmend = basisCombatAmend  # 战力偏移值
        self.Label = label  # 标签
        self.AcctingOnWho = acctingOnWho  # 作用目标

    # 对战力作用
    def CombatAmend(self) -> int:
        return self.BasisCombatAmend

    #待完善...