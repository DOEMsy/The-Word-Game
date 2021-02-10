from copy import deepcopy
from random import choice, randint

from Card.StatusEffect import StatusEffect
from Card.UnitCard import UnitCard
from ExternalLibrary.ExternalLibrary import GetUID, NoSpell
from Game.Label import Has
from Mod.OriginalPackage import Effect


# --------------- 狼 -----------------

class Wolf(UnitCard):
    def __init__(self):
        super().__init__(
            name="狼",
            desc="森林中常见的野生动物",
            combat=2,
            level=1,
            label={
                "动物",
            }
        )


# --------------- 帝国士兵 -----------------

class ImperialSoldier(UnitCard):
    def __init__(self):
        super().__init__(
            name="帝国老兵",
            desc="一名普普通通的士兵，本本分分的谋生",
            combat=3,
            level=1,
            label={
                "人类", "帝国",
            }
        )


# --------------- 哥布林 -----------------

class Goblin(UnitCard):
    def __init__(self):
        super().__init__(
            name="哥布林",
            desc="小型的野生哥布林，是一种常见的魔物",
            combat=2,
            level=1,
            label={
                "亚人",
            }
        )


# --------------- 食尸鬼 -----------------

class Ghoul(UnitCard):
    def __init__(self):
        self.skill_carrion_increased_combat = 1
        super().__init__(
            name="食尸鬼",
            desc="腐臭的尸体和骸骨中诞生的生物，靠吞噬尸体为生；\n"
                 "◇食尸：战场上每有一张牌死亡，自身基础战斗力+{}"
                 "".format(self.skill_carrion_increased_combat),
            combat=3,
            level=1,
            label={
                "亡骸",
            }
        )

    def Debut(self, ins):
        # 注册触发器
        self.ThisGame.eventMonitoring.BundledDeathTrigger(self)
        return True

    def Dead(self) -> bool:
        # 死亡时注销触发器
        self.ThisGame.eventMonitoring.UnBundledDeathTrigger(self)
        self.ThisGame.eventMonitoring.Occurrence({
            "type": "Death",
            "para": [self.UID, self.OwnNO]
        })
        return True

    def DeathProcessing(self, event):
        # 检测到别人死亡时战斗力增加
        UID = event['para'][0]
        if (UID != self.UID):
            self.SelfCombat += self.skill_carrion_increased_combat

    def ToNextTurn(self):
        # 场替时注销触发器
        self.ThisGame.eventMonitoring.UnBundledDeathTrigger(self)


# --------------- 帝国骑士 -----------------

class ImperialKnight(UnitCard):
    def __init__(self):
        super().__init__(
            name="帝国骑士",
            desc="帝国强大的地面部队，擅长快速作战；\n◇冲锋：打出在第一行时，基础战斗力+1",
            combat=4,
            level=1,
            label={
                "人类", "帝国"
            }
        )

    def Debut(self, ins):
        # 冲锋
        if (ins[0] == 1):
            self.SelfCombat += 1
        return True


# --------------- 变形怪 -----------------

class Doppler(UnitCard):
    def __init__(self):
        super().__init__(
            name="变形怪",
            desc="常人则很少有机会见到变形怪的真身，尤其是活着的变形怪，因为他们拥有高超的拟态能力。\n"
                 "◇变身：可以将数值和属性拟态成目标卡牌（战场上任意一张牌）的样子，但不具有其技能",
            combat=0,
            level=2,
            label={
                "高等生物",
            }
        )

    # to = ins = [local,target_UID]
    def Debut(self, ins) -> bool:
        try:
            if(ins[1]!=NoSpell):
                card = self.ThisGame.UIDCardDict[ins[1]]
                self.Name = card.Name + "（变形怪）"
                self.SelfCombat = card.SelfCombat
                self.Label = deepcopy(card.Label)
                self.Level = card.Level
            return True
        except:
            return False


# --------------- 巨型食尸鬼 -----------------

class GiantGhoul(UnitCard):
    def __init__(self):
        self.skill_carrion_increased_combat = 2
        super().__init__(
            name="巨型食尸鬼",
            desc="食尸鬼的亚种，体型是食尸鬼的3倍大；\n"
                 "◇食尸：战场上每有一张牌死亡，自身基础战斗力+{}"
                 "".format(self.skill_carrion_increased_combat),
            combat=5,
            level=2,
            label={
                "亡骸",
            }
        )

    def Debut(self, ins):
        # 注册触发器
        self.ThisGame.eventMonitoring.BundledDeathTrigger(self)
        return True

    def Dead(self) -> bool:
        # 死亡时注销触发器
        self.ThisGame.eventMonitoring.UnBundledDeathTrigger(self)
        self.ThisGame.eventMonitoring.Occurrence({
            "type": "Death",
            "para": [self.UID, self.OwnNO]
        })
        return True

    def DeathProcessing(self, event):
        # 检测到别人死亡时战斗力增加
        UID = event['para'][0]
        if (UID != self.UID):
            self.SelfCombat += self.skill_carrion_increased_combat

    def ToNextTurn(self):
        # 场替时注销触发器
        self.ThisGame.eventMonitoring.UnBundledDeathTrigger(self)


# --------------- 独眼食尸鬼 -----------------

class OneEyedGhoul(UnitCard):
    def __init__(self):
        self.skill_carrion_increased_combat = 4
        super().__init__(
            name="独眼食尸鬼",
            desc="食尸鬼的亚种，面部只有一只眼睛，体型较小，但成长迅速；\n"
                 "◇食尸：战场上每有一张牌死亡，自身基础战斗力+{}"
                 "".format(self.skill_carrion_increased_combat),
            combat=2,
            level=2,
            label={
                "亡骸",
            }
        )

    def Debut(self, ins):
        # 注册触发器
        self.ThisGame.eventMonitoring.BundledDeathTrigger(self)
        return True

    def Dead(self) -> bool:
        # 死亡时注销触发器
        self.ThisGame.eventMonitoring.UnBundledDeathTrigger(self)
        self.ThisGame.eventMonitoring.Occurrence({
            "type": "Death",
            "para": [self.UID, self.OwnNO]
        })
        return True

    def DeathProcessing(self, event):
        # 检测到别人死亡时战斗力增加
        UID = event['para'][0]
        if (UID != self.UID):
            self.SelfCombat += self.skill_carrion_increased_combat

    def ToNextTurn(self):
        # 场替时注销触发器
        self.ThisGame.eventMonitoring.UnBundledDeathTrigger(self)


# --------------- 小布丁 -----------------

class LittlePudding(UnitCard):
    def __init__(self):
        self.skill_carrion_increased_combat = 3
        super().__init__(
            name="小布丁",
            desc="特殊巨型食尸鬼，像宠物一样被四学士圈养，拥有较低的知性\n"
                 "◇食尸：战场上每有一张牌死亡，自身基础战斗力+{}\n"
                 "◇半机械：该生物经历过生化改造，拥有机械属性\n"
                 "◇四学士：这个家伙是四学士的成员"
                 "".format(self.skill_carrion_increased_combat),
            combat=6,
            level=3,
            label={
                "亡骸", "机械", "四学士",
            }
        )

    def Debut(self, ins):
        # 注册触发器
        self.ThisGame.eventMonitoring.BundledDeathTrigger(self)
        return True

    def Dead(self) -> bool:
        # 死亡时注销触发器
        self.ThisGame.eventMonitoring.UnBundledDeathTrigger(self)
        self.ThisGame.eventMonitoring.Occurrence({
            "type": "Death",
            "para": [self.UID, self.OwnNO]
        })
        return True

    def DeathProcessing(self, event):
        # 检测到别人死亡时战斗力增加
        UID = event['para'][0]
        if (UID != self.UID):
            self.SelfCombat += self.skill_carrion_increased_combat

    def ToNextTurn(self):
        # 场替时注销触发器
        self.ThisGame.eventMonitoring.UnBundledDeathTrigger(self)


# --------------- 灵 -----------------

class Spirit(UnitCard):
    def __init__(self):
        super().__init__(
            name="灵",
            desc="自然元素在时间的积累中幻化出的生命\n"
                 "◇魔法生物：这个单位是由魔力构成的",
            combat=1,
            level=1,
            label={
                "自然", "魔法生物",
            }
        )


# --------------- 八刀魔偶 -----------------

class DobbyGolem(UnitCard):
    def __init__(self):
        self.fast_speed_combat_add = 3
        super().__init__(
            name="八刀魔偶",
            desc="罕见的机械族，早已失去了心智，成为了一个无情的屠戮机器\n"
                 "◇伪装：可以伪装成人类，具有人类属性\n"
                 "◇高速演算：打出时有50%几率附带高速演算效果，战斗力+{}"
                .format(self.fast_speed_combat_add),
            combat=8,
            level=3,
            label={
                "机械", "人类"
            }
        )
        self.effect = Effect.FastSpeedCalculus(self.fast_speed_combat_add)

    def Debut(self, ins) -> bool:
        if (choice([True, False])):
            self.AddStatus(self.effect)
        return True


# --------------- 座狼 -----------------

class BigWolf(UnitCard):
    def __init__(self):
        self.night_combat_add = 2
        super().__init__(
            name="座狼",
            desc="森林中的狼王\n"
                 "◇夜行：附带有夜行效果,在夜晚这个单位的战斗力+{},".format(self.night_combat_add),
            combat=5,
            level=2,
            label={
                "动物",
            }
        )
        self.effect = Effect.Nocturnal(self.night_combat_add)

    def Debut(self, ins) -> bool:
        self.AddStatus(self.effect)
        return True


# --------------- 大哥布林 -----------------

class GiantGoblin(UnitCard):
    def __init__(self):
        super().__init__(
            name="大哥布林",
            desc="大型的野生哥布林，是哥布林中少有的变异个体",
            combat=5,
            level=2,
            label={
                "亚人",
            }
        )


# --------------- 哥布林王者 -----------------

class GoblinKing(UnitCard):
    def __init__(self):
        self.combat_up = 1
        self.max_summon_num = 4
        super().__init__(
            name="欧利德",
            desc="◇哥布林王者：这家伙是千年才会出现一次的哥布林的王，及其罕见的个体，具有高度知性；\n"
                 "◇界者：这家伙是一名界者，拥有超越普通个体极限数倍的能力；\n"
                 "◇森林军团：出牌时，对方战场每有一张单位牌，则在己方随机战线召唤一只森林单位，最多{}只；\n"
                 "◇咆哮鼓舞：出牌时，为己方所有单位施加鼓舞效果，战斗力+{}；"
                 "".format(self.max_summon_num, self.combat_up),
            combat=11,
            level=4,
            label={
                "亚人", "界者",
            }
        )
        self.combat_up_effect = Effect.KingTactics(self.combat_up)

    def Debut(self, ins) -> bool:
        # 森林军团
        num = min(len(self.OwnPlayer.OpPlayer.UIDCardDict), self.max_summon_num)
        randomSummon = [Goblin(), Wolf(), GiantGoblin()]
        for i in range(num):
            card = deepcopy(choice(randomSummon))
            card.UID = GetUID()
            self.ThisGame.AddCardToLine(self.OwnPlayer, randint(0, 2), card)

        # 王之战术
        for card in self.OwnPlayer.UIDCardDict.values():
            card.AddStatus(self.combat_up_effect)

        return True


# --------------- 帝国弓箭手 -----------------

class ImperialShotter(UnitCard):
    def __init__(self):
        super().__init__(
            name="帝国弓箭手",
            desc="帝国的一名普普通通的弓箭手",
            combat=3,
            level=1,
            label={
                "人类", "帝国",
            }
        )


# --------------- 彼特杰罗夫 -----------------

class PiterJerLfu(UnitCard):
    def __init__(self):
        self.get_card_num = 1
        super().__init__(
            name="彼特杰罗夫",
            desc="◇银血指挥官：帝国前线作战总指挥官\n"
                 "◇补给：打出后抽取{}张牌"
                 "".format(self.get_card_num),
            combat=8,
            level=3,
            label={
                "人类", "帝国",
            }
        )

    def Debut(self, ins) -> bool:
        self.OwnPlayer.GetCards(self.get_card_num)
        return True


# --------------- 青 -----------------

class Blueness(UnitCard):
    def __init__(self):
        self.assassinate_dmg = 5
        super().__init__(
            name="青",
            desc="◇雾行者：这家伙是雾行者刺客\n"
                 "◇刺杀：对目标单位造成{}点计略伤害"
                 "".format(self.assassinate_dmg),
            combat=5,
            level=3,
            label={
                "亚人", "亚精灵", "雾行者的匕首",
            }
        )

    def Debut(self, ins) -> bool:
        try:
            if(ins[1]!=NoSpell):
                card = self.ThisGame.UIDCardDict[ins[1]]
                card.GetDamage(self.assassinate_dmg, {"计略"})
            return True
        except:
            #可以不选中单位
            return True


# --------------- K-902 -----------------

class K_902(UnitCard):
    def __init__(self):
        self.magic_dmg_off = 0.6
        self.basis_combat_add = 9
        super().__init__(
            name="K-902",
            desc="罕见的机械族，拥有高度知性和传说装备的巨大人形武器\n"
                 "◇应激反魔法装甲：受到的魔法伤害减少{}%\n"
                 "◇终焉作战模式展开: 在第三场时打出，基础作战力 +{}"
                 "".format(self.magic_dmg_off * 100, self.basis_combat_add),
            combat=9,
            level=4,
            label={
                "机械",
            }
        )

    def Debut(self, ins) -> bool:
        if (self.ThisGame.NumberOfInnings == 2):
            self.SelfCombat += self.basis_combat_add
        return True

    def GetDamage(self, num, effectLabel):
        if (Has("魔法", effectLabel)):
            num = int(round(num * (1 - self.magic_dmg_off)))
        self.SelfCombat -= num
        if (self.SelfCombat < 0 and self.Dead()):
            pass
        else:
            self.SelfCombat = 0
        return True


# --------------- 浴火凤凰 -----------------

class BathFirePhoenix(UnitCard):
    def __init__(self):
        self.is_egg = False
        super().__init__(
            name="浴火凤凰",
            desc="传说中的不死神兽\n"
                 "◇长生：无视场替\n"
                 "◇不死：死亡时变成一颗凤凰蛋，战斗力归0，并在下一场复活",
            combat=11,
            level=4,
            label={
                "自然",
            }
        )

    def Dead(self) -> bool:
        # 不死
        self.is_egg = True
        self.Name = "凤凰蛋"
        return False

    def ToNextTurn(self) -> bool:
        # 不死
        if (self.is_egg):
            self.is_egg = False
            self.Name = "浴火凤凰"
            self.SelfCombat = 11
            self.Level = 4
            self.Label.add("自然")
        # 长生
        return False


# --------------- 低阶吸血鬼 -----------------

class LowerOrderVampire(UnitCard):
    def __init__(self):
        self.night_combat_add = 4
        super().__init__(
            name="低阶吸血鬼",
            desc="血缘下贱的下等吸血鬼\n"
                 "◇长生：无视场替\n"
                 "◇伪装：擅长伪装成人类，具有人类属性\n"
                 "◇夜行：附带有夜行效果,在夜晚这个单位的战斗力+{},".format(self.night_combat_add),
            combat=3,
            level=3,
            label={
                "血族", "人类"
            }
        )
        self.effect = Effect.Nocturnal(self.night_combat_add)

    def Debut(self, ins) -> bool:
        self.AddStatus(self.effect)
        return True

    def ToNextTurn(self) -> bool:
        return False

# ---------------  -----------------