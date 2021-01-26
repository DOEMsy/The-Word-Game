class StatysEffect(object):
    def __init__(self, name, desc, basisCombatAmend, attrs, acctingOnWho=None):
        self.Name = name
        self.Desc = desc
        self.BasisCombatAmend = basisCombatAmend
        self.Attrs = attrs
        self.AcctingOnWho = acctingOnWho

    def CombatAmend(self):
        return self.BasisCombatAmend
