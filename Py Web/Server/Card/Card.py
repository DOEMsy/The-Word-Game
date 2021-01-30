from ExternalLibrary.ExternalLibrary import GetUID


class Card(object):

    def __init__(self, name: str, desc: str):
        self.Name = name  # 名称
        self.Desc = desc  # 介绍
        self.Type = "None"  # 卡牌类型
        self.UID = None  # 唯一标识

    # 抽入手中，返回值必须为True
    # 普通卡牌抽入手中才有UID
    def Pump(self) -> bool:
        self.UID = GetUID()
        return True

    # 在手上
    def OnHand(self) -> bool:
        return True

    # 出牌
    def Play(self, player, ins) -> bool:
        return False

    # 弃牌，返回值必须为True
    def Aban(self) -> bool:
        return True

    # 字符串
    def __str__(self) -> str:
        return "[{},{},{}]".format(self.Name, self.Desc, self.Type)

    def dict(self) -> dict:
        return {
            "Name": self.Name,
            "Desc": self.Desc,
            "Type": self.Type,
            "UID" : self.UID,
        }