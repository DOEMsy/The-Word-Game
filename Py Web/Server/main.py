import random
from copy import deepcopy
from random import randint

from ExternalLibrary.ExternalLibrary import GetRandCard
from Game.Game import Game
import Mod
import time
import random
import numpy as np

seed = int(time.time())
random.seed(seed)
np.random.seed(seed)

game = Game()
game.StartServer()

# test↓
'''
for i in range(10):
    game.Players[0].RawPile.append(Goblin())
    game.Players[0].RawPile.append(ImperialSoldier())
    game.Players[0].RawPile.append(Wolf())
    game.Players[1].RawPile.append(Goblin())
    game.Players[1].RawPile.append(ImperialSoldier())
    game.Players[1].RawPile.append(Wolf())
'''
'''
print(    GetRandUnrepeatCard({
        "Type": "UnitCard",
    }, 20) + \
    GetRandUnrepeatCard({
        "Type": "SkillCard",
    }, 10)
)

os.system("pause")
'''
# 双方随机获取牌
# paidui = GetRandCard({"Type": "UnitCard", }, 40) \
#          + GetRandCard({"Type": "SkillCard", }, 20)

paidui  =   GetRandCard({"Level":1},16)\
        +   GetRandCard({"Level":2},14)\
        +   GetRandCard({"Level":3},14)\
        +   GetRandCard({"Level":4},10)\
        +   GetRandCard({"Level":5},6)\

paidui.sort(key=lambda a:a.Level)

#for cd in paidui:
#     print(cd.Level)


NO = randint(0,1)
for card in paidui:
    game.Players[NO].RawPile.append(card)
    NO = (NO+1)%2

# 没必要重排序，目前底层抽牌是随机的，待定
#game.Players[0].RawPile = paidui[0:len(paidui) // 2]
#game.Players[1].RawPile = paidui[len(paidui) // 2:]
#random.shuffle(game.Players[0].RawPile)
#random.shuffle(game.Players[1].RawPile)

# 调试平衡性
for cd in game.Players[0].RawPile:
    print(cd.Level,end=" ")
print()
for cd in game.Players[1].RawPile:
    print(cd.Level,end=" ")
print()

# 1 8
# 2 7
# 3 7
# 4 5
# 5 3

# test↑


game.Players[0].GetCards(10)
game.Players[1].GetCards(10)

while (game.Players[0].Health > 0 and game.Players[1].Health > 0):
    whoFirst = randint(0, 1)
    whoSec = (whoFirst + 1) % 2
    fstPlayer = game.Players[whoFirst]
    secPlayer = game.Players[whoSec]
    while ((not fstPlayer.IsAbstain) or (not secPlayer.IsAbstain)):
        game.SettlementRound()
        game.CalculateCombat()
        if(not fstPlayer.IsAbstain):
            fstPlayer.Reload_POP_POINT()
            while (not fstPlayer.POP_DONE and fstPlayer.POP_POINT>0):
                game.PrintScreen(fstPlayer.NO, True)
                game.PrintScreen(secPlayer.NO)
                game.GetAndCROInstructions(fstPlayer.NO)
                # game.DeathDetection()
                game.CalculateCombat()
        fstPlayer.SettlementOnCourtSkill(),game.CalculateCombat()
        if (not secPlayer.IsAbstain):
            secPlayer.Reload_POP_POINT()
            while (not secPlayer.POP_DONE and secPlayer.POP_POINT > 0):
                game.PrintScreen(fstPlayer.NO)
                game.PrintScreen(secPlayer.NO, True)
                game.GetAndCROInstructions(secPlayer.NO)
                # game.DeathDetection()
                game.CalculateCombat()
        secPlayer.SettlementOnCourtSkill(),game.CalculateCombat()
    game.SettlementToNextInnings()
    fstPlayer.UpLevel_POP_POINT_MAX()
    secPlayer.UpLevel_POP_POINT_MAX()
game.NormalEnd()