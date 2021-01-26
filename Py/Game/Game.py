import os
import random
from copy import deepcopy

from Game.Player import Player


class Game(object):
    def __init__(self):
        self.Players = [Player('Player1', 0), Player('Player2', 1)]
        self.Players[0].OpPlayer = self.Players[1]
        self.Players[1].OpPlayer = self.Players[0]
        self.Players[0].ThisGame = self.Players[1].ThisGame = self
        self.GlobalEffect = []
        self.PlayCardQueue = []
        self.DayOrNight = random.choice([True, False])
        self.NumberOfBoard = 0

    def SettlementToNextTurn(self):
        minCombat = min(self.Players[0].TolCombat, self.Players[1].TolCombat)
        for player in self.Players:
            if (player.TolCombat == minCombat):
                player.Health -= 1

        for NO in range(2):
            player = self.Players[NO]
            player.IsAbstain = False
            for i in range(3):
                tmp = []
                line = player.Lines[i]
                for card in line:
                    if (not card.ToNextTurn()):
                        tmp.append(card)
                player.Lines[i] = deepcopy(tmp)

        tmp = []
        for card in self.GlobalEffect:
            if (not card.ToNextTurn()):
                tmp.append(card)
        self.GlobalEffect = deepcopy(tmp)

        self.NumberOfBoard += 1
        self.DayOrNight = not self.DayOrNight
        return True

    def DeathDetection(self):
        for NO in range(2):
            player = self.Players[NO]
            for i in range(3):
                tmp = []
                line = player.Lines[i]
                for card in line:
                    # 0 濒死 <0 死亡
                    if not (card.Combat() < 0 and card.Dead()):
                        tmp.append(card)
                player.Lines[i] = deepcopy(tmp)
        return True

    def SettlementRound(self):
        tmp = []
        for effect in self.GlobalEffect:
            effect.Round()
            if (not effect.Finish()):
                tmp.append(effect)
        self.GlobalEffect = deepcopy(tmp)
        return True

    def CalculateCombat(self):
        self.Players[0].CalculateCombat()
        self.Players[1].CalculateCombat()

    def PrintScreen(self, NO):
        player = self.Players[NO]
        opPlayer = player.OpPlayer
        oup = ""
        for i in range(3)[::-1]:
            oup += "{}: ".format(i + 1)
            for card in opPlayer.Lines[i]:
                oup += "{},".format(card.sstr())
            oup += "\n"
        oup += "-----------NA:{} CO:{}, HE:{} GV:{} ----------\n".format(opPlayer.Name, opPlayer.TolCombat,
                                                                         opPlayer.Health, opPlayer.IsAbstain)
        oup += "{}\n".format("Day" if (self.DayOrNight) else "Night")
        oup += "Gl: "
        for gl in self.GlobalEffect:
            oup += "{},".format(gl.sstr())
        oup += '\n'
        oup += "-----------NA:{} CO:{}, HE:{} GV:{} ----------\n".format(player.Name, player.TolCombat, player.Health,
                                                                         player.IsAbstain)
        for i in range(3):
            oup += "{}: ".format(i + 1)
            for card in player.Lines[i]:
                oup += "{},".format(card.sstr())
            oup += "\n"
        oup += "You are Player{} now\n".format(NO+1)
        oup += "HandCards:\n"
        card_i = 0
        for card in player.HandCards:
            oup += "{}. {},\n".format(card_i, card.lstr())
            card_i += 1

        os.system("cls")
        print(oup)

        return True

    def GetAndCROInstructions(self, NO):
        player = self.Players[NO]
        while (True):
            inp = input()
            ins = inp.split()
            if (len(ins) == 0): continue
            if (ins[0] == "giveup"):
                player.IsAbstain = True
                break
            elif (ins[0] == "pop"):
                if (len(ins) >= 3):
                    card_i = int(ins[1])
                    ins = ins[2:]
                    if (player.PopCard(card_i, ins)):
                        break
                    else:
                        pass
            elif (ins[0] == "get"):
                if (len(ins) >= 2):
                    player.GetCards(int(ins[1]))
                    break
            print("指令不合法，请重新输入")
        return True
