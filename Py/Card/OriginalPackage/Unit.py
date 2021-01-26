from Card.UnitCard import UnitCard


class Wolf(UnitCard):
    def __init__(self):
        super().__init__(
            name="狼",
            desc="森林中常见的野生动物",
            combat=2,
            level=1,
            label=[
                "Animal",
            ]
        )


class ImperialSoldier(UnitCard):
    def __init__(self):
        super().__init__(
            name="帝国士兵",
            desc="一名普普通通的士兵，本本分分的谋生",
            combat=3,
            level=1,
            label=[
                "Humanoid",
            ]
        )


class Goblin(UnitCard):
    def __init__(self):
        super().__init__(
            name="哥布林",
            desc="小型的野生哥布林，是一种常见的魔物",
            combat=2,
            level=1,
            label=[
                "Humanoid",
            ]
        )
