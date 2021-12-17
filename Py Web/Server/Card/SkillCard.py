from Card.Card import *
from ExternalLibrary.ExternalLibrary import INT
pep = PopExtraPara()

class SkillCard(Card):
    def __init__(self, name: str, desc: str, level: int, label: set, pep:list = []):
        super().__init__(name, desc, pep)
        self.Level = level  # 等级
        self.Label = label  # 标签
        self.Type = "SkillCard"  # 卡牌类型

        self.ComUnitNameUIDStr = "" # 指令绑定的单位识别标识，无则由玩家释放
        self.ComUnitUID = None # 指令绑定的单位，无则由玩家释放
        self.ComUnit = None

    # 出牌
    def Play(self, player, ins) -> bool:
        return self._play(player, ins)

    def _play(self, player, ins) -> bool:
        try:
            card_type = ins[0]
            card_uid = int(ins[1])
            if (card_uid != self.UID): return False
            to = list(map(INT, ins[2:]))
            if (card_type != self.Type):   return False
            if (not self.Debut(to)): return False
            return True
        except Exception as e:
            print("card play error:", repr(e))
            return False


    # 自施加效果启动，在部署到战场上时被调用
    def SelftoLineOn(self):
        self._selftoLineOn()
        # 注册存在时效果
        if(len(self.ExiEffectOn)>0):
            self.ThisGame.RegisterExisEffect(self)
        return True

    # 返回值一定是 true
    def _selftoLineOn(self):
        return True

    # 出牌效果
    def Debut(self, ins) -> bool:
        try:
            return self._debut(ins)
        except Exception as e:
            print("card debut error:", repr(e))

    def _debut(self, ins) -> bool:
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

    # 效果结束，相当于 Unit 中的 Dead
    def Finish(self) -> bool:
        if (self._finish()):
            # 注销存在时效果
            if (len(self.ExiEffectOn) > 0):
                self.ThisGame.UnRegisterExisEffect(self)
            return True
        return False

    def _finish(self) -> bool:
        return True

    # 场替
    def ToNextTurn(self) -> bool:
        if(self._toNextTurn()):
            # 注销存在时效果
            if (len(self.ExiEffectOn) > 0):
                self.ThisGame.UnRegisterExisEffect(self)
            return True
        return False

    def _toNextTurn(self) -> bool:
        return True

    # 转换长字串，待完善
    def lstr(self) -> str:
        return "[{},{},{},lv{},{},{},\n{}]".format(self.UID, self.Type, self.Name, self.Level, self.ComUnitNameUIDStr, self.Label, self.Desc)

    # 转换短字串，待完善
    def sstr(self) -> str:
        return "[{},{},lv{}]".format(self.UID, self.Name, self.Level)

    # 转换dict
    def dict(self) -> dict:
        res = {
            "Name": self.Name,
            "Desc": self.Desc,
            "Type": self.Type,
            "Label": list(self.Label),  # json 不允许出现 set
            "Level": self.Level,
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
        }

    def encode(self)->list:
        return [
            self.Name,
            self.Level,
            self.Location,
            self.Level,
            self.Label.__len__(),
        ]