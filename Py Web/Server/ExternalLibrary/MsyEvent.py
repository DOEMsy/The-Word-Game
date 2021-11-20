import _thread
from threading import Lock
from time import sleep

# from Card.UnitCard import UnitCard
# from Game.Player import Player


class Event(object):
    def __init__(self, etype):
        self.etype = etype

    def __str__(self):
        return "Event(eytpe={})".format(self.etype)

class Death(Event):
    # 死亡卡牌
    def __init__(self, card):
        super().__init__("Death")
        self.card = card

    def __str__(self):
        return "Event(eytpe={},card={})".format(self.etype,self.card.sstr())

class Pop(Event):
    # 卡牌 出牌玩家
    def __init__(self, card, player):
        super().__init__("Pop")
        self.card = card
        self.player = player

    def __str__(self):
        return "Event(eytpe={},player={})".format(self.etype,self.player.NO)

class GetDmg(Event):
    # 卡牌 护盾伤害 本体伤害
    def __init__(self, card, shieldDmg, cureDmg):
        super().__init__("GetDmg")
        self.card = card
        self.shieldDmg = shieldDmg
        self.cureDmg = cureDmg


class EventMonitoring(object):
    def __init__(self):
        self.ThisGame = None
        self.events = []  # 总线
        self.events_size = 0  # 总线大小
        self.Triggers = {
            "Death": {},  # 单位死亡
            "Pop": {},  # 玩家出牌
            "GetDmg": {},  # 单位受到攻击/受伤
        }  # 触发器

        self.eventLock = Lock()  # 总线锁

        _thread.start_new_thread(self.HandleEvents, ())

    # 注入事件
    def Occurrence(self, event: dict):
        self.eventLock.acquire()
        self.events.append(event)
        self.events_size += 1
        self.eventLock.release()

    # 注册触发器
    def BundledTrigger(self, type, trigger):
        self.eventLock.acquire()
        self.Triggers[type][trigger.UID] = trigger
        self.eventLock.release()

    # 注销触发器
    def UnBundledTrigger(self, type, trigger):
        self.eventLock.acquire()
        self.Triggers[type].pop(trigger.UID, None)
        self.eventLock.release()

    # 处理事件
    def HandleEvents(self):
        while True:
            event = None
            self.eventLock.acquire()
            if self.events_size > 0:
                event = self.events.pop(0)
                self.events_size -= 1
            self.eventLock.release()

            if (event != None):
                # 需要修改游戏数据，获取游戏锁
                self.ThisGame.gameLock.acquire()

                etype = event.etype
                # 这里必须用一个list把trig从字典中拿出来，才能支持在事件中注销触发器的操作
                for trig in list(self.Triggers[etype].values()):
                    try:
                        if (etype == "Death"):
                            trig.DeathProcessing(event)
                        elif (etype == "Pop"):
                            trig.PopProcessing(event)
                        elif (etype == "GetDmg"):
                            trig.GetDmgProcessing(event)
                    except Exception as e:
                        print("event error:", Event,repr(e))

                self.ThisGame.gameLock.release()
            else:
                sleep(0.01)

    # 等待事件总线为空
    def WaitingForEventsEmpty(self):
        while (True):
            sleep(0.2)
            self.eventLock.acquire()
            tmp = self.events_size
            self.eventLock.release()
            if (tmp == 0): return
