from copy import deepcopy
from random import randint, choice

from Card.SkillCard import SkillCard
from Card.UnitCard import UnitCard
from ExternalLibrary.ExternalLibrary import GetUID
from Game.Label import Is
from Mod.OriginalPackage import Effect


# --------------- 烈焰风暴 -----------------

class FlameStrike(SkillCard):
    def __init__(self):
        self.minDamage = 0
        self.maxDamage = 4
        super().__init__(
            name="烈焰风暴",
            desc="对全场所有单位造成{}-{}点伤害"
                 "".format(self.minDamage, self.maxDamage),
            level=3,
            label={
                "魔法"
            }
        )

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
                    card.GetDamage(
                        randint(self.minDamage, self.maxDamage),
                        self.Label
                    )
        return True


# --------------- 灵魂虚弱 -----------------

class BodyWeak(SkillCard):
    def __init__(self):
        self.combatAmend = 5
        super().__init__(
            name="灵魂虚弱",
            desc="对敌方某个单位施加灵魂虚弱效果\n"
                 "▼灵魂虚弱：最多减少目标单位{}点战斗力,目标单位等级越高作用效果越差"
                 "".format(self.combatAmend),
            level=2,
            label={
                "魔法"
            }
        )
        self.effect = Effect.BodyWeakEffect(self.combatAmend)

    def Debut(self, ins) -> bool:
        try:
            self.ThisGame.UIDCardDict[ins[0]].AddStatus(self.effect)
            return True
        except:
            return False


# --------------- 禁术：灵魂融合 -----------------

class SoulFusion(SkillCard):
    def __init__(self):
        self.per_label_to_combat = 1
        super().__init__(
            name="禁术：灵魂融合",
            desc="将某一行的所有单位融合成一个违背常理的怪物\n"
                 "◇禁术：这张牌是一张禁术牌\n"
                 "▼融合：将某一行的单位全部杀死，并融合成一个带有腐化的怪物，怪物将继承所有被杀死单位的基础战斗力和属性标签，但不会继承技能。并且在融合时，每有一种属性标签，怪物的基础战斗力+{}"
                 "".format(self.per_label_to_combat),
            level=4,
            label={
                "禁咒",
            }
        )

    def Debut(self, ins) -> bool:
        try:
            label = set()
            combat = 0
            li = abs(ins[0])
            tarPlayer = self.OwnPlayer if (ins[0] > 0) else self.OwnPlayer.OpPlayer

            for card in tarPlayer.Lines[li]:
                try:
                    if (card.Dead()):
                        label |= card.Label
                        combat += card.SelfCombat
                except:
                    pass

            label.add("腐化")
            combat += len(label) * self.per_label_to_combat
            monster = deepcopy(UnitCard(
                name="融合怪物",
                desc="这是一种违背世间常理的存在\n"
                     "◇腐化：这个怪物具有腐化因子\n"
                     "◇融合：这个怪物拥有诸多属性",
                combat=combat,
                level=4,
                label=label
            ))
            monster.UID = GetUID()
            self.ThisGame.AddCardToLine(tarPlayer, li - 1, monster)

            return True

        except:
            return False


# --------------- 战争补给 -----------------

class WarSupplies(SkillCard):
    def __init__(self):
        self.get_card_num = 2
        super().__init__(
            name="战争补给",
            desc="打出后从己方牌库中抽取{}张牌"
                 "".format(self.get_card_num),
            level=3,
            label={
                "计略"
            }
        )

    def Debut(self, ins) -> bool:
        self.OwnPlayer.GetCards(self.get_card_num)
        return True


# --------------- 神圣祝福 -----------------

class HolyBlessing(SkillCard):
    def __init__(self):
        self.max_add_combat = 4
        super().__init__(
            name="神圣祝福",
            desc="增加目标单位最多{}点基础战斗力，对等级越高的敌人影响越低\n"
                 "◇圣吟：对不死者和恶魔将造成伤害"
                 "".format(self.max_add_combat),
            level=2,
            label={
                "圣吟"
            }
        )

    def Debut(self, ins) -> bool:
        try:
            card = self.ThisGame.UIDCardDict[ins[0]]
            add = self.max_add_combat - card.Level + 1
            if (Is("恶魔", card) or Is("不死者", card)):
                card.GetDamage(add, self.Label)
            else:
                card.SelfCombat += add
            return True
        except:
            return False


# --------------- 吞日 -----------------

class NoSunStone(SkillCard):
    def __init__(self):
        super().__init__(
            name="吞日",
            desc="将太阳从世间抹除\n"
                 "◇禁术：这张牌是一张禁术牌\n"
                 "▼吞日：全局效果，再不会有白天出现，效果将无视场替",
            level=4,
            label={
                "禁咒"
            }
        )

    def Debut(self, ins) -> bool:
        self.ThisGame.AddCardToGlobal(self)
        return True

    def Round(self) -> bool:
        self.ThisGame.DayOrNight = False
        return True


# --------------- 雷击 -----------------

class LightningStrike(SkillCard):
    def __init__(self):
        self.max_dmg = 8
        self.min_dmg = 3
        super().__init__(
            name="雷击",
            desc="使用闪电对目标进行打击，造成{}~{}点伤害"
                 "".format(self.min_dmg, self.max_dmg),
            level=2,
            label={
                "魔法"
            }
        )

    def Debut(self, ins) -> bool:
        try:
            self.ThisGame.UIDCardDict[ins[0]].GetDamage(
                randint(self.min_dmg, self.max_dmg),
                self.Label
            )
            return True
        except:
            return False


# --------------- 终焉之战 -----------------

class TheFinalBattle(SkillCard):
    def __init__(self):
        self.get_card_num = 10
        super().__init__(
            name="终焉之战",
            desc="◇神术：这是一张神术牌\n"
                 "◇决战：该牌只能在第三场打出;\n"
                 "◇终焉：对场上所有的单位卡和全局效果卡做场替判定，重新随机日月，双方玩家弃掉所有手牌，随后各自抽取{}张新的手牌;"
                 "".format(self.get_card_num),
            level=5,
            label={
                "神术"
            }
        )

    def Debut(self, ins) -> bool:
        # 决战
        if (self.ThisGame.NumberOfInnings == 2):
            # 终焉
            self.ThisGame.InningsReplacement()
            self.ThisGame.RealDayOrNight = choice([True, False])
            self.OwnPlayer.ThrowCards(range(len(self.OwnPlayer.HandCards)))
            self.OwnPlayer.OpPlayer.ThrowCards(range(len(self.OwnPlayer.HandCards)))
            self.OwnPlayer.GetCards(self.get_card_num)
            self.OwnPlayer.OpPlayer.GetCards(self.get_card_num)
            return True
        else:
            return False
