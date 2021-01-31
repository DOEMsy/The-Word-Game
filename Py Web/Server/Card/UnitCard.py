from Card.Card import *
from ExternalLibrary.ExternalLibrary import toDict


class UnitCard(Card):
    def __init__(self, name: str, desc: str, combat: int, level: int, label: []):
        super().__init__(name, desc)
        self.SelfCombat = combat  # 基础值战斗力
        self.Level = level  # 等级
        self.Label = label  # 标签
        self.Type = "UnitCard"  # 卡牌类型
        self.Status = []  # 卡牌状态槽

    # 出牌
    # ins =  [card_type,to...]
    # 对于普通单位牌，to 只有一项
    def Play(self, player, ins) -> bool:
        try:
            card_type = ins[0]
            card_uid = int(ins[1])
            if (card_uid != self.UID): return False
            to = list(map(int, ins[2:]))
            if (card_type != self.Type):   return False
            if (3 >= to[0] > 0 and self.Debut(to)):
                player.Lines[to[0] - 1].append(self)
            # 打到对面牌区
            # elif (-3 <= to[0] < 0 and self.Debut(to)):
            #    player.OpPlayer.Lines[-1 - to[0]].append(self)
            else:
                return False
            return True
        except:
            return False

    # 应用值战斗力
    def Combat(self) -> int:
        if (self.SelfCombat == 0):  return 0  # 濒死
        res = self.SelfCombat
        for se in self.Status:
            res += se.CombatAmend()
        return max(res, 0)  # 最低不能少于0

    # 出牌效果
    def Debut(self, ins) -> bool:

        # 使用技能？
        # 注册触发器？如果有需要的话

        # 0.2.1 注"销"触发器需要看逻辑时机会，
        # 例如一个卡牌死亡后自爆，则触发器注销应在触发DeathProcessing中，执行完自爆后再注销
        # 如果注销在 CanDead 函数中，那么将可能无法完成自爆
        # 再例如一个监视别人死亡的卡牌，则触发器注销可以放在 Dead 函数中，也可以放在 DeathProcessing 中
        # 但是如果是一张监视出牌的卡片，注册的是其他触发器，DeathProcessing 不会被执行， 那么需要注销就不能放在 DeathProcessing 中
        # 同时 绝大部分正常的卡，场替的时候都要注销触发器

        return True

    # 单位在场效果，打入战区，玩家回合结束结算
    def OnCourt(self) -> bool:
        return True

    # 全局效果，打入全局效果区，每轮结束结算
    def Round(self) -> bool:
        return True

    # 场替
    def ToNextTurn(self) -> bool:
        return True

    # 受到伤害 基础战力
    def GetDamage(self, num):
        self.SelfCombat -= num
        if (self.SelfCombat < 0 and self.Dead()):
            pass
        else:
            self.SelfCombat = 0
        return True

    # 死亡，可以执行这个函数进行即死
    def Dead(self) -> bool:
        self.ThisGame.eventMonitoring.Occurrence({
            "type": "Death",
            "para": [self.UID, self.OwnNO]
        })
        return True

    # 死亡触发器,用于技能
    #   死亡event = {
    #       "type" : "Death",
    #       "para" : [UID,OwnNO]
    #   }
    #
    def DeathProcessing(self, event):
        return True

    # 转换长字串
    def lstr(self) -> str:
        return "[{},{},{},{},{},{}]".format(self.UID, self.Type, self.Name, self.Combat(), self.Level, self.Desc)

    # 转换短字串
    def sstr(self) -> str:
        return "[{},{},{},{}]".format(self.UID, self.Name, self.Combat(), self.Level)

    # 转换dict
    def dict(self) -> dict:
        res = {
            "Name": self.Name,
            "Desc": self.Desc,
            "Type": self.Type,
            "Combat": self.Combat(),
            "Label": self.Label,
            "Level": self.Level,
            "SelfCombat": self.SelfCombat,
            "Status": toDict(self.Status),
            "UID": self.UID,
        }
        return res
