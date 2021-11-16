from copy import deepcopy

from Card.Card import *
from ExternalLibrary import MsyEvent
from ExternalLibrary.ExternalLibrary import toDict, INT, PackList
from ExternalLibrary.MsyEvent import Death, Pop, GetDmg


class UnitCard(Card):
    def __init__(self, name: str, desc: str, combat: int, level: int, label: set, canto: set = {1, 2, 3},
                 shieldValue = 0,unleashOp=[0, False, 0, False], selDedication=0):
        super().__init__(name, desc)
        self.SelfCombat = combat  # 基础值战斗力
        self.Level = level  # 等级
        self.Label = label  # 标签
        self.Type = "UnitCard"  # 卡牌类型
        self.Status = dict()  # 卡牌状态槽 {作用UID:作用效果}
        self.Monitor_Death = False  # 死亡监视器
        self.Monitor_Pop = False  # 出牌监视器
        self.Monitor_GetDmg = False  # 单位受伤监视器

        self.Alive = True  # 保证死亡函数只能执行一次
        self.CantoLines = canto  # 可以打入的行
        self.UnleashOp = unleashOp
        self.SelDedication = selDedication
        self.Effect = []  # 固有效果
        self.ShieldValue = shieldValue  # 护盾版本 0.0.1 测试

        self.ComCard = dict()  # 指令卡牌，与本卡生命周期相同，{类型:数量}
        self._comCardUIDList = []

    # 出牌
    # ins =  [card_type,to...]
    # 对于普通单位牌，to 只有一项
    def Play(self, player, ins) -> bool:
        return self._play(player, ins)

    def _play(self, player, ins) -> bool:
        try:
            card_type = ins[0]
            card_uid = int(ins[1])
            if (card_uid != self.UID): return False
            to = list(map(INT, ins[2:]))
            if (card_type != self.Type):   return False
            if (to[0] in self.CantoLines):
                if (3 >= to[0] > 0 and self.Debut(to)):
                    self.ThisGame.AddCardToLine(player, to[0] - 1, self)
                    return True
                    # player.Lines[to[0] - 1].append(self)
                    # self.ThisGame.UIDCardDict[self.UID] = self
                # 打到对面牌区
                elif (-3 <= to[0] < 0 and self.Debut(to)):
                    self.ThisGame.AddCardToLine(player.OpPlayer, 1 - to[0], self)
                    return True
                    # elif (-3 <= to[0] < 0 and self.Debut(to)):
                    #    player.OpPlayer.Lines[-1 - to[0]].append(self)
            return False
        except Exception as e:
            print("card play error:", repr(e))
            return False

    # 应用值战斗力
    def Combat(self) -> int:
        return self._combat()

    # 战斗力 自身
    def _combat(self) -> int:
        if (self.SelfCombat == 0):  return 0  # 濒死
        res = self.SelfCombat
        for se in self.Status.values():
            res += self._combat_status(se)
        if (0 <= self.Location < 3):
            for ef in self.OwnPlayer.lineExisEffect[self.Location].values():
                res += self._combat_exis_effect(ef)
        return max(0, res)

    # 战斗力 响应效果值
    def _combat_status(self, status) -> int:
        return status.CombatAmend()

    # 战斗力 响应其他人存在时效果值
    def _combat_exis_effect(self, effect) -> int:
        res, label = effect.ExiEffect(self)
        return res

    # 出牌效果 注册函数
    def Debut(self, ins) -> bool:
        try:
            return self._debut(ins)
        except Exception as e:
            print("card debut error:", repr(e))

    # 出牌效果 实现函数
    def _debut(self, ins) -> bool:
        return True

    # 自施加效果启动，在部署到战场上时被调用
    def SelftoLineOn(self):

        self._selftoLineOn()
        # 施加效果
        for efc in self.Effect:
            self.AddStatus(efc)

        # 获取指令卡牌
        for tp, num in self.ComCard.items():
            for _ in range(num):
                card = ConcretizationCard(tp)
                self._comCardUIDList.append(card.UID)
                card.ComUnitNameUIDStr = "∈" + self.Name + '(' + str(self.UID) + ')'
                card.ComUnitUID = self.UID
                card.Pump(self.OwnPlayer)

        # 注册监视器
        # 死亡监视器
        if (self.Monitor_Death):
            self.ThisGame.eventMonitoring.BundledTrigger("Death", self)
        if (self.Monitor_Pop):
            self.ThisGame.eventMonitoring.BundledTrigger("Pop", self)
        if (self.Monitor_GetDmg):
            self.ThisGame.eventMonitoring.BundledTrigger("GetDmg", self)

        # 使用技能？
        # 注册触发器？如果有需要的话

        # 0.2.1 注"销"触发器需要看逻辑时机会，
        # 例如一个卡牌死亡后自爆，则触发器注销应在触发DeathProcessing中，执行完自爆后再注销
        # 如果注销在 CanDead 函数中，那么将可能无法完成自爆
        # 再例如一个监视别人死亡的卡牌，则触发器注销可以放在 Dead 函数中，也可以放在 DeathProcessing 中
        # 但是如果是一张监视出牌的卡片，注册的是其他触发器，DeathProcessing 不会被执行， 那么需要注销就不能放在 DeathProcessing 中
        # 同时 绝大部分正常的卡，场替的时候都要注销触发器

        # 注册存在时效果
        if (len(self.ExiEffectOn) > 0):
            self.ThisGame.RegisterExisEffect(self)

        return True

    # 返回值一定是 true
    def _selftoLineOn(self):
        return True

    # 单位在场效果，打入战区，玩家回合结束结算
    def OnCourt(self) -> bool:
        return self._onCourt()

    def _onCourt(self) -> bool:
        return True

    # 全局效果，打入全局效果区，每轮结束结算
    def Round(self) -> bool:
        return self._round()

    def _round(self) -> bool:
        return True

    # 场替
    def ToNextTurn(self) -> bool:
        if (self._toNextTurn()):

            # 吊销指令卡牌
            self.OwnPlayer.ThrowCards_withUIDList(self._comCardUIDList)

            # 场替注销触发器
            if (self.Monitor_Death):
                self.ThisGame.eventMonitoring.UnBundledTrigger("Death", self)
            if (self.Monitor_Pop):
                self.ThisGame.eventMonitoring.UnBundledTrigger("Pop", self)
            if (self.Monitor_GetDmg):
                self.ThisGame.eventMonitoring.UnBundledTrigger("GetDmg", self)

            # 注销存在时效果
            if (len(self.ExiEffectOn) > 0):
                self.ThisGame.UnRegisterExisEffect(self)

            return True
        return False

    def _toNextTurn(self) -> bool:
        return True

    # 受到伤害 基础战力
    # 返回值为受到该次攻击是否死亡
    # 1:   返回 0 没有受到伤害，返回 1 受到伤害，返回 2 受到伤害并死亡
    # 2:   受到伤害的实际数值
    def GetDamage(self, num, effectLabel, canUseShield=True):
        attack_res = 0

        # 护盾抗伤害
        shiedDmg = 0
        tmp = ""
        if (canUseShield):
            if (self.ShieldValue >= num):
                self.ShieldValue -= num
                shiedDmg = num
                num = 0
            else:
                num -= self.ShieldValue
                shiedDmg = self.ShieldValue
                self.ShieldValue = 0
            if (shiedDmg > 0):
                tmp += "护盾抵消了{}点伤害".format(shiedDmg)
                if (self.ShieldValue == 0): tmp += "并被击碎"
                tmp += "，本体"

        cureDmg = self._getDamage(num, effectLabel)
        if (cureDmg > 0):
            attack_res += 1
            self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + tmp + " 受到伤害 " + str(cureDmg))
        else:
            self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + tmp + " 免疫了伤害 ")
        if (self.SelfCombat < 0):
            if (self.Dead()):
                attack_res += 1
            # 如果不死，默认战斗力归0，否者将优先遵循Dead()中对战斗力的设定
            elif (self.SelfCombat < 0):
                self.SelfCombat = 0

        # 注入攻击事件
        event = MsyEvent.GetDmg(
            card=self,
            shieldDmg=shiedDmg,
            cureDmg=cureDmg
        )
        self.ThisGame.eventMonitoring.Occurrence(event)

        return attack_res, cureDmg

    # 返回伤害数值，0 表示免疫了伤害
    def _getDamage(self, num, effectLabel):
        self.SelfCombat -= num
        return num

    # 增加基础战斗力
    # 返回 0 表示效果失败，1 表示效果成功
    def AddSelfCombat(self, num, effectLabel):
        num = self._addSelfCombat(num, effectLabel)
        res = 0
        if (num > 0):
            res += 1
            self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + " 基础战斗力+ " + str(num))
        else:
            self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + " 免疫了效果 ")
        return res

    # 受伤实现相同， 0 为免疫
    def _addSelfCombat(self, num, effectLabel):
        self.SelfCombat += num
        return num

    # 死亡，可以执行这个函数进行即死
    def Dead(self) -> bool:
        if (self.Alive and self._dead()):
            self.Alive = False

            # 发送死亡信号
            event = MsyEvent.Death(
                card=self,
            )
            self.ThisGame.eventMonitoring.Occurrence(event)

            # 吊销指令卡牌
            self.OwnPlayer.ThrowCards_withUIDList(self._comCardUIDList)

            # 死亡只能用来注销非死亡触发器
            if (self.Monitor_Pop):
                self.ThisGame.eventMonitoring.UnBundledTrigger("Pop", self)
            if (self.Monitor_GetDmg):
                self.ThisGame.eventMonitoring.UnBundledTrigger("GetDmg", self)

            # 注销存在时效果
            if (len(self.ExiEffectOn) > 0):
                self.ThisGame.UnRegisterExisEffect(self)

            return True
        else:
            return False

    # 返回是否死亡
    def _dead(self) -> bool:
        return True

    # 死亡触发器,用于技能
    #   死亡event = {
    #       "type" : "Death",
    #       "para" : [UID,OwnNO]
    #   }
    #
    def DeathProcessing(self, event:Death):
        self._deathProcessing(event)
        # 在死亡触发操作中 注销死亡触发器，保证死亡监测函数可以使用
        UID = event['para'][0]
        if (UID == self.UID and self.Monitor_Death):
            self.ThisGame.eventMonitoring.UnBundledTrigger("Death", self)
        return True

    def _deathProcessing(self, event:Death):
        return True

    def PopProcessing(self, event:Pop):
        self._popProcessing(event)

    def _popProcessing(self, event:Pop):
        return True

    def GetDmgProcessing(self, event:GetDmg):
        self._getDmgProcessing(event)

    def _getDmgProcessing(self, event:GetDmg):
        return True

    # 转换长字串
    def lstr(self) -> str:
        return "[{},{},{},{},{},lv{},{},\n{}]".format(self.UID, self.Type, self.Name, self.CantoLines, self.Combat(),
                                                      self.Level, self.Label, self.Desc)

    # 转换短字串
    def sstr(self) -> str:
        # return "[{},{},{},lv{}]".format(self.UID, self.Name, self.Combat(), self.Level)
        cbt = self.Combat()
        res = ""
        res += "[{},{},{}".format(self.UID, self.Name, self.SelfCombat)
        if (cbt > self.SelfCombat):    res += "(+%.1f)"%(cbt - self.SelfCombat)
        if (cbt < self.SelfCombat):    res += "(-%.1f)"%(self.SelfCombat - cbt)
        if (self.ShieldValue > 0):       res += "[%.1f]"%(self.ShieldValue)
        res += ",lv{}]".format(self.Level)
        return res

    # 添加效果
    def AddStatus(self, status):
        if (self._addStatus(status)):
            self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + " 被施加效果 " + status.Name)
            return True
        else:
            self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + " 免疫了效果 " + status.Name)
            return False

    def _addStatus(self, status):
        status.Apply(self)
        return True

    # 移除效果
    def RemStatus(self, status):
        try:
            if (self._remStatus(status)):
                self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + " 消除效果 " + status.Name)
        except Exception as e:
            print("card remove status error", self.UID, status.UID, repr(e))

    def _remStatus(self, status):
        self.Status.pop(status.UID)
        return True

    # 添加 减少 护盾
    def AddShield(self, num, label):
        adv = self._addShield(num, label)
        if (adv > 0):
            self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + " 护盾值增加 " + str(adv))
        return adv

    def _addShield(self, num, label):
        self.ShieldValue += num
        return num

    def DevShield(self, num, label):
        sdmg = self._devShield(num, label)
        if (sdmg > 0):
            self.ThisGame.Print_Message("单位 " + self.Name + "(" + str(self.UID) + ")" + " 护盾值减少 " + str(sdmg))
        return sdmg

    def _devShield(self, num, label):
        sdmg = min(self.ShieldValue, num)
        self.ShieldValue -= sdmg
        return sdmg

    # 转换dict
    def dict(self) -> dict:
        res = {
            "Name": self.Name,
            "Desc": self.Desc,
            "Type": self.Type,
            "CantoLines": list(self.CantoLines),
            "Combat": self.Combat(),
            "Label": list(self.Label),  # json 不允许出现 set
            "Level": self.Level,
            "SelfCombat": self.SelfCombat,
            "Status": toDict(list(self.Status.values())),
            "UID": self.UID,
        }
        return res

    def pack(self) -> dict:
        return {
            "Name": self.Name,
            "Desc": self.Desc,
            "Type": self.Type,
            "Label": list(self.Label),  # json 不允许出现 set
            "OwnNO": self.OwnNO,
            "Level": self.Level,
            "UID": self.UID,
            "CantoLines": list(self.CantoLines),
            "SelfCombat": self.SelfCombat,
            "Combat": self.Combat(),
            "Status": PackList(list(self.Status.values())),
            # 释放目标需求，[选目标数，必须选全，选行数目，必须选全]
            "UnleashOp": self.UnleashOp,
            # 需要选择多少张牌进行献祭，（随机献祭不算在内）
            "SelDedication": self.SelDedication,
        }
