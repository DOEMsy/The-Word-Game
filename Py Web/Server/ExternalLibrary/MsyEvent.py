import _thread
from threading import Lock
from time import sleep


class EventMonitoring(object):
    def __init__(self):
        self.ThisGame = None
        self.events = []  # 总线
        self.DeathTriggers = {}  # 死亡触发器
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
        self.eventLock.release()

    # 注册死亡触发器
    def BundledDeathTrigger(self, trigger):
        self.eventLock.acquire()
        self.DeathTriggers[trigger.UID] = trigger
        self.eventLock.release()

    # 注销死亡触发器
    def UnBundledDeathTrigger(self, trigger):
        self.eventLock.acquire()
        try:
            self.DeathTriggers.pop(trigger.UID)
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
            except:
                pass
            self.eventLock.release()

            if (event != None):
                if (event["type"] == "Death"):
                    # 需要修改游戏数据，获取游戏锁
                    self.ThisGame.gameLock.acquire()
                    for key in self.DeathTriggers:
                        self.DeathTriggers[key].DeathProcessing(event)
                    self.ThisGame.gameLock.release()

            sleep(0.05)
