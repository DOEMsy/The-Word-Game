from random import randint

from Card.SkillCard import SkillCard


class FlameStrike(SkillCard):
    def __init__(self):
        super().__init__(
            name="烈焰风暴",
            desc="对全场所有单位造成0-8点伤害",
            level=1,
            label=[

            ]
        )
        self.minDamage = 0
        self.maxdamage = 8

    def Debut(self, ins) -> bool:
        # game = self.ThisGame
        # for NO in range(2):
        #    player = game.Players[NO]
        #    for i in range(3):
        #        line = player.Lines[i]
        #        for j in range(len(line)):
        #            card = line[j]
        #            card.GetDamage(self.damage)
        for player in self.ThisGame.Players:
            for line in player.Lines:
                for card in line:
                    card.GetDamage(randint(self.minDamage,self.maxdamage))
        return True
