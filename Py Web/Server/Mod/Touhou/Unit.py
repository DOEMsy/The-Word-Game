from copy import deepcopy
from random import sample, choice, randint
import numpy as np
from Card.UnitCard import UnitCard
from ExternalLibrary.ExternalLibrary import NoSpell, ConcretizationCard


# --------------- 博丽灵梦 -----------------

class HakureiReimu(UnitCard):
    def __init__(self):
        self.max_num_attack = 3
        self.attack_dmg = 1
        self.combat_add = 2
        super().__init__(
            name="博丽灵梦",
            desc="贪财的红白巫女，好像是某个作品系列的主角？\n"
                 "◇追踪符札：出牌时，发射{}个弹幕，每个弹幕可对敌方随机一个单位造成{}点魔法伤害\n"
                 "◇阴阳玉：砸人的效果出奇，打出时使得自身基础战斗力+{}"
                 "".format(self.max_num_attack, self.attack_dmg, self.combat_add),
            combat=5,
            level=3,
            label={
                "人类",
            },
            canto={2},
        )

    def _debut(self, ins) -> bool:
        # 追踪符札
        for _ in range(self.max_num_attack):
            try:
                target = choice(list(self.OwnPlayer.OpPlayer.UIDCardDict.values()))
                target.GetDamage(self.attack_dmg, {"魔法"})
            except:
                # 有可能选不到目标
                pass
        # 阴阳玉
        # self.SelfCombat += self.combat_add
        self.AddSelfCombat(self.combat_add,{"物理"})

        return True


# --------------- 多多良小伞 -----------------

class TataraKogasa(UnitCard):
    def __init__(self):
        self.scary_probability = 0.01
        super().__init__(
            name="多多良小伞",
            desc="被遗忘了的唐伞变化而成的付丧神\n"
                 "◇惊吓：有{}%的几率惊吓到场上随机卡牌，将其直接吓跑（离开战场，判定为死亡）"
                 "".format(self.scary_probability * 100),
            combat=3,
            level=3,
            label={
                "妖精"
            },
            canto={1},
        )

    def _debut(self, ins) -> bool:
        for target in self.ThisGame.UIDCardDict.values():
            try:
                if (np.random.choice([
                    True, False
                ], p=np.array([
                    self.scary_probability,
                    1 - self.scary_probability
                ]).ravel())):
                    target.Dead()
            except:
                pass
        return True


# --------------- 多多良假伞 -----------------

class TataraKogasaFake(UnitCard):
    def __init__(self):
        self.get_card_num = 1
        super().__init__(
            name="多多良假伞",
            desc="被遗忘了的☣☂变化而成的付丧神\n"
                 "◇惊吓：有0%的几率惊吓到场上随机卡牌，将其直接吓跑（离开战场，判定为死亡）\n"
                 "◇替身：这张牌打出后会变成某人形，并且玩家将抽取{}张新的手牌"
                 "".format(self.get_card_num),
            combat=3,
            level=3,
            label={
                "妖精"
            },
            canto={1},
        )

    def _debut(self, ins) -> bool:
        # 替身
        self.Name = "某人形"
        self.Desc = "◇机械：某种人形作战兵器，具有机械属性\n" \
                    "◇伪装：和人类长的一模一样，具有人类属性"
        self.SelfCombat = 4
        self.Level = 3
        self.Label = {
            "人类", "机械"
        }
        self.OwnPlayer.GetCards(self.get_card_num)
        return True


# --------------- 雾雨魔理沙 -----------------

class KirisameMarisa(UnitCard):
    def __init__(self):
        self.get_card_num = 1
        self.boom_max_dmg = 4
        self.boom_min_dmg = 2
        super().__init__(
            name="雾雨魔理沙",
            desc="性格恶劣有严重收集癖的魔法使，好像是某个作品系列的主角DA☆ZE\n"
                 "◇魔法道具：不知道从哪里掏出来的一枚炸弹，可对指定目标造成{}~{}点魔法伤害\n"
                 "◇暂时借走：打出时，将抽取{}张卡从对方牌堆中"
                 "".format(self.boom_min_dmg, self.boom_max_dmg, self.get_card_num),
            combat=5,
            level=3,
            label={
                "人类"
            },
            canto={2},
        )

    def _debut(self, ins) -> bool:
        # 魔法道具,可以选择不使用
        if (ins[1] != NoSpell):
            target = self.ThisGame.UIDCardDict[ins[1]]
            target.GetDamage(randint(self.boom_min_dmg, self.boom_max_dmg), {"魔法"})
        # 暂时借走
        self.OwnPlayer.GetCards_FromOp(self.get_card_num)
        return True


# --------------- 魂魄妖梦 -----------------

class KonpakuYoumu(UnitCard):
    def __init__(self):
        self.combat_add = 3
        super().__init__(
            name="魂魄妖梦",
            desc="脑子有些缺根筋的园艺师，同时也是一个剑术高手\n"
                 "◇半人半灵：人类和幽灵的混血，同时具有两种属性\n"
                 "◇二刀流：同时使用楼观剑和白楼剑，出牌时基础战斗力+{}"
                 "".format(self.combat_add),
            combat=4,
            level=3,
            label={
                "人类", "幽灵"
            },
            canto={1},
        )

    def _debut(self, ins) -> bool:
        # self.SelfCombat += self.combat_add
        self.AddSelfCombat(self.combat_add,{"特性"})
        return True


# --------------- 琪露诺 -----------------

class Cirno(UnitCard):
    def __init__(self):
        self.frog_num = 2
        super().__init__(
            name="琪露诺",
            desc="雾之湖的大贤者\n"
                 "◇结冰的修行：打出后向玩家手牌中塞入{}张冻青蛙牌"
                 "".format(self.frog_num),
            combat=4,
            level=3,
            label={
                "妖精"
            },
            canto={1},
        )
        self.summon = UnitCard(
            name="冻青蛙",
            desc="一点作用没有",
            combat=0,
            level=1,
            label={
                "动物"
            }
        )

    def _debut(self, ins) -> bool:
        for _ in range(self.frog_num):
            card = ConcretizationCard(self.summon)
            card.Pump(self.OwnPlayer)
        return True
