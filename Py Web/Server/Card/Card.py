from ExternalLibrary.ExternalLibrary import GetUID, Throw_VisualizationError, ConcretizationCard


class Card(object):

    def __init__(self, name: str, desc: str):
        self.Name = name  # 名称
        self.Desc = desc  # 介绍
        self.Type = "None"  # 卡牌类型
        self.UID = -1  # 唯一标识
        self.OwnNO = -1  # 拥有者编号 -1 中立, 0 玩家1 , 1 玩家2
        self.OwnPlayer = None
        self.ThisGame = None  # 本局游戏
        self.Location = -2  # 位置  -2 未出现 , -1 手牌 , 0 1 2 战线 ,3 全局效果
        self.visualization = False  # 具象化，没有具象化的卡牌不允许使用

    # 抽入手中，返回值必须为True
    def Pump(self, player) -> bool:
        if (not self.visualization):
            # 没有具象化，不允许使用
            Throw_VisualizationError(self)
        # 对没有存入牌库的卡牌，赋予UID
        if (self.UID == -1): self.UID = GetUID()
        self.Location = -1
        self.OwnNO = player.NO
        self.ThisGame = player.ThisGame
        self.OwnPlayer = player
        self.OwnPlayer.HandCards.append(self)
        # self.ThisGame.Print_Message("玩家 " + player.Name + "获得了 1 张卡牌")
        return True

    # 在手上
    def OnHand(self) -> bool:
        return True

    # 出牌
    def Play(self, player, ins) -> bool:
        return False

    # 弃牌，返回值必须为True
    def Aban(self) -> bool:
        self._aban()
        return True

    def _aban(self) -> bool:
        return True

    # 具现化
    def Concre(self):
        return ConcretizationCard(self)

    # 字符串
    def __str__(self) -> str:
        return "[{},{},\n{}]".format(self.Type, self.Name, self.Desc)

    def lstr(self):
        return self.__str__()

    def sstr(self):
        return self.__str__()

    def dict(self) -> dict:
        return {
            "Name": self.Name,
            "Desc": self.Desc,
            "Type": self.Type,
            "UID": self.UID,
        }

    def pack(self) -> dict:
        return {
            "Name": self.Name,
            "Desc": self.Desc,
            "Type": self.Type,
            "UID": self.UID,
        }