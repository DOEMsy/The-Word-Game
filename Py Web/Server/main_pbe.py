import random
from copy import deepcopy
from random import randint

from ExternalLibrary.ExternalLibrary import GetRandCard
from Game.Game import Game
import Mod
import time
import random

from Mod.OriginalPackage.Skill import LuckyCoin
from Mod.OriginalPackage.Unit import Irinas


seed = int(time.time())
random.seed(seed)
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
game.Players[0].Pump(Irinas().Concre())
game.Players[0].Pump(LuckyCoin().Concre())
game.Players[1].Pump(Irinas().Concre())
game.Players[1].Pump(LuckyCoin().Concre())

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
        if (not fstPlayer.IsAbstain):
            game.PrintScreen(fstPlayer.NO, True)
            game.PrintScreen(secPlayer.NO)
            game.GetAndCROInstructions(fstPlayer.NO)
            fstPlayer.SettlementOnCourtSkill()
            # game.DeathDetection()
            game.CalculateCombat()
        if (not secPlayer.IsAbstain):
            game.PrintScreen(fstPlayer.NO)
            game.PrintScreen(secPlayer.NO, True)
            game.GetAndCROInstructions(secPlayer.NO)
            secPlayer.SettlementOnCourtSkill()
            # game.DeathDetection()
            game.CalculateCombat()
    game.SettlementToNextInnings()
game.NormalEnd()