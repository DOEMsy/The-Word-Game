from copy import deepcopy
from random import randint, choice

import numpy as np

from Card.SkillCard import SkillCard
from Card.StatusEffect import StatusEffect
from Card.UnitCard import UnitCard
from ExternalLibrary.ExternalLibrary import GetUID, ConcretizationCard, GetRandCard
from Game.Label import Is
from Mod.OriginalPackage import Effect, Unit


# --------------- 爆裂魔法 -----------------

class Explosion(SkillCard):
    def __init__(self):
        self.minDamage = 0
        self.maxDamage = 16
        super().__init__(
            name="爆裂魔法",
            desc="某红魔大法师的招牌魔法，对敌方所有单位造成{}-{}点魔法伤害\n"
                 "Explosion~!"
                 "".format(self.minDamage, self.maxDamage),
            level=4,
            label={
                "魔法"
            }
        )

    def _debut(self, ins) -> bool:
        # game = self.ThisGame
        # for NO in range(2):
        #    player = game.Players[NO]
        #    for i in range(3):
        #        line = player.Lines[i]
        #        for j in range(len(line)):
        #            card = line[j]
        #            card.GetDamage(self.damage)
        for card in self.OwnPlayer.OpPlayer.UIDCardDict.values():
            card.GetDamage(
                randint(self.minDamage, self.maxDamage),
                self.Label
            )
        return True


# --------------- 灵魂虚弱 -----------------

class BodyWeak(SkillCard):
    def __init__(self):
        self.combatAmend = 9
        super().__init__(
            name="灵魂虚弱",
            desc="对敌方某个单位施加灵魂虚弱效果\n"
                 "◇灵魂虚弱：最多减少目标单位{}点战斗力,目标单位等级越高作用效果越差"
                 "".format(self.combatAmend),
            level=2,
            label={
                "魔法"
            }
        )
        self.effect = Effect.BodyWeakEffect(self.combatAmend)

    def _debut(self, ins) -> bool:
        try:
            self.ThisGame.UIDCardDict[ins[0]].AddStatus(self.effect)
            return True
        except:
            return False


# --------------- 禁术：灵魂融合 -----------------
# pop i tarLine throw_i
class SoulFusion(SkillCard):
    def __init__(self):
        self.per_label_to_combat = 1
        super().__init__(
            name="禁术：灵魂融合",
            desc="将某一行的所有单位融合成一个违背常理的怪物\n"
                 "◇禁术：这张牌是一张禁术牌，打出时必须指定弃一张手牌\n"
                 "◇融合：将某一行的单位全部杀死，并融合成一个带有腐化的怪物，怪物将继承所有被杀死单位的基础战斗力和属性标签，但不会继承技能。并且在融合时，每有一种属性标签，怪物的基础战斗力+{}"
                 "".format(self.per_label_to_combat),
            level=4,
            label={
                "禁咒",
            }
        )

    def _debut(self, ins) -> bool:
        if (  # 禁术
                self.OwnPlayer.HandCards[ins[1]].UID != self.UID and
                self.OwnPlayer.ThrowCards_withIlist([ins[1]])
        ):
            label = set()
            combat = 0
            tarPlayer = self.OwnPlayer if (ins[0] > 0) else self.OwnPlayer.OpPlayer
            li = abs(ins[0]) - 1
            for card in tarPlayer.Lines[li]:
                try:
                    if (card.Dead()):
                        label |= card.Label
                        combat += card.SelfCombat
                except:
                    pass

            label.add("腐化")
            combat += len(label) * self.per_label_to_combat
            monster = ConcretizationCard(UnitCard(
                name="融合怪物",
                desc="这是一种违背世间常理的存在\n"
                     "◇腐化：这个怪物具有腐化因子\n"
                     "◇融合：这个怪物拥有诸多属性",
                combat=combat,
                level=4,
                label=label
            ))
            self.ThisGame.AddCardToLine(tarPlayer, li, monster)
            return True
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

    def _debut(self, ins) -> bool:
        self.OwnPlayer.GetCards(self.get_card_num)
        return True


# --------------- 神圣祝福 -----------------

class HolyBlessing(SkillCard):
    def __init__(self):
        self.max_add_combat = 7
        super().__init__(
            name="神圣祝福",
            desc="增加目标单位最多{}点基础战斗力，对等级越高的敌人影响越低\n"
                 "◇圣吟：对不死者和恶魔将造成圣吟伤害"
                 "".format(self.max_add_combat),
            level=2,
            label={
                "圣吟"
            }
        )

    def _debut(self, ins) -> bool:
        card = self.ThisGame.UIDCardDict[ins[0]]
        add = self.max_add_combat - card.Level + 1
        if (Is("恶魔", card) or Is("不死者", card)):
            card.GetDamage(add, self.Label)
        else:
            # card.SelfCombat += add
            card.AddSelfCombat(add, self.Label)
        return True


# --------------- 吞日 -----------------
# pop i throw_i
class NoSunStone(SkillCard):
    def __init__(self):
        super().__init__(
            name="吞日",
            desc="将太阳从世间抹除\n"
                 "◇禁术：这张牌是一张禁术牌，打出时必须指定弃一张手牌\n"
                 "▼吞日：全局效果，再不会有白天出现，效果将无视场替",
            level=4,
            label={
                "禁咒"
            }
        )

    def _debut(self, ins) -> bool:
        if (  # 禁术
                self.OwnPlayer.HandCards[ins[0]].UID != self.UID and
                self.OwnPlayer.ThrowCards_withIlist([ins[0]])
        ):
            self.ThisGame.AddCardToGlobal(self)
            return True
        return False

    def _round(self) -> bool:
        self.ThisGame.DayOrNight = False
        return True

    def _toNextTurn(self) -> bool:
        return False



# --------------- 雷击 -----------------

class LightningStrike(SkillCard):
    def __init__(self):
        self.max_dmg = 8
        self.min_dmg = 4
        super().__init__(
            name="雷击",
            desc="使用闪电对目标进行打击，造成{}~{}点魔法伤害"
                 "".format(self.min_dmg, self.max_dmg),
            level=3,
            label={
                "魔法"
            }
        )

    def _debut(self, ins) -> bool:
        self.ThisGame.UIDCardDict[ins[0]].GetDamage(
            randint(self.min_dmg, self.max_dmg),
            self.Label
        )
        return True


# --------------- 终焉之战 -----------------

class TheFinalBattle(SkillCard):
    def __init__(self):
        self.get_card_num = 10
        super().__init__(
            name="终焉之战",
            desc="从这张牌洗入牌堆开始，命运就已经被扭曲了\n"
                 "◇神术：这是一张神术牌\n"
                 "◇决战：该牌只能在第三场打出;\n"
                 "◇终焉：对场上所有的单位卡和全局效果卡做场替判定，重新随机日月，双方玩家弃掉所有手牌，随后各自抽取{}张新的手牌;"
                 "".format(self.get_card_num),
            level=5,
            label={
                "神术"
            }
        )

    def _debut(self, ins) -> bool:
        # 决战
        if (self.ThisGame.NumberOfInnings == 2):
            # 终焉
            self.ThisGame.InningsReplacement()
            self.ThisGame.RealDayOrNight = choice([True, False])
            self.OwnPlayer.ThrowCards_ALL()
            self.OwnPlayer.OpPlayer.ThrowCards_ALL()
            self.OwnPlayer.GetCards(self.get_card_num)
            self.OwnPlayer.OpPlayer.GetCards(self.get_card_num)
            return True
        else:
            return False


# --------------- 魔法箭 -----------------

class MagicArrow(SkillCard):
    def __init__(self):
        self.dmg = 3
        self.get_card_prob = 0.5
        super().__init__(
            name="魔法箭",
            desc="使用魔法箭对目标进行打击，造成{}点魔法伤害\n"
                 "◇廉价：出牌时有{}%的概率抽取一张牌"
                 "".format(self.dmg, self.get_card_prob * 100),
            level=1,
            label={
                "魔法"
            }
        )

    def _debut(self, ins) -> bool:
        try:
            self.ThisGame.UIDCardDict[ins[0]].GetDamage(
                self.dmg,
                self.Label
            )
            if (choice([True, False])): self.OwnPlayer.GetCards(1)
            return True
        except:
            return False


# --------------- 魔法飞弹 -----------------

class MagicMissile(SkillCard):
    def __init__(self):
        self.target_num = 5
        self.max_dmg = 2
        self.min_dmg = 1
        super().__init__(
            name="魔法飞弹",
            desc="发射出{}个魔法飞弹对随机敌人进行打击，每个飞弹造成{}~{}点魔法伤害"
                 "".format(self.target_num, self.min_dmg, self.max_dmg),
            level=2,
            label={
                "魔法"
            }
        )

    def _debut(self, ins) -> bool:
        for _ in range(self.target_num):
            try:
                target = choice(list(self.OwnPlayer.OpPlayer.UIDCardDict.values()))
                target.GetDamage(
                    randint(self.min_dmg, self.max_dmg),
                    self.Label
                )
            except:
                # 有可能选不到目标
                pass

        return True


# --------------- 立即死亡 -----------------
# pop i tarUID throw_i
class DieImmediately(SkillCard):
    def __init__(self):
        self.max_level_can = 4
        super().__init__(
            name="格列姆的凝视",
            desc="雾行者高层持有的至上宝具，拥有夺取性命的能力，但使用需要付出同等的代价\n"
                 "◇禁术：这张牌是一张禁术牌，打出时必须指定弃一张手牌\n"
                 "◇即死：指定一张等级最高为Lv{}的卡牌立即死亡，对于高于等级或免疫死亡的卡牌将无效——枯萎吧，凋零吧，扭断吧，生命的曲线"
                 "".format(self.max_level_can),
            level=4,
            label={
                "禁咒"
            }
        )

    def _debut(self, ins) -> bool:
        if (  # 禁术
                self.OwnPlayer.HandCards[ins[1]].UID != self.UID and
                self.OwnPlayer.ThrowCards_withIlist([ins[1]])
        ):  # 立即死亡
            target = self.ThisGame.UIDCardDict[ins[0]]
            if (target.Level <= self.max_level_can):
                target.Dead()
            return True
        return False


# --------------- 硬币 -----------------

class Coin(SkillCard):
    def __init__(self):
        self.max_dmg = 4
        self.min_dmg = 2
        self.dmg_upp = 3
        super().__init__(
            name="硬币",
            desc="一枚镍制的硬币，不知道为啥你可以把它射出去\n"
                 "◇简易电磁炮：将硬币向一个目标发射出去照成{}~{}点物理伤害\n"
                 "◇精密仪器杀手：对于机械单位造成{}倍伤害"
                 "".format(self.min_dmg, self.max_dmg, self.dmg_upp),
            level=2,
            label={
                "物理"
            }
        )

    def _debut(self, ins) -> bool:
        dmg = randint(self.min_dmg, self.max_dmg)
        target = self.ThisGame.UIDCardDict[ins[0]]
        if (Is("机械", target)):    dmg *= self.dmg_upp
        self.ThisGame.UIDCardDict[ins[0]].GetDamage(
            dmg,
            self.Label
        )
        return True


# --------------- 异端审判 -----------------

class ReligiousTrial(SkillCard):
    def __init__(self):
        self.dmg = 4
        self.dmg_up = 5
        self.dmg_upp = 2
        super().__init__(
            name="异端审判",
            desc="指定目标进行审判，造成{}点圣吟伤害\n"
                 "◇亚人杀手：对于亚人额外造成{}点圣吟伤害——人类是至上的种族，一切非人种族必须灭绝\n"
                 "◇圣吟：对于不死者和恶魔造成{}倍伤害"
                 "".format(self.dmg, self.dmg_up, self.dmg_upp),
            level=3,
            label={
                "圣吟"
            }
        )

    def _debut(self, ins) -> bool:
        dmg = self.dmg
        target = self.ThisGame.UIDCardDict[ins[0]]
        if (Is("亚人", target)):    dmg += self.dmg_up
        if (Is("不死者", target) or Is("恶魔",target)):     dmg *= self.dmg_upp
        self.ThisGame.UIDCardDict[ins[0]].GetDamage(
            dmg,
            self.Label
        )
        return True


# --------------- 混乱因子 -----------------

class ChaosFactor(SkillCard):
    def __init__(self):
        self.target_num_max = 50
        self.target_num_min = 20
        self.dmg = 1
        self.get_card_num = 3
        super().__init__(
            name="混乱因子",
            desc="释放{}~{}个混乱因子，随机攻击场上任意一个单位，每个混乱因子可造成{}点腐化伤害\n"
                 "◇腐化：这张牌具有腐化效果，腐化的伤害会治疗腐化生物\n"
                 "◇混沌：出牌后双方玩家可同时从对方的牌库中抽取{}张牌"
                 "".format(self.target_num_min, self.target_num_max, self.dmg, self.get_card_num),
            level=4,
            label={
                "腐化"
            }
        )

    def _debut(self, ins) -> bool:

        for _ in range(randint(self.target_num_min, self.target_num_max)):
            try:
                # 混乱因子
                target = choice(list(self.ThisGame.UIDCardDict.values()))
                if (Is("腐化", target)):
                    target.AddSelfCombat(
                        self.dmg,
                        self.Label
                    )
                else:
                    target.GetDamage(
                        self.dmg,
                        self.Label
                    )
            except:
                # 有可能选不到目标
                pass
        # 混沌
        self.ThisGame.Players[0].GetCards_FromOp(self.get_card_num)
        self.ThisGame.Players[1].GetCards_FromOp(self.get_card_num)

        return True


# --------------- 卫国战争 -----------------

class GreatPatrioticWar(SkillCard):
    def __init__(self):
        super().__init__(
            name="卫国战争",
            desc="弗朗坎特姆帝国军队有着优秀的调度能力，可以迅速掌控战场\n"
                 "◇计略：这一张计略牌\n"
                 "◇增援：在己方场上随机召唤出与2^(敌方lv4及以上单位数量)的帝国军队——在天灾面前，我们毫不退缩\n"
                 "◇召收：本卡每召唤三个单位，可获得一张战争补给卡牌",
            level=5,
            label={
                "计略"
            }
        )
        self.summon = [Unit.ImperialKnight(), Unit.ImperialShotter(), Unit.ImperialShotter()]
        self.give = WarSupplies()

    def _debut(self, ins) -> bool:

        num = 0
        for cd in self.OwnPlayer.OpPlayer.UIDCardDict.values():
            if (cd.Level >= 4):
                num += 1

        num = 2**num

        for _ in range(num):
            card = ConcretizationCard(choice(self.summon))
            self.ThisGame.AddCardToLine(self.OwnPlayer, randint(0, 2), card)

        # 召收
        for _ in range(num // 3):
            card = ConcretizationCard(self.give)
            card.Pump(self.OwnPlayer)

        return True


# --------------- 生锈的斧头 -----------------

class RustyAxe(SkillCard):
    def __init__(self):
        self.dmg = 4
        self.tetanus = 2
        super().__init__(
            name="生锈的斧头",
            desc="不知道从哪里捡来的，有一定的年头了\n"
                 "◇飞斧：把这东西飞出去打中可以造成{}点物理伤害\n"
                 "◇破伤风：被这把斧子击中的普通生物获得破伤风buff，魔法效果。\n"
                 "◇觉醒：用这把斧子击杀敌人会获得了不得的东西？"
                 "".format(self.dmg),
            level=3,
            label={
                "计略"
            }
        )
        self.effect = Effect.SingleDebuffingBuffTemplate(
            name="破伤风",
            desc="该单位中了破伤风，战斗力-{}".format(self.tetanus),
            combatAmend=self.tetanus,
            label={"魔法"}
        )
        self.summon = Ragnarok()

    def _debut(self, ins) -> bool:
        target = self.ThisGame.UIDCardDict[ins[0]]
        hasdead = (target.GetDamage(self.dmg, {"物理"}) == 2)
        if (Is("普通生物", target)):
            target.AddStatus(self.effect)
        if (hasdead):
            card = ConcretizationCard(self.summon)
            card.Pump(self.OwnPlayer)
        return True


# 只能通过斧头获得
class Ragnarok(SkillCard):
    def __init__(self):
        self.dmg = 30
        super().__init__(
            name="诸神黄昏",
            desc="这把锈斧染了鲜血后，焕然一新\n"
                 "◇开天：把这东西飞出去打中可以对指定行的所有单位造成{}点神术伤害".format(self.dmg),
            level=4,
            label={
                "神术"
            }
        )

    # 123 己方行 -1-2-3敌方行
    def _debut(self, ins) -> bool:
        tarline = None
        if (3 >= ins[0] > 0):
            tarline = self.OwnPlayer.Lines[ins[0] - 1]
        # 打到对面牌区
        elif (-3 <= ins[0] < 0):
            tarline = self.OwnPlayer.OpPlayer.Lines[-ins[0]-1]
        else:
            return False
        for card in tarline:
            card.GetDamage(self.dmg, {"神术"})
        return True


# --------------- 烈焰风暴 -----------------

class FireBoom(SkillCard):
    def __init__(self):
        self.dmg = 3
        super().__init__(
            name="烈焰风暴",
            desc="对目标行所有单位造成{}点魔法伤害"
                 "".format(self.dmg),
            level=2,
            label={
                "魔法"
            }
        )

    # 123 己方行 -1-2-3敌方行
    def _debut(self, ins) -> bool:
        tarline = None
        if (3 >= ins[0] > 0):
            tarline = self.OwnPlayer.Lines[ins[0] - 1]
        # 打到对面牌区
        elif (-3 <= ins[0] < 0):
            tarline = self.OwnPlayer.OpPlayer.Lines[-ins[0]-1]
        else:
            return False
        for card in tarline:
            card.GetDamage(self.dmg, {"魔法"})
        return True


# --------------- 雄心 -----------------

class LionHeart(SkillCard):
    def __init__(self):
        self.combat_add = 3
        super().__init__(
            name="雄心",
            desc="对目标行所有单位施加雄心效果，战斗力+{}"
                 "".format(self.combat_add),
            level=2,
            label={
                "魔法"
            }
        )
        self.effect = Effect.SingleBuffingBuffTemplate(
            name="雄心",
            desc="单位拥有雄心效果，战斗力+{}".format(self.combat_add),
            combatAmend=self.combat_add,
            label={"魔法"}
        )

    # 123 己方行 -1-2-3敌方行
    def _debut(self, ins) -> bool:
        tarline = None
        if (3 >= ins[0] > 0):
            tarline = self.OwnPlayer.Lines[ins[0] - 1]
        # 打到对面牌区
        elif (-3 <= ins[0] < 0):
            tarline = self.OwnPlayer.OpPlayer.Lines[-ins[0]-1]
        else:
            return False
        for card in tarline:
            card.AddStatus(self.effect)
        return True


# --------------- 压迫 -----------------

class Oppression(SkillCard):
    def __init__(self):
        self.combat_dec = 3
        super().__init__(
            name="压迫",
            desc="对目标行所有单位施加压迫效果，战斗力-{}"
                 "".format(self.combat_dec),
            level=2,
            label={
                "魔法"
            }
        )
        self.effect = Effect.SingleDebuffingBuffTemplate(
            name="压迫",
            desc="单位拥有的勇气减少了，战斗力-{}".format(self.combat_dec),
            combatAmend=self.combat_dec,
            label={"魔法"}
        )

    # 123 己方行 -1-2-3敌方行
    def _debut(self, ins) -> bool:
        tarline = None
        if (3 >= ins[0] > 0):
            tarline = self.OwnPlayer.Lines[ins[0] - 1]
        # 打到对面牌区
        elif (-3 <= ins[0] < 0):
            tarline = self.OwnPlayer.OpPlayer.Lines[-ins[0]-1]
        else:
            return False
        for card in tarline:
            card.AddStatus(self.effect)
        return True


# --------------- 魔力爆破 -----------------

class MagicBlasting(SkillCard):
    def __init__(self):
        self.every_effect_dmg = 5
        super().__init__(
            name="魔力爆破",
            desc="通过连锁反应引爆目标身上的所有的魔法效果，每有一种效果造成{}点伤害"
                 "".format(self.every_effect_dmg),
            level=3,
            label={
                "魔法"
            }
        )

    def _debut(self, ins) -> bool:
        ct = 0
        pops = []
        target = self.ThisGame.UIDCardDict[ins[0]]
        for uid, effect in target.Status.items():
            if (Is("魔法", effect)):
                ct += 1
                pops.append(uid)

        for uid in pops:
            target.RemStatus(uid)

        self.ThisGame.UIDCardDict[ins[0]].GetDamage(
            ct * self.every_effect_dmg,
            self.Label
        )
        return True

# --------------- 无限 -----------------

class InfiniteSacrifice(SkillCard):
    def __init__(self):
        super().__init__(
            name="无限",
            desc="仅在神话中存在的宝具，无限\n"
                 "◇无主动：此牌无法被打出\n"
                 "◇无限：当持牌作为弃牌时，将获得一张相同的牌".format(),
            level=5,
            label={
                "神术","宝具"
            }
        )

    def _debut(self, ins) -> bool:
        return False

    def _aban(self) -> bool:
        card = ConcretizationCard(self)
        card.Pump(self.OwnPlayer)
        return True


# --------------- 幸运币 -----------------

class LuckyCoin(SkillCard):
    def __init__(self):
        self.add_combat = 5
        self.dmg_combat = 2
        self.ct = 0
        super().__init__(
            name="幸运币",
            desc="掷出一枚幸运币\n"
                 "◇字面：指定的目标单位增加{}点基础战斗力\n"
                 "◇花面：指定的目标单位受到{}点魔法伤害，再获得一枚幸运币"
                 "".format(self.add_combat,self.dmg_combat),
            level=2,
            label={
                "魔法"
            }
        )

    def _debut(self, ins) -> bool:
        if(choice([True,False])):
            self.ThisGame.UIDCardDict[ins[0]].AddSelfCombat(self.add_combat,self.Label)
        else:
            self.ThisGame.UIDCardDict[ins[0]].GetDamage(self.dmg_combat,self.Label)

            card = ConcretizationCard(self)
            card.ct += 1
            if(card.ct == 3):
                card = ConcretizationCard(GetRandCard({"Level":5},1)[0])

            card.Pump(self.OwnPlayer)
        return True


# --------------- 治疗术 -----------------

class Healing(SkillCard):
    def __init__(self):
        self.add_combat = 3
        self.add_combat_2 = 1
        self.ct = 1
        super().__init__(
            name="治疗术",
            desc="指定一个目标增加{}点基础战斗力\n"
                 "◇余波：目标同行内的其他单位提升{}点战斗力"
                 "".format(self.add_combat,self.add_combat_2),
            level=3,
            label={
                "魔法"
            }
        )

    def _debut(self, ins) -> bool:
        uid = ins[0]
        li = self.ThisGame.UIDCardDict[uid].Location
        self.ThisGame.UIDCardDict[uid].AddSelfCombat(self.add_combat,self.Label)
        for card in self.ThisGame.UIDCardDict[uid].OwnPlayer.Lines[li]:
            if(card.UID != uid):
                card.AddSelfCombat(self.add_combat_2,self.Label)
        return True

# --------------- 虚数粒子飞弹 -----------------

class ImaginaryParticleMissile(SkillCard):
    def __init__(self):
        self.target_num = 3
        self.max_dmg = 4
        self.min_dmg = 2
        super().__init__(
            name="虚数粒子飞弹",
            desc="发射出{}个虚数粒子对随机敌人进行打击，每个飞弹造成{}~{}点物理伤害"
                 "".format(self.target_num, self.min_dmg, self.max_dmg),
            level=2,
            label={
                "机械"
            }
        )

    def _debut(self, ins) -> bool:
        for _ in range(self.target_num):
            try:
                target = choice(list(self.OwnPlayer.OpPlayer.UIDCardDict.values()))
                target.GetDamage(
                    randint(self.min_dmg, self.max_dmg),
                    {"物理"}
                )
            except:
                # 有可能选不到目标
                pass

        return True

# --------------- 纳米断层保护 -----------------

class NanoTomographyProtection(SkillCard):
    def __init__(self):
        self.shield_get = 4
        self.combat_up = 5
        self.shield_cup = 2
        super().__init__(
            name="纳米断层保护",
            desc="选定一个目标，用微小的辅助计算机将其包裹起来形成护盾，增加{}点护盾值\n"
                 "◇辅助运算：目标为机械单位时，施加运算加速效果，增加其{}点战斗力\n"
                 "◇强化供能：目标为Lv4及以上的机械单位时，护盾值提升{}倍"
                 "".format(self.shield_get,self.combat_up,self.shield_cup),
            level=3,
            label={
                "机械"
            }
        )
        self.effect = Effect.SingleBuffingBuffTemplate(
            name="运算加速",
            desc="这个单位提升了运算能力，战斗力增加{}".format(self.combat_up),
            combatAmend=self.combat_up,
            label=self.Label
        )

    def _debut(self, ins) -> bool:
        target = self.ThisGame.UIDCardDict[ins[0]]
        shield = self.shield_get
        if(Is("机械",target)):
            target.AddStatus(self.effect)
            if(target.Level>=4):
                shield *= self.shield_cup
        target.AddShield(shield,self.Label)
        return True

# --------------- 魔法护盾 -----------------

class MagicShield(SkillCard):
    def __init__(self):
        self.shield_get = 4
        super().__init__(
            name="魔法护盾",
            desc="选定一个目标，增加{}点护盾值"
                 "".format(self.shield_get),
            level=2,
            label={
                "魔法"
            }
        )

    def _debut(self, ins) -> bool:
        target = self.ThisGame.UIDCardDict[ins[0]]
        shield = self.shield_get
        target.AddShield(shield,self.Label)
        return True

# --------------- 神圣庇护 -----------------

class DivineRefuge(SkillCard):
    def __init__(self):
        self.shield_get = 3
        self.combat_up = 2
        super().__init__(
            name="神圣庇护",
            desc="选定一个目标，增加{}点护盾值和{}点基础战斗力\n"
                 "◇圣吟：对不死者和恶魔将造成圣吟伤害"
                 "".format(self.shield_get,self.combat_up),
            level=2,
            label={
                "魔法"
            }
        )

    def _debut(self, ins) -> bool:
        target = self.ThisGame.UIDCardDict[ins[0]]
        if(Is("不死者",target) or Is("恶魔",target)):
            target.GetDamage(self.shield_get+self.combat_up,self.Label)
        else:
            target.AddShield(self.shield_get,self.Label)
            target.AddSelfCombat(self.combat_up,self.Label)
        return True

# --------------- 谜团 只能通过弗兰德斯获取 -----------------

class Mystery(SkillCard):
    def __init__(self):
        super().__init__(
            name="谜团",
            desc="没有人知道这是什么\n"
                 "◇神术：这是一张神术牌，具有改变世间常理的力量",
            level=5,
            label={
                "神术"
            }
        )

    def _debut(self, ins) -> bool:

        x = randint(1,10)
        if(x==1): # 全场随机受伤
            for card in self.ThisGame.UIDCardDict.values():
                card.GetDamage(randint(0,1)*randint(1,10),self.Label)
        elif(x==2): # 己方随机受伤
            for card in self.OwnPlayer.UIDCardDict.values():
                card.GetDamage(randint(0,1)*randint(1,10),self.Label)
        elif(x==3): # 敌方随机受伤
            for card in self.OwnPlayer.OpPlayer.UIDCardDict.values():
                card.GetDamage(randint(0,1)*randint(1,10),self.Label)
        elif(x==4): # 全场随机加护盾
            for card in self.ThisGame.UIDCardDict.values():
                card.AddShield(randint(0,1)*randint(1,10),self.Label)
        elif(x==5): # 己方随机加护盾
            for card in self.OwnPlayer.UIDCardDict.values():
                card.AddShield(randint(0,1)*randint(1,10),self.Label)
        elif(x==6): # 敌方随机加护盾
            for card in self.OwnPlayer.OpPlayer.UIDCardDict.values():
                card.AddShield(randint(0,1)*randint(1,10),self.Label)
        elif(x==7): # 随机方抽牌
            self.ThisGame.Players[randint(0,1)].GetCards(1)
        elif(x==8): # 随机方弃牌
            self.ThisGame.Players[randint(0, 1)].ThrowCards_RandForNum(1)
        elif(x==9): # 随机牌死亡
            for card in self.ThisGame.UIDCardDict.values():
                if(randint(0,5)==0):
                    card.Dead()
        elif(x==10): # 什么也没有发生
            pass

        return True

# --------------- 灵魂剥夺 -----------------

class BodyDeprivation(SkillCard):
    def __init__(self):
        self.combatAmend = 999999
        super().__init__(
            name="灵魂剥夺",
            desc="将敌人的灵魂直接击碎，使其失去作战能力。\n"
                 "".format(self.combatAmend),
            level=4,
            label={
                "魔法"
            }
        )
        self.effect = Effect.SingleDebuffingBuffTemplate(
            name="灵魂剥夺",
            desc="这个单位的失去了灵魂，没有作战能力",
            combatAmend=self.combatAmend,
            label=self.Label
        )

    def _debut(self, ins) -> bool:
        try:
            self.ThisGame.UIDCardDict[ins[0]].AddStatus(self.effect)
            return True
        except:
            return False


