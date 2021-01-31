from random import choice

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
            name="帝国老兵",
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

class TestUnit1(UnitCard):
    def __init__(self):
        super().__init__(
            name="老段",
            desc="OSSA最强战力；技能·无敌：不会受到任何伤害；技能·嗜血：场上每有一个单位死亡，自身基础战斗力+1；技能·内鬼：出牌时33%概率打到对面战场",
            combat=0,
            level=1,
            label=[
                "Humanoid",
            ]
        )

    def Play(self, player, ins) -> bool:
        try:
            card_type = ins[0]
            card_uid = int(ins[1])
            if (card_uid != self.UID): return False
            to = list(map(int, ins[2:]))
            if (card_type != self.Type):   return False
            if (3 >= to[0] > 0 and self.Debut(to)):
                # 内鬼
                if(choice([True,True,False])):
                    player.Lines[to[0] - 1].append(self)
                else:
                    player.OpPlayer.Lines[to[0]-1].append(self)
            else:
                return False
            return True
        except:
            return False

    def Debut(self,ins):
        #注册触发器
        self.ThisGame.eventMonitoring.BundledDeathTrigger(self)
        return True

    def GetDamage(self, num):
        #无法受到伤害
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
        # 检测到别人死亡时战斗力+1
        UID = event['para'][0]
        if(UID != self.UID):
            self.SelfCombat+=1

    def ToNextTurn(self):
        # 场替时注销触发器
        self.ThisGame.eventMonitoring.UnBundledDeathTrigger(self)

class TestUnit2(UnitCard):
    def __init__(self):
        super().__init__(
            name="炮姐",
            desc="技能·鸽子：出牌时有50%概率消失",
            combat=0,
            level=1,
            label=[
                "Humanoid",
            ]
        )

    def Play(self, player, ins) -> bool:
        try:
            card_type = ins[0]
            card_uid = int(ins[1])
            if (card_uid != self.UID): return False
            to = list(map(int, ins[2:]))
            if (card_type != self.Type):   return False
            if (3 >= to[0] > 0 and self.Debut(to)):
                if(choice([True,False])):
                    player.Lines[to[0] - 1].append(self)
            # 打到对面牌区
            # elif (-3 <= to[0] < 0 and self.Debut(to)):
            #    player.OpPlayer.Lines[-1 - to[0]].append(self)
            else:
                return False
            return True
        except:
            return False


class TestUnit3(UnitCard):
    def __init__(self):
        super().__init__(
            name="wls",
            desc="wlsnb！：出牌时，所有可见字符都将变成wlsnb",
            combat=0,
            level=1,
            label=[
                "Humanoid",
            ]
        )

    def Debut(self, ins) -> bool:
        for player in self.ThisGame.Players:
            player.Name = "wlsnb"

            for card in player.HandCards:
                card.Name = "wlsnb"
                card.Desc = "wlsnb"

            for line in player.Lines:
                for card in line:
                    card.Name = "wlsnb"
                    card.Desc = "wlsnb"
        return True