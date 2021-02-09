from Card.StatusEffect import StatusEffect
from Game.Label import Is


# --------------- 灵魂虚弱 -----------------

class BodyWeakEffect(StatusEffect):
    def __init__(self, combatAmend):
        self.maxCombatAmend = combatAmend
        super().__init__(
            name="灵魂虚弱",
            desc="减少单位{}点战斗力".format(combatAmend),
            label={"魔法"},
        )

    def CombatAmend(self):
        res = max(0, self.maxCombatAmend - self.AcctingOnWho.Level+1)
        # desc 是会变动的
        self.Desc = "减少单位{}点战斗力".format(res)
        return -res


# --------------- 高速演算 -----------------

class FastSpeedCalculus(StatusEffect):
    def __init__(self, combatAmend):
        super().__init__(
            name="高速演算",
            desc="该单位采用了高效的作战方案，战斗力+{}"
                .format(combatAmend),
            combatAmend=combatAmend,
            label={"魔法"}
        )


# --------------- 夜行 -----------------

class Nocturnal(StatusEffect):
    def __init__(self, combatAmend):
        super().__init__(
            name="夜行",
            desc="该单位在夜间时战斗力+{}"
                .format(combatAmend),
            combatAmend=combatAmend,
            label={"特性"}
        )

    def CombatAmend(self):
        if (self.ThisGame.DayOrNight == False):
            return self.basicCombatAmend
        else:
            return 0

# --------------- 鼓舞 -----------------

class KingTactics(StatusEffect):
    def __init__(self, combatAmend):
        super().__init__(
            name="鼓舞",
            desc="该单位振奋了，战斗力+{}"
                .format(combatAmend),
            combatAmend=combatAmend,
            label={"战术"}
        )
