from copy import deepcopy
from random import sample, choice, randint
import numpy as np
from Card.UnitCard import UnitCard
from ExternalLibrary.ExternalLibrary import NoSpell, ConcretizationCard
from ExternalLibrary.MsyEvent import GetDmg
from Game.Label import Has
from Mod.AncientGods import Skill

# --------------- 克拉肯 -----------------

class Kraken(UnitCard):
    def __init__(self):
        super().__init__(
            name="克拉肯",
            desc="在深不可测的海底，北海巨妖正在沉睡，它已经沉睡了数个世纪，并将继续安枕在巨大的海虫身上，直到有一天海虫的火焰将海底温暖，人和天使都将目睹它带着怒吼从海底升起，海面上的一切将毁于一旦\n"
                 "◇潮渊之境的怪兽：这家伙是个远古生物\n"
                 "◇触手：" # TODO(DOEMsy 2021.6.1) 记得先实现一个召唤物机制  
                 "".format(),
            combat=28,
            level=4,
            label={
                "远古"
            },
            canto={1},
        )

# --------------- 征服·天启四骑士 ---------------

class ConquerApocalypse(UnitCard):
    def __init__(self):
        super().__init__(
            name="征服",
            desc="◇天启四骑士：我看见羔羊揭开七印中第一印的时候，就听见四活物中的一个活物，声音如雷，说：“你来！”我就观看，见有一匹白马，骑在马上的拿着弓，并有冠冕赐给他。他便出来，胜了又要胜。\n"
                 "◇天启·征服：出场时，增加（敌方手牌数目+敌方场上战力和）的基础战斗力\n"
                 "◇天启·神羽：基础战斗力增加时，获得等量的护盾"
                 "".format(),
            combat=0,
            level=5,
            label={
                "天使"
            },
            canto={1},
        )

    def _addSelfCombat(self, num, effectLabel):
        self.SelfCombat += num
        self._addShield(num,{'特性','神术'})
        return num

    def _selftoLineOn(self):
        card_num = self.OwnPlayer.OpPlayer.HandCards.__len__()
        op_total_cmt = self.OwnPlayer.OpPlayer.TolCombat
        self._addSelfCombat(card_num+op_total_cmt,{'特性','神术'})
        return True

# --------------- 屠戮·天启四骑士 ---------------

class ExtirpateApocalypse(UnitCard):
    def __init__(self):
        self.card_num = 3
        super().__init__(
            name="屠戮",
            desc="◇天启四骑士：揭开第二印的时候，我听见第二个活物说：“你来！”就另有一匹马出来，是红的。有权柄给了那骑马的，可以从地上夺去太平，使人彼此相杀，又有一把大刀赐给他。\n"
                 "◇天启·屠戮：拥有{}次释放屠戮的机会\n"
                 "◇天启·神羽：不会受到任何的伤害和状态效果，但是不免疫死亡"
                 "".format(self.card_num),
            combat=0,
            level=5,
            label={
                "天使"
            },
            canto={2},
        )
        self.ComCard = {Skill.Extirpate():self.card_num}

    def _getDamage(self, num, effectLabel):
        return 0

    def _addStatus(self, status):
        return False

    def _combat_exis_effect(self, effect):
        return 0


# --------------- 饥荒·天启四骑士 ---------------

class FamineApocalypse(UnitCard):
    def __init__(self):
        self.throw_num = 2
        self.shield_value = 12
        super().__init__(
            name="饥荒",
            desc="◇天启四骑士：揭开第三印的时候，我听见第三个活物说：“你来！”我就观看，见有一匹黑马。骑在马上的手里拿着天平。我听见在四活物中似乎有声音说：“一钱银子买一升麦子，一钱银子买三升大麦，油和酒不可糟蹋。\n"
                 "◇天启·饥荒：出场时，强制对方随机弃掉{}张手牌，场替时强制对方弃掉所有手牌。\n"
                 "◇天启·神羽：拥有{}点护盾"
                 "".format(self.throw_num,self.shield_value),
            combat=3,
            level=5,
            label={
                "天使"
            },
            canto={2},
            shieldValue=self.shield_value,
        )

    def _selftoLineOn(self):
        self.OwnPlayer.OpPlayer.ThrowCards_RandForNum(self.throw_num)
        return True

    def _toNextTurn(self) -> bool:
        self.OwnPlayer.OpPlayer.ThrowCards_ALL()
        return True

# --------------- 瘟疫·天启四骑士 ---------------

class PlagueApocalypse(UnitCard):
    def __init__(self):
        super().__init__(
            name="瘟疫",
            desc="◇天启四骑士：揭开第四印的时候，我听见第四个活物说：“你来！”我就观看，见有一匹惨绿色马。骑在马上的，名字叫做死，阴府也随着他，有权柄赐给他们，可以用刀剑、饥荒、瘟疫野兽，杀害地上四分之一的人。”\n"
                 "◇天启·瘟疫：存在时，场上所有单位一旦受伤立即濒死\n"
                 "◇天启·神羽：不会受到任何的伤害和状态效果，但是不免疫死亡"
                 "".format(),
            combat=0,
            level=5,
            label={
                "天使"
            },
            canto={2},
        )
        self.Monitor_GetDmg = True
    def  _getDmgProcessing(self, event:GetDmg):
        UID = event.card.UID
        cureDmg = event.cureDmg
        # 受伤未死亡的单位立即濒死
        if (UID != self.UID and cureDmg>0):
            tagert = event.card
            tagert.SelfCombat = 0
        return True

    def _getDamage(self, num, effectLabel):
        return 0

    def _addStatus(self, status):
        return False

    def _combat_exis_effect(self, effect):
        return 0
