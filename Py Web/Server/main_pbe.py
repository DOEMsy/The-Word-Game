import random
from copy import deepcopy
from random import randint

from ExternalLibrary.ExternalLibrary import GetRandCard
from Game.Game import Game
import Mod
import time
import random
import numpy as np

from Mod.OriginalPackage.Skill import LuckyCoin, GreatPatrioticWar, LightningStrike
from Mod.OriginalPackage.Unit import Irinas, Leviathan, DemonJay, C_999, HighPriestofAltoMadike, \
    MoonbearclassAerialBattleship, K_902


seed = int(time.time())
random.seed(seed)
np.random.seed(seed)

game = Game()
game.StartServerPvP()

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

paidui = GetRandCard({"Type": "UnitCard", }, 40) \
         + GetRandCard({"Type": "SkillCard", }, 20)

random.shuffle(paidui)
random.shuffle(paidui)
random.shuffle(paidui)

for _ in range(10):
    game.Players[0].Pump(DemonJay().Concre())
    game.Players[0].Pump(K_902().Concre())
game.Players[1].Pump(C_999().Concre())

game.Players[1].Pump(HighPriestofAltoMadike().Concre())
#game.Players[1].RawPile = paidui[len(paidui) // 2:]

random.shuffle(game.Players[0].RawPile)
random.shuffle(game.Players[1].RawPile)

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