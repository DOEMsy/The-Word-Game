from copy import deepcopy
from random import choice, randint, random, sample

import numpy as np

from Card.StatusEffect import StatusEffect
from Card.UnitCard import UnitCard
from ExternalLibrary.ExternalLibrary import GetUID, NoSpell, ConcretizationCard, GetRandCard
from Game.Label import Has, Is
from Mod.OriginalPackage import Effect, Skill


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
            },
            canto={1},
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
            },
            canto={1, 3},
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
            },
            canto={1},
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
            },
            canto={1},
        )
        # 注册死亡触发器
        self.Monitor_Death = True

    def _deathProcessing(self, event):
        # 检测到别人死亡时战斗力增加
        UID = event['para'][0]
        if (UID != self.UID):
            # self.SelfCombat += self.skill_carrion_increased_combat
            self.AddSelfCombat(self.skill_carrion_increased_combat)


# --------------- 帝国骑士 -----------------

class ImperialKnight(UnitCard):
    def __init__(self):
        super().__init__(
            name="帝国骑士",
            desc="帝国强大的地面部队，擅长快速作战；\n◇冲锋：出牌时，打出在第一行时，基础战斗力+1",
            combat=5,
            level=2,
            label={
                "人类", "帝国"
            },
            canto={1, 3},
        )

    def _debut(self, ins):
        # 冲锋
        if (ins[0] == 1):
            # self.SelfCombat += 1
            self.AddSelfCombat(1)
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
            },
            canto={1, 2, 3},
        )

    # to = ins = [local,target_UID]
    def _debut(self, ins) -> bool:
        try:
            if (ins[1] != NoSpell):
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
            },
            canto={1},
        )
        # 注册死亡触发器
        self.Monitor_Death = True

    def _deathProcessing(self, event):
        # 检测到别人死亡时战斗力增加
        UID = event['para'][0]
        if (UID != self.UID):
            # self.SelfCombat += self.skill_carrion_increased_combat
            self.AddSelfCombat(self.skill_carrion_increased_combat)


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
            },
            canto={1, 3},
        )
        # 注册死亡触发器
        self.Monitor_Death = True

    def _deathProcessing(self, event):
        # 检测到别人死亡时战斗力增加
        UID = event['para'][0]
        if (UID != self.UID):
            # self.SelfCombat += self.skill_carrion_increased_combat
            self.AddSelfCombat(self.skill_carrion_increased_combat)


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
            },
            canto={1, 3},
        )
        # 注册死亡触发器
        self.Monitor_Death = True

    def _deathProcessing(self, event):
        # 检测到别人死亡时战斗力增加
        UID = event['para'][0]
        if (UID != self.UID):
            # self.SelfCombat += self.skill_carrion_increased_combat
            self.AddSelfCombat(self.skill_carrion_increased_combat)


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
            },
            canto={2},
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
            },
            canto={1, 2},
        )
        self.effect = Effect.FastSpeedCalculus(self.fast_speed_combat_add)

    def _debut(self, ins) -> bool:
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
            },
            canto={1},
        )
        self.effect = Effect.Nocturnal(self.night_combat_add)

    def _debut(self, ins) -> bool:
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
            },
            canto={1},
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
                 "◇森林军团：出牌时，对方战场每比己方多一张单位牌，则在己方随机战线召唤一只森林单位，最多{}只；\n"
                 "◇咆哮鼓舞：为欧利德召唤的所有单位施加鼓舞效果，战斗力+{}；"
                 "".format(self.max_summon_num, self.combat_up),
            combat=9,
            level=4,
            label={
                "亚人", "界者",
            },
            canto={1},
        )
        self.combat_up_effect = Effect.KingTactics(self.combat_up)

    def _debut(self, ins) -> bool:
        # 森林军团
        num = min(max(0, (len(self.OwnPlayer.OpPlayer.UIDCardDict) - len(self.OwnPlayer.UIDCardDict))),
                  self.max_summon_num)
        randomSummon = [Goblin(), Wolf(), GiantGoblin()]
        for i in range(num):
            card = ConcretizationCard(choice(randomSummon))
            # 王之战术
            card.AddStatus(self.combat_up_effect)
            self.ThisGame.AddCardToLine(self.OwnPlayer, randint(0, 2), card)

        # 王之战术(废弃)
        # for card in self.OwnPlayer.UIDCardDict.values():
        #     card.AddStatus(self.combat_up_effect)

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
            },
            canto={1, 3},
        )

    def _debut(self, ins) -> bool:
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
            },
            canto={2},
        )

    def _debut(self, ins) -> bool:
        try:
            if (ins[1] != NoSpell):
                card = self.ThisGame.UIDCardDict[ins[1]]
                card.GetDamage(self.assassinate_dmg, {"计略"})
            return True
        except:
            # 可以不选中单位
            return True


# --------------- K-902 -----------------

class K_902(UnitCard):
    def __init__(self):
        self.magic_dmg_off = 0.6
        self.basis_combat_add = 10
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
            },
            canto={2},
        )

    def _debut(self, ins) -> bool:
        if (self.ThisGame.NumberOfInnings == 2):
            self.SelfCombat += self.basis_combat_add
        return True

    def _getDamage(self, num, effectLabel):
        if (Has("魔法", effectLabel)):
            num = int(round(num * (1 - self.magic_dmg_off)))
        self.SelfCombat -= num
        return num


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
            },
            canto={2},
        )

    def _dead(self) -> bool:
        # 不死
        if(self.is_egg==False):
            self.is_egg = True
            self.SelfCombat = 0
            self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + " 因技能 <不死> 变成了凤凰蛋 ")
            self.Name = "凤凰蛋"
        return False

    def _toNextTurn(self) -> bool:
        # 不死
        if (self.is_egg):
            self.is_egg = False
            self.Name = "浴火凤凰"
            self.SelfCombat = 11
            self.Level = 4
            self.Label.add("自然")
            self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + " 因技能 <不死> 复活了 ")
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
            },
            canto={2},
        )
        self.effect = Effect.Nocturnal(self.night_combat_add)

    def _debut(self, ins) -> bool:
        self.AddStatus(self.effect)
        return True

    def _toNextTurn(self) -> bool:
        return False


# --------------- 奥拓麦迪克神圣教国大祭司 -----------------

class HighPriestofAltoMadike(UnitCard):
    def __init__(self):
        self.card_num = 2
        self.dmg_off = 0.33
        super().__init__(
            name="奥拓麦迪克神圣教国大祭司",
            desc="◇神职人员：这单位是奥拓麦迪克神圣教国大祭司\n"
                 "◇圣光加护：该单位对圣吟伤害有{}%免疫\n"
                 "◇大审判官：出牌后向玩家手牌中塞入{}张异端审判卡牌"
                 "".format(self.dmg_off * 100, self.card_num),
            combat=3,
            level=4,
            label={
                "人类", "神圣教国"
            },
            canto={3},
        )
        self.summon = Skill.ReligiousTrial()

    def _debut(self, ins) -> bool:
        for _ in range(self.card_num):
            card = ConcretizationCard(self.summon)
            card.Pump(self.OwnPlayer)
        return True

    def _getDamage(self, num, effectLabel):
        if (Has("圣吟", effectLabel)):
            num = int(round(num * (1 - self.dmg_off)))
        self.SelfCombat -= num
        return num


# --------------- 伊莉娜丝 -----------------

class Irinas(UnitCard):
    def __init__(self):
        self.night_combat_add = 2
        super().__init__(
            name="伊莉娜丝",
            desc="十三英雄之一，外貌如孩童一般的人类与吸血鬼的混血儿，希德尼亚魔法学院的特聘教师\n"
                 "◇半吸血鬼：同时具有人类和血族属性，但是血族的能力有所下降\n"
                 "◇长生：无视场替\n"
                 "◇夜行：附带有夜行效果,在夜晚这个单位的战斗力+{}\n"
                 "◇大魔法师：打出后随机获得数张Lv4及以下的魔法卡牌".format(self.night_combat_add),
            combat=7,
            level=4,
            label={
                "血族", "人类"
            },
            canto={2},
        )
        self.effect = Effect.Nocturnal(self.night_combat_add)

    def _debut(self, ins) -> bool:
        self.AddStatus(self.effect)
        # bug？无法复现

        cards = sample(ConcretizationCard(*(
                GetRandCard({"Level": 4, "Label": {"魔法"}}, 1) +
                GetRandCard({"Level": 3, "Label": {"魔法"}}, 2) +
                GetRandCard({"Level": 2, "Label": {"魔法"}}, 2) +
                GetRandCard({"Level": 1, "Label": {"魔法"}}, 2)
        )), randint(1, 4))


        for cd in cards:
            cd.Pump(self.OwnPlayer)
        return True

    def _toNextTurn(self) -> bool:
        return False


# --------------- 兔疣 -----------------

class RabbitWart(UnitCard):
    def __init__(self):
        self.give_probability = 1.00
        self.probability_recession = 0.8
        self.max_fenlie = 3
        self.min_fenlie = 2
        super().__init__(
            name="兔疣",
            desc="很多只没有像无毛兔子的小动物的肉体混乱的拼接在了一起\n"
                 "◇恶魔：这家伙是个恶魔，不属于现世\n"
                 "◇群居：出牌时有{}%概率再获得一张相同卡牌\n"
                 "◇分裂：当一只兔疣死亡后，会分裂成{}~{}个小兔疣，小兔疣不具有分裂能力"
                 "".format(self.give_probability * 100, self.min_fenlie, self.max_fenlie),
            combat=1,
            level=4,
            label={
                "恶魔",
            },
            canto={1, 2, 3},
        )
        self.summon = UnitCard(
            name="小兔疣",
            desc="由一只兔疣分裂而成\n"
                 "◇恶魔：这家伙是个恶魔，不属于现世",
            combat=1,
            level=4,
            label={
                "恶魔",
            }
        )
        # 注册死亡触发器 分裂
        self.Monitor_Death = True

    def _debut(self, ins):
        # 群居
        if (np.random.choice([
            True, False
        ], p=np.array([
            self.give_probability,
            1 - self.give_probability
        ]).ravel())):
            card = ConcretizationCard(RabbitWart())
            card.give_probability *= self.probability_recession
            card.Desc = "很多只没有像无毛兔子的小动物的肉体混乱的拼接在了一起\n" \
                        "◇恶魔：这家伙是个恶魔，不属于现世\n" \
                        "◇群居：出牌时有{}%概率再获得一张相同卡牌\n" \
                        "◇分裂：当一只兔疣死亡后，会分裂成{}~{}个小兔疣，小兔疣不具有分裂能力" \
                        "".format(card.give_probability * 100, card.min_fenlie, card.max_fenlie)
            card.Pump(self.OwnPlayer)

        return True

    def _deathProcessing(self, event):
        # 分裂，死亡时变成两个小兔疣
        UID = event['para'][0]
        if (UID == self.UID):
            summonNum = randint(self.min_fenlie, self.max_fenlie)
            for _ in range(summonNum):
                card = ConcretizationCard(self.summon)
                self.ThisGame.AddCardToLine(self.OwnPlayer, self.Location, card)


# --------------- 虚灵 -----------------

class Aetherial(UnitCard):
    def __init__(self):
        self.combat_conversion = 2
        self.promote_efficiency = 0.5
        super().__init__(
            name="虚灵",
            desc="能够同化吸收世间万物的自然灵体\n"
                 "◇魔法生物：这个家伙的身体是由魔力构成的\n"
                 "◇吸收：每当有一个有效果或伤害作用于该单位，则该单位基础战斗力+{}\n"
                 "◇适应：基础战斗力提升效率+{}%"
                 "".format(self.combat_conversion, self.promote_efficiency * 100),
            combat=4,
            level=2,
            label={
                "自然", "魔法生物"
            },
            canto={2},
        )

    def _addSelfCombat(self, num, effectLabel):
        # 吸收
        num += 2
        # 适应
        num *= (1 + self.promote_efficiency)
        self.SelfCombat += num
        return num

    def _getDamage(self, num, effectLabel):
        self.SelfCombat -= num
        self.AddSelfCombat(0)
        return num

    # 添加效果
    def _addStatus(self, status):
        status.Apply(self)
        self.AddSelfCombat(0)


# --------------- 破坏之神 哈威克 -----------------

class Harwick(UnitCard):
    def __init__(self):
        self.throw_card_num = 3
        super().__init__(
            name="哈威克",
            desc="外神，破坏之神，具有将一切粉碎的权能\n"
                 "◇神明：这单位是一名神\n"
                 "◇神羽：不会受到任何的伤害和状态效果，但是不免疫死亡\n"
                 "◇权能·瓦解：出牌时己方玩家随机弃掉最多{}张手牌\n"
                 "◇权能·毁灭：出牌时对场上所有单位造成随机正整数的神术伤害"
                 "".format(self.throw_card_num),
            combat=15,
            level=5,
            label={
                "神明",
            },
            canto={3},
        )

    def _debut(self, ins) -> bool:
        # 瓦解
        self.OwnPlayer.ThrowCards_RandForNum(self.throw_card_num)
        # 毁灭
        for target in self.ThisGame.UIDCardDict.values():
            target.GetDamage(randint(1, int(9e18)), {"神术"})

        return True

    def _getDamage(self, num, effectLabel):
        return False

    def _addStatus(self, status):
        return False


# --------------- 骸骨战士 -----------------

class SkeletonSoldier(UnitCard):
    def __init__(self):
        super().__init__(
            name="骸骨战士",
            desc="生前可能是个冒险者，或者是个士兵？因为某种原因即便只有骨架依旧战斗的战士，不具有知性",
            combat=3,
            level=1,
            label={
                "亡骸",
            },
            canto={1},
        )


# --------------- 骷髅法师 -----------------

class SkeletalMage(UnitCard):
    def __init__(self):
        super().__init__(
            name="骷髅法师",
            desc="某个法师死后只记得他的法术技能",
            combat=5,
            level=2,
            label={
                "亡骸",
            },
            canto={2},
        )


# --------------- 幽魂 -----------------

class Ghosts(UnitCard):
    def __init__(self):
        super().__init__(
            name="幽魂",
            desc="游荡的灵魂，很少具有攻击性",
            combat=2,
            level=1,
            label={
                "幽灵",
            },
            canto={1},
        )


# --------------- 幽魂之母 -----------------

class MotherofGhosts(UnitCard):
    def __init__(self):
        self.summon_num = 3
        super().__init__(
            name="幽魂之母",
            desc="具有强大魔力的灵魂"
                 "◇幽魂：出场时于同行召唤{}只幽魂\n"
                 "◇束灵：场上每有一个单位死亡，则在己方战场随机召唤一只幽魂"
                 "".format(self.summon_num),
            combat=7,
            level=3,
            label={
                "幽灵",
            },
            canto={2},
        )
        # 注册死亡触发器
        self.Monitor_Death = True
        self.summon = Ghosts()

    def _debut(self, ins) -> bool:
        # 幽魂
        for _ in range(self.summon_num):
            card = ConcretizationCard(self.summon)
            self.ThisGame.AddCardToLine(self.OwnPlayer, ins[0] - 1, card)
        return True

    def _deathProcessing(self, event):
        # 束灵 检测到别人死亡
        UID = event['para'][0]
        if (UID != self.UID):
            # self.SelfCombat += self.skill_carrion_increased_combat
            card = ConcretizationCard(self.summon)
            self.ThisGame.AddCardToLine(self.OwnPlayer, randint(0, 2), card)


# --------------- 魔力之源 -----------------

class MagicSource(UnitCard):
    def __init__(self):
        super().__init__(
            name="魔力之源",
            desc="蕴含一定魔力的源质点，可以与某些魔法产生联动\n"
                 "◇联动：每当己方玩家打出一张带有“魔法”或“魔法生物”的卡牌时，就会免费释放一次魔法飞弹",
            combat=0,
            level=3,
            label={
                "魔法生物",
            },
            canto={2},
        )
        self.summon = Skill.MagicMissile()
        # 注册出牌触发器
        self.Monitor_Pop = True

    def _popProcessing(self, event):
        NO = event["para"][0]
        card_pop = event["para"][1]
        if (NO == self.OwnPlayer.NO and card_pop.UID!=self.UID):
            if (Is("魔法", card_pop) or Is("魔法生物", card_pop)):
                card = ConcretizationCard(self.summon)
                card.OwnPlayer = self.OwnPlayer
                card.Debut([])

        return True


# --------------- 水晶巨人 -----------------

class GlassGiant(UnitCard):
    def __init__(self):
        self.dmg_li = 5
        super().__init__(
            name="水晶巨人",
            desc="由自然孕育出来的有思维的活水晶\n"
                 "◇脆弱：单次受到≥{}点的伤害立即死亡"
                 "".format(self.dmg_li),
            combat=14,
            level=3,
            label={
                "自然",
            },
            canto={1},
        )

    def _getDamage(self, num, effectLabel):
        if (num >= self.dmg_li):
            self.Dead()
        else:
            self.SelfCombat -= num
        return num


# --------------- 岩石巨人 -----------------

class StoneGiant(UnitCard):
    def __init__(self):
        self.dmg_off = 0.5
        self.min_dmg = 1
        self.cmt_dd = 3
        super().__init__(
            name="岩石巨人",
            desc="由自然孕育出来的有思维的活石头\n"
                 "◇坚硬：受到的物理伤害减少{}%，最低不少于{}\n"
                 "◇笨重：所在行内每有一个其他单位则自身战斗力-{}"
                 "".format(self.dmg_off * 100, self.min_dmg, self.cmt_dd),
            combat=13,
            level=3,
            label={
                "自然",
            },
            canto={1},
        )
        self.effect = Effect.ReduceCombatEffectivenessAccordingNumberofOtherUnitsInLine(
            name="笨重",
            combatAmend=self.cmt_dd,
            desc="所在行内每有一个其他单位则自身战斗力-{}".format(self.cmt_dd),
            label={"特性"}
        )

    def _debut(self, ins) -> bool:
        self.AddStatus(self.effect)
        return True

    def _getDamage(self, num, effectLabel):
        if (Has("物理", effectLabel)):
            num = int(round(num * (1 - self.dmg_off)))
        self.SelfCombat -= num
        return num


# --------------- 寒霜巨人 -----------------

class SnowGiant(UnitCard):
    def __init__(self):
        super().__init__(
            name="寒霜巨人",
            desc="由自然孕育出来的有思维的活体雪巨人\n"
                 "◇寒霜抗性：不会受到寒霜天气影响"
                 "".format(),
            combat=12,
            level=3,
            label={
                "自然",
            },
            canto={1},
        )

    def _addStatus(self, status):
        if (Is("寒霜", status)):
            return False
        status.Apply(self)
        return True


# --------------- 曼德拉草 -----------------

class Mandrake(UnitCard):
    def __init__(self):
        self.tarline = 1
        self.max_level_att = 3
        self.dmg = 4
        self.baqi = False
        super().__init__(
            name="曼德拉草",
            desc="根部形似人类的植物，含有大量有毒的致幻成分\n"
                 "◇扎根/拔起：打出后种入地下，战斗力归0。当受到伤害时，将免疫一次伤害，钻出地面，进入战斗状态\n"
                 "◇尖叫：拔起时，对双方{}排所有lv{}及以下单位造成{}点魔法伤害"
                 "".format(self.tarline, self.max_level_att, self.dmg),
            combat=3,
            level=2,
            label={
                "自然",
            },
            canto={1},
        )
        self.cmt = self.SelfCombat

    def _debut(self, ins) -> bool:
        self.Name = "曼德拉草（扎根）"
        self.SelfCombat = 0
        self.baqi = False
        return True

    def _getDamage(self, num, effectLabel):
        if (not self.baqi):
            self.Name = "曼德拉草"
            self.SelfCombat = self.cmt
            self.baqi = True
            num = 0
            for card in self.OwnPlayer.Lines[self.tarline - 1]:
                if(card.UID!=self.UID):
                    card.GetDamage(self.dmg, {"魔法"})
            for card in self.OwnPlayer.OpPlayer.Lines[self.tarline - 1]:
                card.GetDamage(self.dmg, {"魔法"})
        self.SelfCombat -= num
        return num


# --------------- 招财铃铛 -----------------

class Bell(UnitCard):
    def __init__(self):
        self.get_card_num = 1
        self.cumulative_damage = 0
        self.can_damage = 5
        self.least_num = 5
        super().__init__(
            name="招财铃铛",
            desc="可以带来好运的铃铛\n"
                 "◇非战斗：该牌基础战斗力恒为0\n"
                 "◇强运：每当该牌累计受到一定伤害，就可以使得己方抽取{}张牌，当累计发动{}次后该牌失效（判定为死亡）"
                 "".format(self.get_card_num, self.least_num),
            combat=0,
            level=3,
            label={
                "宝具",
            },
            canto={1, 2, 3},
        )

    def _addSelfCombat(self, num, effectLabel):
        self.SelfCombat = 0
        return 0

    def _getDamage(self, num, effectLabel):
        self.SelfCombat = 0
        self.cumulative_damage += num
        if (self.cumulative_damage >= self.can_damage):
            getcardnum = self.cumulative_damage // self.can_damage
            getcardnum = min(getcardnum, self.least_num)
            self.cumulative_damage %= self.can_damage
            self.OwnPlayer.GetCards(getcardnum)
            self.least_num -= getcardnum
            if (self.least_num == 0):
                self.Dead()
        return num


# --------------- 骸骨巨人 -----------------

class SkeletonGiant(UnitCard):
    def __init__(self):
        self.cmt_add = 3
        super().__init__(
            name="骸骨巨人",
            desc="某种巨大人形魔物的尸骸\n"
                 "◇异形：可以随意操控躯体，以出人意料的方式作战，战斗力+{}"
                 "".format(self.cmt_add),
            combat=10,
            level=3,
            label={
                "亡骸",
            },
            canto={1},
        )
        self.effect = Effect.SingleBuffingBuffTemplate(
            name="异形",
            desc="该单位可以随意操控躯体，以出人意料的方式作战，战斗力+{}"
                 "".format(self.cmt_add),
            combatAmend=self.cmt_add,
            label={"特性"}
        )

    def _debut(self, ins) -> bool:
        self.AddStatus(self.effect)
        return True


# --------------- 恶·极 -----------------

class Evilest(UnitCard):
    def __init__(self):
        self.dmg_up = 1.00
        self.change_cmt_line = 16
        super().__init__(
            name="恶·极",
            desc="由世间万物的恶，孕育而成\n"
                 "◇罪恶：受到圣吟伤害增加{}%\n"
                 "◇集恶：同时拥有恶魔、不死者、腐化属性\n"
                 "◇终恶：打出时基础战斗力增加双方墓地卡牌数量的数值，若打出时战斗力达到{}点则变成最终之恶，各项属性翻倍"
                 "".format(self.dmg_up * 100, self.change_cmt_line),
            combat=0,
            level=4,
            label={
                "不死者", "恶魔", "腐化",
            },
            canto={2},
        )

    def _debut(self, ins) -> bool:
        self.SelfCombat += len(self.OwnPlayer.UnitGrave) + len(self.OwnPlayer.OpPlayer.UnitGrave)
        if (self.SelfCombat >= self.change_cmt_line):
            self.Name = "最终之恶"
            self.SelfCombat *= 2
            self.Level += 1
            self.dmg_up *= 2
            self.Desc = "世上最大最暴力的恶，颠覆常理的存在\n" \
                        "◇罪恶：受到圣吟伤害增加{}%\n" \
                        "◇集恶：同时拥有恶魔、不死者、腐化属性".format(self.dmg_up * 100)
        return True

    def _getDamage(self, num, effectLabel):
        if (Has("圣吟", effectLabel)):
            num = int(round(num * (1 + self.dmg_up)))
        self.SelfCombat -= num
        return num


# --------------- 细米子群 -----------------

class Worm(UnitCard):
    def __init__(self):
        self.cmt_add = 1
        super().__init__(
            name="细米子群",
            desc="原野、森林中常见的野生小虫子，基本不具有危害性\n"
                 "◇数量之灾：己方每有一个其他的虫属性单位，自身战斗力+{}"
                 "".format(self.cmt_add),
            combat=0,
            level=1,
            label={
                "虫",
            },
            canto={1, 2, 3},
        )
        self.effect = Effect.NumberDisaster(self.cmt_add)

    def _debut(self, ins) -> bool:
        self.AddStatus(self.effect)
        return True


# --------------- 巨型马陆 -----------------

class GiantMalu(UnitCard):
    def __init__(self):
        self.cmt_add = 1
        self.min_dmg = 2
        self.max_dmg = 3
        super().__init__(
            name="巨型马陆",
            desc="巨型的多足食肉主义者\n"
                 "◇数量之灾：己方每有一个其他的虫属性单位，自身战斗力+{}\n"
                 "◇腐蚀：选定一个单位造成{}~{}点物理伤害"
                 "".format(self.cmt_add, self.min_dmg, self.max_dmg),
            combat=4,
            level=2,
            label={
                "虫",
            },
            canto={1, 2},
        )
        self.effect = Effect.NumberDisaster(self.cmt_add)

    def _debut(self, ins) -> bool:
        self.ThisGame.UIDCardDict[ins[1]].GetDamage(randint(self.min_dmg, self.max_dmg), {"物理"})
        self.AddStatus(self.effect)
        return True


# --------------- 兵蚁 -----------------

class Ants(UnitCard):
    def __init__(self):
        self.cmt_add = 1
        super().__init__(
            name="兵蚁",
            desc="中型的多足食肉主义者\n"
                 "◇数量之灾：己方每有一个其他的虫属性单位，自身战斗力+{}"
                 "".format(self.cmt_add),
            combat=4,
            level=2,
            label={
                "虫",
            },
            canto={1},
        )
        self.effect = Effect.NumberDisaster(self.cmt_add)

    def _debut(self, ins) -> bool:
        self.AddStatus(self.effect)
        return True


# --------------- 须龙 -----------------

class WormDragon(UnitCard):
    def __init__(self):
        self.cmt_add = 1
        super().__init__(
            name="须龙",
            desc="大型的空中多节掠食者\n"
                 "◇数量之灾：己方每有一个其他的虫属性单位，自身战斗力+{}\n"
                 "◇龙：具有龙属性"
                 "".format(self.cmt_add),
            combat=10,
            level=3,
            label={
                "虫", "龙"
            },
            canto={3},
        )
        self.effect = Effect.NumberDisaster(self.cmt_add)

    def _debut(self, ins) -> bool:
        self.AddStatus(self.effect)
        return True


# --------------- 大马士蝶 -----------------

class DamascusButterfly(UnitCard):
    def __init__(self):
        self.cmt_add = 1
        self.cmt_add2 = 4
        self.cmt_dbf = 2
        super().__init__(
            name="大马士蝶",
            desc="擅长拟态的巨大鳞翅目锤角亚目动物\n"
                 "◇数量之灾：己方每有一个其他的虫属性单位，自身战斗力+{}\n"
                 "◇拟态：打出时战斗力+{}\n"
                 "◇夺魂鳞粉：对选定行所有单位施加夺魂效果，战斗力-{}"
                 "".format(self.cmt_add, self.cmt_add2, self.cmt_dbf),
            combat=2,
            level=3,
            label={
                "虫",
            },
            canto={2},
        )
        self.effect = Effect.NumberDisaster(self.cmt_add)
        self.effect2 = Effect.SingleBuffingBuffTemplate(name="拟态", desc="该单位擅长拟态，战斗力+{}".format(self.cmt_add2),
                                                        combatAmend=self.cmt_add2, label={"计略"})
        self.effect3 = Effect.SingleDebuffingBuffTemplate(name="夺魂", desc="该单位沾染了鳞粉，战斗力-{}".format(self.cmt_dbf),
                                                          combatAmend=self.cmt_dbf, label={"魔法"})

    def _debut(self, ins) -> bool:
        tarline = None
        if (3 >= ins[1] > 0):
            tarline = self.OwnPlayer.Lines[ins[1] - 1]
        # 打到对面牌区
        elif (-3 <= ins[1] < 0):
            tarline = self.OwnPlayer.OpPlayer.Lines[- ins[1] - 1]
        else:
            return False
        for card in tarline:
            card.AddStatus(self.effect3)
        self.AddStatus(self.effect)
        self.AddStatus(self.effect2)
        return True


# --------------- 利维坦 -----------------

class Leviathan(UnitCard):
    def __init__(self):
        super().__init__(
            name="利维坦",
            desc="宛如一座空中之城的巨大虫族生物，遮云蔽日的天灾\n"
                 "◇数量之灾：己方每有一个其他的虫属性单位，自身战斗力+{}\n"
                 "◇雷云包裹：出牌时，杀死己方场上所有非虫属性单位，己方玩家弃掉所有手牌\n"
                 "◇天空要塞：在场时，敌方玩家每出一张牌，都会在己方战场随机召唤一只Lv3及以下的虫属性单位",
            combat=30,
            level=4,
            label={
                "虫", "龙"
            },
            canto={3},
        )
        self.Monitor_Pop = True

    def _debut(self, ins) -> bool:
        for card in self.OwnPlayer.UIDCardDict.values():
            if (not Is("虫", card)):
                card.Dead()
        self.OwnPlayer.ThrowCards_ALL()
        return True

    def _popProcessing(self, event):
        NO = event["para"][0]
        if (NO == self.OwnPlayer.OpPlayer.NO):
            card = ConcretizationCard(random.choice(
                GetRandCard({"Level": 3, "Label": {"虫"}}, 1) +
                GetRandCard({"Level": 2, "Label": {"虫"}}, 1) +
                GetRandCard({"Level": 1, "Label": {"虫"}}, 1)
            ))
            self.ThisGame.AddCardToLine(self.OwnPlayer, randint(0, 2), card)
        return True

# --------------- C++ -----------------
class CPrimePlus(UnitCard):
    def __init__(self):
        self.get_card_num = 2
        super().__init__(
            name="C++",
            desc="某个不知名的遗骸，也许有点什么用\n"
                 "◇优质祭品：该牌作为弃牌时，会获得{}张卡牌"
                 "".format(self.get_card_num),
            combat=0,
            level=3,
            label={
                "亡骸",
            },
            canto={1,2,3},
        )
    # 功能未实现