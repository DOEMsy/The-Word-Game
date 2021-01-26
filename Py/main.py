from random import randint
from Game.Game import Game
from Card.OriginalPackage.Unit import *

game = Game()
whoFirst = randint(0, 1)

#test↓

for i in range(10):
    game.Players[0].RawPile.append(Goblin())
    game.Players[0].RawPile.append(ImperialSoldier())
    game.Players[0].RawPile.append(Wolf())
    game.Players[1].RawPile.append(Goblin())
    game.Players[1].RawPile.append(ImperialSoldier())
    game.Players[1].RawPile.append(Wolf())

#test↑

while(game.NumberOfBoard<3):
    whoSec = (whoFirst + 1) % 2
    fstPlayer = game.Players[whoFirst]
    secPlayer = game.Players[whoSec]
    while((not fstPlayer.IsAbstain) or (not secPlayer.IsAbstain)):
        if(not fstPlayer.IsAbstain):
            game.PrintScreen(fstPlayer.NO)
            game.GetAndCROInstructions(fstPlayer.NO)
            fstPlayer.SettlementOnCourtSkill()
            game.DeathDetection()
            game.CalculateCombat()
        if(not secPlayer.IsAbstain):
            game.PrintScreen(secPlayer.NO)
            game.GetAndCROInstructions(secPlayer.NO)
            secPlayer.SettlementOnCourtSkill()
            game.DeathDetection()
            game.CalculateCombat()
        game.SettlementRound()
    game.SettlementToNextTurn()
