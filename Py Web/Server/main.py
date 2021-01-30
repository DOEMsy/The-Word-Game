from copy import deepcopy
from random import randint

from ExternalLibrary.ExternalLibrary import GetRandCard
from Game.Game import Game
import Mod

game = Game()
game.StartServer()
whoFirst = randint(0, 1)

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

game.Players[0].RawPile = GetRandCard({
    "Level": 1
}, 20)
game.Players[1].RawPile = GetRandCard({
    "Level": 1
}, 20)

# test↑
game.Players[0].GetCards(10)
game.Players[1].GetCards(10)

while (game.NumberOfBoard < 3):
    whoSec = (whoFirst + 1) % 2
    fstPlayer = game.Players[whoFirst]
    secPlayer = game.Players[whoSec]
    while ((not fstPlayer.IsAbstain) or (not secPlayer.IsAbstain)):
        if (not fstPlayer.IsAbstain):
            game.PrintScreen(fstPlayer.NO, True)
            game.PrintScreen(secPlayer.NO)
            game.GetAndCROInstructions(fstPlayer.NO)
            fstPlayer.SettlementOnCourtSkill()
            #game.DeathDetection()
            game.CalculateCombat()
        if (not secPlayer.IsAbstain):
            game.PrintScreen(fstPlayer.NO)
            game.PrintScreen(secPlayer.NO, True)
            game.GetAndCROInstructions(secPlayer.NO)
            secPlayer.SettlementOnCourtSkill()
            #game.DeathDetection()
            game.CalculateCombat()
        game.SettlementRound()
    game.SettlementToNextTurn()
