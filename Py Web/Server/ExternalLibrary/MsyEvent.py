import _thread
from threading import Lock
from time import sleep


class EventMonitoring(object):
    def __init__(self):
        self.ThisGame = None
        self.events = []  # 总线
        self.events_size = 0  # 总线大小
        self.Triggers = {
            "Death":{},
            "Pop":{},
        }  # 触发器
        '''
            event = [
                {
                    "type":"",  #事件类型
                    "para":[    #事件参数

                    ]
                }
            ]
        '''
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
        try:
            self.Triggers[type].pop(trigger.UID)
        except:
            pass
        self.eventLock.release()

    # 处理事件
    def HandleEvents(self):
        while True:
            event = None
            self.eventLock.acquire()
            try:
                event = self.events.pop(0)
                self.events_size -= 1
            except:
                pass
            self.eventLock.release()

            if (event != None):
                # 需要修改游戏数据，获取游戏锁
                self.ThisGame.gameLock.acquire()
                # 单位死亡
                if (event["type"] == "Death"):
                    for trig in list(self.Triggers[event["type"]].values()):
                        try:
                            trig.DeathProcessing(event)
                        except:
                            pass
                # 玩家出牌
                elif (event["type"] == "Pop"):
                    for trig in list(self.Triggers[event["type"]].values()):
                        try:
                            trig.PopProcessing(event)
                        except:
                            pass
                # 待定
                elif (event["type"] == "?"):
                    pass
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
