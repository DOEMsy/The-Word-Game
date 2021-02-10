import _thread
from threading import Lock
from time import sleep


class EventMonitoring(object):
    def __init__(self):
        self.ThisGame = None
        self.events = []  # 总线
        self.events_size = 0 # 总线大小
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
        self.events_size+=1
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
                self.events_size -= 1
            except:
                pass
            self.eventLock.release()

            if (event != None):
                self.ThisGame.gameLock.acquire()
                if (event["type"] == "Death"):
                    # 需要修改游戏数据，获取游戏锁

                    for key in self.DeathTriggers:
                        try:
                            self.DeathTriggers[key].DeathProcessing(event)
                        except:
                            pass
                self.ThisGame.gameLock.release()
            else:
                sleep(0.01)

    #等待事件总线为空
    def WaitingForEventsEmpty(self):
        while(True):
            sleep(0.2)
            self.eventLock.acquire()
            tmp = self.events_size
            self.eventLock.release()
            if(tmp==0): return
