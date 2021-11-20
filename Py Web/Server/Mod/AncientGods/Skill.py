from copy import deepcopy
from random import randint, choice

import numpy as np

from Card.SkillCard import SkillCard
from Card.StatusEffect import StatusEffect
from Card.UnitCard import UnitCard
from ExternalLibrary.ExternalLibrary import GetUID, ConcretizationCard, GetRandCard
from Game.Label import Is

# --------------- 屠戮 -----------------
# 只能通屠戮骑士获得
class Extirpate(SkillCard):
    def __init__(self):
        self.minDamage = 0
        self.maxDamage = 8
        super().__init__(
            name="屠戮",
            desc="对目标行所有单位造成{}~{}点神术伤害"
                 "".format(self.minDamage, self.maxDamage),
            level=4,
            label={
                "神术"
            }
        )

    def _debut(self, ins) -> bool:
        tarline = None
        if (3 >= ins[0] > 0):
            tarline = self.OwnPlayer.Lines[ins[0] - 1]
        # 打到对面牌区
        elif (-3 <= ins[0] < 0):
            tarline = self.OwnPlayer.OpPlayer.Lines[-ins[0] - 1]
        else:
            return False
        for card in tarline:
            card.GetDamage(
                randint(self.minDamage, self.maxDamage),
                self.Label
            )
        return True

# --------------- 契约·无色 -----------------

class Colorless(SkillCard):
    def __init__(self):
        self.throw_num = 2
        super().__init__(
            name="契约·无色",
            desc="象征着空无的恶魔，可以抹除现实一切现象的存在\n"
                 "◇恶魔契约：这张牌是一张禁咒牌，需要支付某种代价\n"
                 "◇无色：对场上所有单位场替判定，代价是己方随机弃{}张牌"
                 "".format(self.throw_num),
            level=5,
            label={
                "禁咒","恶魔契约"
            }
        )

    def _debut(self, ins) -> bool:
        self.ThisGame.InningsReplacement()
        self.OwnPlayer.ThrowCards_RandForNum(self.throw_num)
        return True

# --------------- 契约·紫色 -----------------