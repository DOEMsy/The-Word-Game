from random import randint, choice,seed
from time import time, sleep
from Card.Card import PopExtraPara
from ExternalLibrary.ExternalLibrary import EncodeList
from ExternalLibrary.MsyRPC import Req
PEP = PopExtraPara()
seed(time())

class Model(object):
    def __init__(self):
        self.player = None
        self.OpPlayer = None
        self.ThisGame = None
        self.board = ""
        self.move = ""

    def Init_Oup(self):
        self.data_oup_path = "Server/AI/data/foolish_{}_{}.txt".format(self.player.NO, time())
        self.save_file = open(self.data_oup_path, 'wb', buffering=0)

    def getAllTarget(self,CardSet):
        return list(CardSet.UIDCardDict.values())

    def getRandTarget(self,CardSet):
        target = choice(self.getAllTarget(CardSet))
        return target

    def getRandLine(self):
        line = choice([-3,-2,-1,1,2,3])
        return line

    def getRandHandCard(self):
        handcards = self.player.HandCards
        sz = len(handcards)
        i = randint(0,sz-1)
        card = handcards[i]
        return card,i

    def Freaze_Board(self):
        self.board = []
        for line in self.player.Lines:
            self.board.append(EncodeList(line))
        for line in self.OpPlayer.Lines:
            self.board.append(EncodeList(line))
        self.board.append(EncodeList(self.ThisGame.GlobalCard))
        self.board.append([
            self.ThisGame.DayOrNight,
            self.player.TolCombat,
            self.player.Health,
            self.player.IsAbstain,
            len(self.player.HandCards),
            len(self.player.UnitGrave),
            self.OpPlayer.TolCombat,
            self.OpPlayer.Health,
            self.OpPlayer.IsAbstain,
            len(self.OpPlayer.HandCards),
            len(self.OpPlayer.UnitGrave),
        ])
        self.board.append(EncodeList(self.player.HandCards))
        self.board = str(self.board)

    def Save_Board(self,result):
        self.save_file.write((self.board + '\n').encode())
        self.save_file.write((self.move + '\n').encode())
        self.save_file.write((str(result)+ '\n').encode())

    def randomMove(self):
        res = []
        while True:
            try:
                ins = choice(["pop"]*50 + ["pass"]*20 + ["giveup"]*1)
                self.move = [ins,[],[],[],[]]
                res = [ins]
                if(res[0]=="pop"):
                    card,i = self.getRandHandCard()
                    res += [i]
                    self.move[1] = card.encode()
                    for p in card.pop_extra_para:
                        if p==PEP.LINE:
                            l = self.getRandLine()
                            res.append(l)
                            self.move[2].append(l)
                        elif p==PEP.TUID:
                            t = self.getRandTarget(self.ThisGame)
                            res.append(t.UID)
                            self.move[3].append(t.encode())
                        elif p==PEP.THWI:
                            c,i = self.getRandHandCard()[1]
                            res.append(i)
                            self.move[4].append(c.encode())
                self.move = str(self.move)
                return res + [""]
            except Exception as e:
                print(res)
                print(e)

    def GetBestMove(self):
        # sleep(6)
        res = self.randomMove()
        req = Req(self.player.NO,res[0],res[1:])
        return req
